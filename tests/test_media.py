"""Integration tests use tiny synthetic lavfi media, never third-party footage."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import struct
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("media", ROOT / "scripts" / "media.py")
media = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(media)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
class MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.folder = Path(cls.temp.name)
        cls.source = cls.folder / "fonte com espaços; sem shell.mp4"
        media.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=red:s=160x90:r=10:d=18",
                   "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=18",
                   "-vf", "drawbox=x=0:y=0:w=iw:h=ih:color=blue:t=fill:enable='gte(t,9)'",
                   "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.case_dir = Path(tempfile.mkdtemp(dir=self.folder))
        self.plan = {"schema_version": "0.1.0", "duration_target_seconds": {"min": 1, "max": 3}, "editing": {
            "source_files": [{"id": "live", "path": str(self.source)}],
            "segments": [{"source_id": "live", "source_in_seconds": 10, "source_out_seconds": 11},
                         {"source_id": "live", "source_in_seconds": 1, "source_out_seconds": 2}],
            "captions_output_timeline": [{"start_seconds": 0.1, "end_seconds": 0.8, "text": "Olá, Brasil!", "highlight_word": "Brasil"},
                                         {"start_seconds": 1.1, "end_seconds": 1.8, "text": "Depois do corte"}],
            "output": {"width": 90, "height": 160, "fps": 10, "video_codec": "h264", "audio_codec": "aac", "pixel_format": "yuv420p"}}}

    def save(self, plan=None):
        p = self.case_dir / "plano.json"
        p.write_text(json.dumps(plan or self.plan), encoding="utf-8")
        return p

    def test_render_reorders_source_and_preserves_final_timeline(self):
        manifest = media.render(self.save(), self.case_dir / "out")
        self.assertAlmostEqual(manifest["actual_duration_seconds"], 2, delta=0.15)
        self.assertEqual(manifest["time_mapping"][1]["output_in_seconds"], 1)
        self.assertEqual(manifest["audiovisual_review"]["status"], "pending")
        self.assertFalse(manifest["audiovisual_review"]["full_watch_with_audio_done"])
        self.assertEqual(manifest["delivery"]["status"], "not_delivered")
        output = Path(manifest["outputs"]["clip.mp4"])
        streams = manifest["technical_probe"]["streams"]
        video = next(s for s in streams if s["codec_type"] == "video")
        audio = next(s for s in streams if s["codec_type"] == "audio")
        self.assertEqual((video["width"], video["height"], video["codec_name"], video["pix_fmt"]), (90, 160, "h264", "yuv420p"))
        self.assertEqual(audio["codec_name"], "aac")
        srt = Path(manifest["outputs"]["clip.srt"]).read_text()
        self.assertIn("00:00:01,100 --> 00:00:01,800", srt)
        self.assertIn("Olá, Brasil!", srt)
        ass = Path(manifest["outputs"]["clip.ass"]).read_text()
        self.assertIn("OutlineColour", ass)
        self.assertIn("{\\c&H00FFFF&}Brasil", ass)
        # Color away from captions proves the two source ranges were reordered.
        for timestamp, dominant in ((0.2, 2), (1.2, 0)):
            result = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(timestamp), "-i", str(output), "-frames:v", "1",
                                     "-vf", "crop=2:2:0:0,format=rgb24", "-f", "rawvideo", "pipe:1"], capture_output=True, check=True)
            rgb = list(result.stdout[:3])
            self.assertGreater(rgb[dominant], 180)
            self.assertLess(rgb[2 if dominant == 0 else 0], 60)
        saved = json.loads(Path(manifest["outputs"]["render-manifest.json"]).read_text())
        self.assertEqual(saved["checksums_sha256"]["clip.mp4"], media.sha256_file(output))

    def test_fifteen_second_export_and_explicit_crop(self):
        self.plan["duration_target_seconds"] = {"min": 15, "max": 30}
        self.plan["editing"]["segments"] = [{"source_id": "live", "source_in_seconds": 1, "source_out_seconds": 16}]
        self.plan["editing"]["crops"] = [{"segment_index": 0, "x": 0, "y": 0, "width": 160, "height": 90}]
        result = media.render(self.save(), self.case_dir / "out")
        self.assertAlmostEqual(result["actual_duration_seconds"], 15, delta=0.2)

    def test_contain_blur_preserves_both_edges_after_explicit_crop(self):
        source = self.case_dir / "edge-markers.mp4"
        media.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=blue:s=320x90:r=10:d=1",
                   "-vf", "drawbox=x=80:y=0:w=20:h=ih:color=red:t=fill,drawbox=x=220:y=0:w=20:h=ih:color=lime:t=fill",
                   "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)])
        self.plan["editing"]["source_files"][0]["path"] = str(source)
        self.plan["editing"]["segments"] = [{"source_id": "live", "source_in_seconds": 0, "source_out_seconds": 1,
                                              "crop": {"x": 80, "y": 0, "width": 160, "height": 90}}]
        self.plan["editing"]["captions_output_timeline"] = []
        self.plan["editing"]["output"]["fit_mode"] = "contain_blur"
        result = media.render(self.save(), self.case_dir / "out")
        self.assertEqual(result["fit_mode"], "contain_blur")
        video = next(s for s in result["technical_probe"]["streams"] if s["codec_type"] == "video")
        self.assertEqual((video["width"], video["height"]), (90, 160))
        for x, dominant in ((2, 0), (86, 1)):
            decoded = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", result["outputs"]["clip.mp4"],
                                      "-frames:v", "1", "-vf", f"crop=2:2:{x}:80,format=rgb24", "-f", "rawvideo", "pipe:1"],
                                     capture_output=True, check=True)
            self.assertGreater(decoded.stdout[dominant], 180)
            self.assertLess(decoded.stdout[2], 60)

    def test_contain_blur_normalizes_non_square_pixels_before_layout(self):
        source = self.case_dir / "anamorphic.mp4"
        media.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=white:s=160x90:r=10:d=1",
                   "-vf", "setsar=2/1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)])
        metadata = media.probe(source)
        self.assertEqual(metadata["streams"][0]["sample_aspect_ratio"], "2:1")
        self.plan["editing"]["source_files"][0]["path"] = str(source)
        self.plan["editing"]["segments"] = [{"source_id": "live", "source_in_seconds": 0, "source_out_seconds": 1}]
        self.plan["editing"]["captions_output_timeline"] = []
        self.plan["editing"]["output"]["fit_mode"] = "contain_blur"
        result = media.render(self.save(), self.case_dir / "out")
        video = next(s for s in result["technical_probe"]["streams"] if s["codec_type"] == "video")
        self.assertEqual(video["sample_aspect_ratio"], "1:1")
        decoded = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", result["outputs"]["clip.mp4"],
                                  "-frames:v", "1", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"],
                                 capture_output=True, check=True)
        # 160x90 with SAR2:1 displays as320x90 (32:9). At output width90,
        # the preserved white foreground is about25px tall, not50px (16:9).
        pixels = decoded.stdout
        bright_rows = [y for y in range(160) if min(pixels[(y*90+45)*3:(y*90+45)*3+3]) > 245]
        self.assertGreaterEqual(len(bright_rows), 22)
        self.assertLessEqual(len(bright_rows), 28)
        self.assertIn(80, bright_rows)

    def test_fractional_cuts_map_to_real_output_frames(self):
        self.plan["editing"]["segments"] = [
            {"source_id": "live", "source_in_seconds": 10, "source_out_seconds": 10.66},
            {"source_id": "live", "source_in_seconds": 1, "source_out_seconds": 1.66}]
        self.plan["editing"]["captions_output_timeline"] = [{"start_seconds": 0.7, "end_seconds": 1.3, "text": "Segundo trecho"}]
        result = media.render(self.save(), self.case_dir / "out")
        self.assertEqual(result["time_mapping"][0]["output_frames"], 7)
        self.assertAlmostEqual(result["time_mapping"][1]["output_in_seconds"], 0.7)
        self.assertAlmostEqual(result["expected_duration_seconds"], 1.4)
        self.assertAlmostEqual(result["actual_duration_seconds"], 1.4, delta=0.1)

    def test_delayed_audio_keeps_initial_silence(self):
        delayed = self.case_dir / "delayed-audio.mkv"
        media.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=red:s=160x90:r=10:d=2",
                   "-itsoffset", "1", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=1",
                   "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-c:a", "pcm_s16le", "-t", "2", str(delayed)])
        audio = next(s for s in media.probe(delayed)["streams"] if s["codec_type"] == "audio")
        self.assertAlmostEqual(float(audio["start_time"]), 1, delta=0.01)
        self.plan["editing"]["source_files"][0]["path"] = str(delayed)
        self.plan["editing"]["segments"] = [{"source_id": "live", "source_in_seconds": 0, "source_out_seconds": 2}]
        self.plan["editing"]["captions_output_timeline"] = []
        result = media.render(self.save(), self.case_dir / "out")
        decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", result["outputs"]["clip.mp4"], "-map", "0:a:0",
                                  "-ac", "1", "-ar", "48000", "-f", "f32le", "pipe:1"], capture_output=True, check=True)
        samples = [s[0] for s in struct.iter_unpack("<f", decoded.stdout)]
        def rms(start, end):
            window = samples[round(start*48000):round(end*48000)]
            return math.sqrt(sum(s*s for s in window) / len(window))
        self.assertLess(rms(0.1, 0.8), 0.001)
        self.assertGreater(rms(1.15, 1.8), 0.04)

    def test_legacy_output_in_is_validated_not_silently_ignored(self):
        self.plan["editing"]["segments"][0]["output_in"] = 50
        with self.assertRaisesRegex(media.MediaError, "output_in deve corresponder"):
            media.render(self.save(), self.case_dir / "out")
        self.plan["editing"]["segments"][0]["output_in"] = 0
        self.plan["editing"]["segments"][1]["output_in"] = 1
        result = media.render(self.save(), self.case_dir / "out")
        self.assertEqual(result["time_mapping"][1]["output_in_seconds"], 1)

    def test_selected_video_stream_index_is_used_when_cover_is_first(self):
        multi = self.case_dir / "multiple-video-streams.mkv"
        media.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "lavfi", "-i", "color=c=green:s=32x32:r=10:d=2",
                   "-f", "lavfi", "-i", "color=c=red:s=160x90:r=10:d=2", "-map", "0:v:0", "-map", "1:v:0",
                   "-c:v", "libx264", "-t", "2", str(multi)])
        original_probe = media.probe
        def probe_cover_first(path):
            result = original_probe(path)
            if Path(path).resolve() == multi.resolve():
                # Matroska drops attached_pic; simulate that metadata field only.
                # Both actual video stream indices remain real and are decoded.
                result["streams"][0]["disposition"]["attached_pic"] = 1
            return result
        self.plan["editing"]["source_files"][0]["path"] = str(multi)
        self.plan["editing"]["segments"] = [{"source_id": "live", "source_in_seconds": 0, "source_out_seconds": 2}]
        self.plan["editing"]["captions_output_timeline"] = []
        with mock.patch.object(media, "probe", side_effect=probe_cover_first):
            result = media.render(self.save(), self.case_dir / "out")
        decoded = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", result["outputs"]["clip.mp4"],
                                  "-frames:v", "1", "-vf", "crop=2:2:0:0,format=rgb24", "-f", "rawvideo", "pipe:1"],
                                 capture_output=True, check=True)
        self.assertGreater(decoded.stdout[0], 180)
        self.assertLess(decoded.stdout[1], 60)

    def test_invalid_intervals_captions_and_unsupported_effects_fail(self):
        invalid = []
        p = copy.deepcopy(self.plan); p["editing"]["segments"][0]["source_out_seconds"] = 20; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["segments"][0]["source_out_seconds"] = 9; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["segments"][0]["speed"] = 2; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["segments"][0]["source_id"] = "missing"; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["captions_output_timeline"][1]["end_seconds"] = 4; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["captions_output_timeline"][1]["start_seconds"] = 0.5; invalid.append(p)
        p = copy.deepcopy(self.plan); p["duration_target_seconds"] = {"min": 15, "max": 30}; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["overlays"] = [{"text": "não ignorar"}]; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["output"]["width"] = 91; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["output"]["fps"] = 0; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["output"]["fit_mode"] = "invalid"; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["source_files"][0]["path"] = "https://example.com/video.mp4"; invalid.append(p)
        p = copy.deepcopy(self.plan); p["editing"]["segments"][0]["source_in_seconds"] = float("nan"); invalid.append(p)
        for i, plan in enumerate(invalid):
            with self.subTest(case=i), self.assertRaises(media.MediaError):
                media.render(self.save(plan), self.case_dir / f"invalid-{i}")
            self.assertFalse((self.case_dir / f"invalid-{i}" / "clip.mp4").exists())

    def test_no_overwrite_without_explicit_flag(self):
        folder = self.case_dir / "existing"
        folder.mkdir()
        (folder / "clip.mp4").write_bytes(b"preserve")
        with self.assertRaises(media.MediaError):
            media.render(self.save(), folder)
        self.assertEqual((folder / "clip.mp4").read_bytes(), b"preserve")

    def test_even_explicit_overwrite_cannot_replace_original_source(self):
        folder = self.case_dir / "protected"
        folder.mkdir()
        source = folder / "clip.mp4"
        shutil.copyfile(self.source, source)
        self.plan["editing"]["source_files"][0]["path"] = str(source)
        before = media.sha256_file(source)
        with self.assertRaisesRegex(media.MediaError, "substituir uma fonte"):
            media.render(self.save(), folder, overwrite=True)
        self.assertEqual(media.sha256_file(source), before)

    def test_probe_and_preflight_do_not_install_dependencies(self):
        self.assertGreater(float(media.probe(self.source)["format"]["duration"]), 17)
        status = media.preflight()
        self.assertFalse(status["installs_performed"])
        self.assertFalse(status["models_downloaded"])
        self.assertTrue(status["filters"]["subtitles"])

    def test_missing_transcription_dependency_has_clear_error(self):
        with mock.patch.dict(sys.modules, {"faster_whisper": None}):
            with self.assertRaisesRegex(media.MediaError, "faster-whisper não está instalado"):
                media.transcribe(self.source, self.case_dir / "transcript.json")

    def test_transcription_checks_output_before_import_or_download(self):
        target = self.case_dir / "existing.json"
        target.write_text("preserve")
        with mock.patch.dict(sys.modules, {"faster_whisper": None}):
            with self.assertRaisesRegex(media.MediaError, "Saída já existe"):
                media.transcribe(self.source, target, model="small", allow_download=True)
        self.assertEqual(target.read_text(), "preserve")

    def test_transcription_language_options_are_forwarded_without_network(self):
        for language, expected in (("pt", "pt"), ("en", "en"), ("auto", None)):
            factory = mock.Mock()
            factory.return_value.transcribe.return_value = (iter([]), SimpleNamespace(language="en"))
            with mock.patch.dict(sys.modules, {"faster_whisper": SimpleNamespace(WhisperModel=factory)}):
                result = media.transcribe(self.source, self.case_dir / f"{language}.json", model_dir=self.case_dir, language=language)
            self.assertEqual(factory.return_value.transcribe.call_args.kwargs["language"], expected)
            self.assertTrue(factory.call_args.kwargs["local_files_only"])
            data = json.loads(Path(result["transcript_path"]).read_text())
            self.assertEqual(data["requested_language"], language)
        with self.assertRaisesRegex(media.MediaError, "language deve ser"):
            media.transcribe(self.source, self.case_dir / "invalid-language.json", language="xx")

    def test_ass_literal_text_cannot_inject_override_commands(self):
        text = media.ass_text([{"start_seconds": 0, "end_seconds": 1, "text": r"{\\pos(0,0)}Olá", "highlight_word": None}], 90, 160)
        self.assertNotIn(r"{\\pos(0,0)}", text)
        self.assertIn("｛", text)


if __name__ == "__main__":
    unittest.main()

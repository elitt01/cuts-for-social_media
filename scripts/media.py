#!/usr/bin/env python3
"""Local media toolkit; model download only with explicit flag, no publishing or paid APIs."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


class MediaError(ValueError):
    """A clear, actionable error caused by media, dependencies, or a plan."""


def run(args, *, cwd=None):
    try:
        result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise MediaError(f"Dependência ausente: {args[0]}. Execute preflight.") from exc
    if result.returncode:
        raise MediaError(f"{Path(args[0]).name} falhou ({result.returncode}): {result.stderr[-4000:]}")
    return result.stdout


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_file(value, base=None):
    if not isinstance(value, str) or not value.strip():
        raise MediaError("Informe um caminho de arquivo local não vazio.")
    if "://" in value:
        raise MediaError("URLs não são aceitas nesta CLI; forneça um arquivo local acessível.")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (Path(base) if base else Path.cwd()) / path
    path = path.resolve()
    if not path.is_file():
        raise MediaError(f"Arquivo local não encontrado: {path}")
    return path


def number(value, label, *, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise MediaError(f"{label} deve ser um número finito.")
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise MediaError(f"{label} fora do intervalo permitido.")
    return float(value)


def probe(path):
    path = local_file(str(path))
    return json.loads(run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))


def preflight():
    binaries = {}
    for name in ("ffmpeg", "ffprobe", "yt-dlp", "node"):
        executable = shutil.which(name)
        item = {"path": executable, "available": bool(executable)}
        if executable:
            try:
                flag = "-version" if name in ("ffmpeg", "ffprobe") else "--version"
                item["version"] = run([executable, flag]).splitlines()[0]
            except MediaError as exc:
                item["error"] = str(exc)
        binaries[name] = item
    filters, encoders = {}, {}
    if binaries["ffmpeg"]["available"]:
        raw_filters = run(["ffmpeg", "-hide_banner", "-filters"])
        raw_encoders = run(["ffmpeg", "-hide_banner", "-encoders"])
        filters = {name: bool(re.search(r"\b" + name + r"\s", raw_filters)) for name in
                   ("subtitles", "crop", "scale", "concat", "trim", "atrim", "loudnorm")}
        encoders = {name: bool(re.search(r"\b" + name + r"\s", raw_encoders)) for name in ("libx264", "aac")}
    return {"python": sys.version.split()[0], "binaries": binaries, "filters": filters,
            "encoders": encoders, "optional_dependencies": {
                "faster_whisper": importlib.util.find_spec("faster_whisper") is not None},
            "disk_free_bytes": shutil.disk_usage(Path.cwd()).free,
            "installs_performed": False, "models_downloaded": False}


def seconds_stamp(seconds, *, ass=False):
    factor = 100 if ass else 1000
    ticks = round(seconds * factor)
    whole, remainder = divmod(ticks, factor)
    hours, rest = divmod(whole, 3600)
    minutes, secs = divmod(rest, 60)
    return (f"{hours}:{minutes:02}:{secs:02}.{remainder:02}" if ass else
            f"{hours:02}:{minutes:02}:{secs:02},{remainder:03}")


def validate_captions(items, duration):
    if not isinstance(items, list):
        raise MediaError("captions_output_timeline deve ser uma lista.")
    cleaned = []
    previous_end = 0.0
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise MediaError(f"Legenda {i} deve ser um objeto.")
        start = number(item.get("start_seconds"), f"Legenda {i}: início", minimum=0)
        end = number(item.get("end_seconds"), f"Legenda {i}: fim", minimum=0)
        if end <= start or end > duration + 0.001:
            raise MediaError(f"Legenda {i} tem intervalo inválido ou excede a timeline final.")
        if start < previous_end - 0.001:
            raise MediaError("Legendas devem estar em ordem, sem sobreposição nesta V1.")
        text = item.get("text")
        if not isinstance(text, str) or not text.strip() or any(ord(c) < 32 and c not in "\n\t" for c in text):
            raise MediaError(f"Legenda {i} precisa de texto válido.")
        highlight = item.get("highlight_word")
        if highlight is not None and (not isinstance(highlight, str) or not highlight or highlight not in text):
            raise MediaError(f"Legenda {i}: highlight_word deve ocorrer no texto.")
        cleaned.append({"start_seconds": start, "end_seconds": end, "text": text, "highlight_word": highlight})
        previous_end = end
    return cleaned


def srt_text(captions):
    return "\n\n".join(f"{i}\n{seconds_stamp(c['start_seconds'])} --> {seconds_stamp(c['end_seconds'])}\n{c['text']}"
                        for i, c in enumerate(captions, 1)) + ("\n" if captions else "")


def ass_escape(text):
    # Fullwidth braces/backslash prevent ASS override injection from source text.
    return text.replace("\\", "＼").replace("{", "｛").replace("}", "｝").replace("\n", "\\N").replace("\t", " ")


def ass_text(captions, width, height):
    font_size = max(16, round(height * 0.035))
    outline = max(1, round(height * 0.002))
    margin = round(height * 0.16)
    side = round(width * 0.08)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,{font_size},&H00FFFFFF,&H0000FFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,{outline},0,2,{side},{side},{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for c in captions:
        body = ass_escape(c["text"])
        if c.get("highlight_word"):
            word = ass_escape(c["highlight_word"])
            body = body.replace(word, "{\\c&H00FFFF&}" + word + "{\\c&HFFFFFF&}", 1)
        lines.append(f"Dialogue: 0,{seconds_stamp(c['start_seconds'], ass=True)},{seconds_stamp(c['end_seconds'], ass=True)},Default,,0,0,0,,{body}")
    return header + "\n".join(lines) + "\n"


def transcribe(path, output, *, model=None, model_dir=None, allow_download=False, language="pt"):
    path = local_file(str(path))
    if language not in ("pt", "en", "auto"):
        raise MediaError("language deve ser pt, en ou auto.")
    target = Path(output).resolve()
    if target.exists():
        raise MediaError(f"Saída já existe: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise MediaError("faster-whisper não está instalado. Instale requirements-optional.txt se quiser transcrever; preflight não instala nada.") from exc
    if model_dir:
        model_value = str(Path(model_dir).resolve())
        if not Path(model_value).is_dir():
            raise MediaError("--model-dir precisa apontar para um modelo local CTranslate2 existente.")
    else:
        model_value = model or "small"
        if not allow_download:
            raise MediaError("Informe --model-dir com um modelo local, ou --allow-model-download para autorizar baixar o modelo indicado.")
    engine = WhisperModel(model_value, device="cpu", compute_type="int8", local_files_only=not allow_download)
    segments, info = engine.transcribe(str(path), language=None if language == "auto" else language, word_timestamps=True, vad_filter=True)
    data = {"schema_version": "0.1.0", "source_file": str(path), "language": info.language,
            "time_reference": "input_file", "source_offset_seconds": 0,
            "engine": "faster-whisper", "model": model_value, "requested_language": language, "review_status": "pending", "segments": []}
    for segment in segments:
        data["segments"].append({"start_seconds": segment.start, "end_seconds": segment.end, "text": segment.text,
            "words": [{"start_seconds": w.start, "end_seconds": w.end, "text": w.word, "probability": w.probability}
                      for w in (segment.words or [])]})
    if target.exists():
        raise MediaError(f"Saída já existe: {target}")
    write_json(target, data)
    return {"transcript_path": str(target), "review_status": "pending", "time_reference": "input_file"}


def load_plan(plan_path):
    path = local_file(str(plan_path))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise MediaError(f"Não foi possível ler JSON do plano: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("editing"), dict):
        raise MediaError("O plano precisa conter o objeto editing.")
    return path, data, data["editing"]


def render(plan_path, output_dir, *, overwrite=False):
    plan_path, plan, editing = load_plan(plan_path)
    # Reject unsupported editing requests rather than silently ignoring them.
    for field in ("overlays", "audio_assets"):
        if editing.get(field):
            raise MediaError(f"editing.{field} ainda não é renderizado nesta V1. Prepare esses elementos fora desta CLI.")
    source_items = editing.get("source_files")
    segment_items = editing.get("segments")
    if not isinstance(source_items, list) or not source_items or not isinstance(segment_items, list) or not segment_items:
        raise MediaError("Preencha editing.source_files e editing.segments antes de renderizar.")
    output = editing.get("output") or {}
    if not isinstance(output, dict):
        raise MediaError("editing.output deve ser um objeto.")
    width = number(output.get("width", 1080), "Largura", minimum=16, maximum=4096)
    height = number(output.get("height", 1920), "Altura", minimum=16, maximum=4096)
    if width % 2 or height % 2 or width != int(width) or height != int(height):
        raise MediaError("Largura e altura devem ser inteiros pares para yuv420p.")
    width, height = int(width), int(height)
    fps_value = output.get("fps", 30)
    fps = number(30 if fps_value is None else fps_value, "FPS", minimum=1, maximum=120)
    fit_mode = output.get("fit_mode", "cover")
    if fit_mode not in ("cover", "contain_blur"):
        raise MediaError("editing.output.fit_mode deve ser cover ou contain_blur.")
    if output.get("video_codec", "h264") not in ("h264", "libx264") or output.get("audio_codec", "aac") != "aac" or output.get("pixel_format", "yuv420p") != "yuv420p":
        raise MediaError("Esta V1 exporta apenas H264/AAC/yuv420p.")
    sources, source_order = {}, []
    for item in source_items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"] or item["id"] in sources:
            raise MediaError("Cada fonte precisa de id textual único e path local.")
        source_path = local_file(item.get("path"), plan_path.parent)
        metadata = probe(source_path)
        videos = [s for s in metadata["streams"] if s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic")]
        if not videos:
            raise MediaError(f"Fonte sem stream de vídeo: {source_path}")
        duration = number(float(metadata.get("format", {}).get("duration", 0)), "Duração da fonte", minimum=0.001)
        sar_text = videos[0].get("sample_aspect_ratio")
        try:
            sar = 1.0 if sar_text in (None, "N/A", "0:1", "0/1") else float(Fraction(sar_text.replace(":", "/")))
        except (ValueError, TypeError, ZeroDivisionError, AttributeError) as exc:
            raise MediaError(f"Sample aspect ratio inválido: {sar_text}") from exc
        sar = number(sar, "Sample aspect ratio", minimum=0.000001)
        audios = [s for s in metadata["streams"] if s["codec_type"] == "audio"]
        sources[item["id"]] = {"path": source_path, "index": len(source_order), "duration": duration,
            "video": videos[0], "sar": sar, "audio": audios[0] if audios else None, "has_audio": bool(audios)}
        source_order.append(item["id"])
    crop_items = editing.get("crops") or []
    if not isinstance(crop_items, list):
        raise MediaError("editing.crops deve ser lista.")
    crop_by_segment = {}
    for item in crop_items:
        if not isinstance(item, dict) or isinstance(item.get("segment_index"), bool) or not isinstance(item.get("segment_index"), int) or not 0 <= item["segment_index"] < len(segment_items):
            raise MediaError("Cada crop precisa de segment_index válido (começando em zero).")
        if item["segment_index"] in crop_by_segment:
            raise MediaError("Crop duplicado para o mesmo segmento.")
        crop_by_segment[item["segment_index"]] = item
    timeline, filters, duration = [], [], 0.0
    for i, item in enumerate(segment_items):
        if not isinstance(item, dict) or item.get("source_id") not in sources:
            raise MediaError(f"Segmento {i}: source_id inexistente.")
        if item.get("speed", 1) != 1:
            raise MediaError("Mudança de velocidade não é suportada nesta V1.")
        source = sources[item["source_id"]]
        start = number(item.get("source_in_seconds", item.get("source_in")), f"Segmento {i}: início", minimum=0)
        end = number(item.get("source_out_seconds", item.get("source_out")), f"Segmento {i}: fim", minimum=0)
        if end <= start or end > source["duration"] + 0.001:
            raise MediaError(f"Segmento {i}: intervalo inválido ou além da fonte.")
        output_frames = max(1, round((end - start) * fps))
        segment_duration = output_frames / fps
        for output_start_field in ("output_in_seconds", "output_in"):
            if output_start_field in item and abs(number(item[output_start_field], output_start_field) - duration) > 0.001:
                raise MediaError(f"{output_start_field} deve corresponder à concatenação sem lacunas.")
        crop = item.get("crop", crop_by_segment.get(i))
        crop_filter = ""
        if crop:
            if not isinstance(crop, dict) or crop.get("units", "pixels") != "pixels":
                raise MediaError("Crop deve usar objeto com units=pixels.")
            x, y, cw, ch = [number(crop.get(k), f"Crop {i}: {k}", minimum=0) for k in ("x", "y", "width", "height")]
            if not cw or not ch or x + cw > source["video"]["width"] or y + ch > source["video"]["height"]:
                raise MediaError("Crop excede os limites da fonte ou está vazio.")
            crop_filter = f"crop={cw:g}:{ch:g}:{x:g}:{y:g},"
        # Autocenter is geometric, not face/speaker tracking.
        # Preserve each stream's timestamp relative to the same segment origin.
        # Independent PTS-STARTPTS would erase a delayed audio stream's offset.
        # Crop coordinates belong to source pixels. Then normalize their display
        # aspect before either layout so setsar=1 cannot deform anamorphic media.
        square_pixels = (f"scale=w='max(2,round(iw*{source['sar']:.12g}/2)*2)':h=ih,setsar=1,"
                         if abs(source["sar"] - 1) > 1e-9 else "setsar=1,")
        source_filter = (f"[{source['index']}:{source['video']['index']}]trim=start={start:g}:end={end:g},"
                         f"setpts=PTS-{start:g}/TB,{crop_filter}{square_pixels}")
        if fit_mode == "contain_blur":
            filters.append(source_filter + f"split=2[bgsrc{i}][fgsrc{i}]")
            filters.append(f"[bgsrc{i}]scale={width}:{height}:force_original_aspect_ratio=increase,"
                           f"crop={width}:{height},setsar=1,gblur=sigma=20:steps=1,eq=brightness=-0.10:saturation=0.85[bg{i}]")
            filters.append(f"[fgsrc{i}]scale={width}:{height}:force_original_aspect_ratio=decrease,setsar=1[fg{i}]")
            layout_filter = f"[bg{i}][fg{i}]overlay=x=(W-w)/2:y=(H-h)/2:shortest=1,"
        else:
            layout_filter = source_filter + f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,"
        vf = (layout_filter + f"fps=fps={fps:g}:start_time=0,tpad=stop_mode=clone:stop_duration={2/fps:.9f},"
              f"trim=end_frame={output_frames},setpts=N/({fps:g}*TB),format=yuv420p[v{i}]")
        filters.append(vf)
        if source["has_audio"]:
            filters.append(f"[{source['index']}:{source['audio']['index']}]atrim=start={start:g}:end={end:g},asetpts=PTS-{start:g}/TB,aresample=48000:async=1:first_pts=0,aformat=sample_fmts=fltp:channel_layouts=stereo,apad,atrim=duration={segment_duration:.9f}[a{i}]")
        else:
            filters.append(f"anullsrc=channel_layout=stereo:sample_rate=48000,atrim=duration={segment_duration:.9f},asetpts=PTS-STARTPTS[a{i}]")
        timeline.append({"source_id": item["source_id"], "source_in_seconds": start, "source_out_seconds": end,
                         "output_in_seconds": duration, "output_out_seconds": duration + segment_duration,
                         "output_frames": output_frames, "output_duration_seconds": segment_duration})
        duration += segment_duration
    target_duration = plan.get("duration_target_seconds")
    if target_duration is not None:
        if not isinstance(target_duration, dict):
            raise MediaError("duration_target_seconds deve conter min e max.")
        lower = number(target_duration.get("min"), "Duração mínima", minimum=0)
        upper = number(target_duration.get("max"), "Duração máxima", minimum=lower)
        if duration < lower - 0.001 or duration > upper + 0.001:
            raise MediaError("Duração planejada fora de duration_target_seconds; ajuste o corte ou a faixa explícita.")
    captions = validate_captions(editing.get("captions_output_timeline", []), duration)
    targets = ["clip.mp4", "clip.srt", "clip.ass", "render-manifest.json"]
    directory = Path(output_dir).expanduser().resolve()
    protected = {plan_path, *(source["path"] for source in sources.values())}
    if any((directory / name).resolve() in protected for name in targets):
        raise MediaError("A saída não pode substituir uma fonte ou o plano, mesmo com --overwrite.")
    if any((directory / name).exists() for name in targets) and not overwrite:
        raise MediaError("Saída já existe; escolha outra pasta ou use --overwrite explicitamente.")
    status = preflight()
    if not all(status["binaries"][n]["available"] for n in ("ffmpeg", "ffprobe")) or not all(status["encoders"].values()):
        raise MediaError("Render precisa de ffmpeg/ffprobe com encoders libx264 e aac.")
    if captions and not status["filters"].get("subtitles"):
        raise MediaError("O FFmpeg instalado não tem filtro subtitles/libass para legendas.")
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="render-", dir=directory) as temporary:
        temporary = Path(temporary)
        (temporary / "clip.srt").write_text(srt_text(captions), encoding="utf-8")
        (temporary / "clip.ass").write_text(ass_text(captions, width, height), encoding="utf-8")
        concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(len(timeline)))
        filters.append(concat_inputs + f"concat=n={len(timeline)}:v=1:a=1[joined][audio]")
        filters.append("[joined]subtitles=clip.ass[video]" if captions else "[joined]null[video]")
        (temporary / "filtergraph.txt").write_text(";\n".join(filters), encoding="utf-8")
        args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y"]
        for source_id in source_order:
            args.extend(["-i", str(sources[source_id]["path"])])
        args.extend(["-filter_complex_script", "filtergraph.txt", "-filter_complex_threads", "1", "-map", "[video]", "-map", "[audio]",
                     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                     "-ar", "48000", "-movflags", "+faststart", "-t", f"{duration:.6f}", "clip.mp4"])
        run(args, cwd=temporary)
        metadata = probe(temporary / "clip.mp4")
        actual_duration = float(metadata["format"]["duration"])
        if abs(actual_duration - duration) > max(0.2, 2 / fps):
            raise MediaError("Duração exportada difere do plano; arquivo não foi aprovado tecnicamente.")
        files = {name: str(directory / name) for name in targets}
        manifest = {"schema_version": "0.1.0", "run_id": plan.get("run_id"), "status": "technically_verified/audiovisual_pending",
                    "plan_path": str(plan_path), "expected_duration_seconds": duration, "actual_duration_seconds": actual_duration,
                    "time_mapping": timeline, "caption_time_reference": "output", "caption_count": len(captions),
                    "fit_mode": fit_mode,
                    "outputs": files, "checksums_sha256": {name: sha256_file(temporary/name) for name in targets[:3]},
                    "technical_probe": metadata, "audiovisual_review": {"status": "pending", "full_watch_with_audio_done": False,
                    "context_fidelity": "not_checked", "caption_accuracy": "not_checked", "mobile_readability": "not_checked"},
                    "delivery": {"status": "not_delivered"}, "limitations": ["Layout geométrico; sem rastreamento de rostos.",
                    "Sem seleção semântica, memes, música ou efeitos automáticos.", "Legendas precisam estar na timeline final e ser revisadas."]}
        write_json(temporary / "render-manifest.json", manifest)
        for name in targets:
            os.replace(temporary / name, directory / name)
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("preflight", help="Detecta dependências, sem instalar nada")
    p = subs.add_parser("probe", help="Inspeciona um arquivo local")
    p.add_argument("input")
    p.add_argument("--output")
    p = subs.add_parser("transcribe", help="Transcreve em CPU, com idioma selecionável e faster-whisper opcional")
    p.add_argument("input")
    p.add_argument("--output", required=True)
    p.add_argument("--model")
    p.add_argument("--model-dir")
    p.add_argument("--allow-model-download", action="store_true")
    p.add_argument("--language", choices=("pt", "en", "auto"), default="pt")
    p = subs.add_parser("render", help="Renderiza um plano; revisão audiovisual fica pendente")
    p.add_argument("plan")
    p.add_argument("--output-dir", required=True)
    p.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            result = preflight()
        elif args.command == "probe":
            result = probe(args.input)
            if args.output:
                target = Path(args.output).resolve()
                if target.exists():
                    raise MediaError("A saída de probe já existe; escolha outro caminho.")
                target.parent.mkdir(parents=True, exist_ok=True)
                write_json(target, result)
        elif args.command == "transcribe":
            result = transcribe(args.input, args.output, model=args.model, model_dir=args.model_dir,
                                allow_download=args.allow_model_download, language=args.language)
        else:
            result = render(args.plan, args.output_dir, overwrite=args.overwrite)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Recipe for the documented 1080x720 Alanzoka radio source; not a general tracker."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font", type=Path, default=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    parser.add_argument("--bold-font", type=Path, default=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
    args = parser.parse_args()
    source, target = args.input.resolve(), args.output.resolve()
    manifest = target.with_suffix(".json")
    if not source.is_file() or source == target or target.exists() or manifest.exists():
        parser.error("Fonte deve existir; MP4 e manifesto de saída precisam ser novos e diferentes da fonte.")
    if not args.font.is_file() or not args.bold_font.is_file():
        parser.error("Informe --font e --bold-font com fontes TTF locais existentes.")
    metadata = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(source)
    ]))
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    if (video["width"], video["height"]) != (1080, 720) or float(metadata["format"]["duration"]) < 23:
        parser.error("Esta receita tem crops fixos para a fonte documentada de 1080x720, com pelo menos 23s.")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="alanzoka-render-", dir=target.parent) as temp:
        work = Path(temp)
        shutil.copyfile(args.font, work / "regular.ttf")
        shutil.copyfile(args.bold_font, work / "bold.ttf")
        texts = {
            "credit": "ALANZOKA  •  FONTE: @ALANZOKAREACT",
            "hook1": "O Alan só queria",
            "hook2": "curtir a rádio...",
            "payoff1": "a direção ficou",
            "payoff2": "em segundo plano",
        }
        for name, value in texts.items():
            (work / f"{name}.txt").write_text(value, encoding="utf-8")
        def text_filter(name, y, *, size=60, color="white", enable=None, font="bold.ttf"):
            value = (f"drawtext=fontfile={font}:textfile={name}.txt:expansion=none:"
                     f"fontsize={size}:fontcolor={color}:borderw=4:bordercolor=black@0.85:"
                     f"shadowcolor=black@0.6:shadowx=2:shadowy=3:x=(w-text_w)/2:y={y}")
            return value + (f":enable='{enable}'" if enable else "")
        filters = [
            "[0:v:0]trim=start=0:end=23,setpts=PTS,split=2[camsrc][gamesrc]",
            "[camsrc]crop=330:210:738:120,scale=1080:-2,crop=1080:600:0:0,setsar=1,pad=1080:640:0:0:color=0x101010[cam]",
            "[gamesrc]crop=590:700:140:20,scale=1080:1280,setsar=1,eq=brightness=0.025:contrast=1.03[game]",
            "[cam][game]vstack=inputs=2[stack]",
            "[stack]" + ",".join([
                text_filter("credit", 606, size=23, font="regular.ttf"),
                "drawbox=x=0:y=636:w=iw:h=4:color=0xffdc44:t=fill",
                text_filter("hook1", 694, enable="between(t,0,3.3)"),
                text_filter("hook2", 766, color="0xffdc44", enable="between(t,0,3.3)"),
                text_filter("payoff1", 1410, size=57, enable="between(t,19.7,22.7)"),
                text_filter("payoff2", 1478, size=57, color="0xffdc44", enable="between(t,19.7,22.7)"),
                "fps=30,trim=end_frame=690,setpts=N/(30*TB),format=yuv420p",
            ]) + "[v]",
            "[0:a:0]atrim=start=0:end=23,asetpts=PTS,aresample=48000:async=1:first_pts=0,apad,atrim=end=23,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.03,afade=t=out:st=22.9:d=0.1[a]",
        ]
        (work / "filters.txt").write_text(";\n".join(filters), encoding="utf-8")
        rendered = work / "render.mp4"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-n", "-i", str(source),
            "-filter_complex_script", "filters.txt", "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-c:a", "aac", "-b:a", "160k",
            "-ar", "48000", "-t", "23", "-map_metadata", "-1", "-movflags", "+faststart",
            "-metadata", "title=Alanzoka no GTA 6 — a rádio virou prioridade",
            "-metadata", "comment=Fonte: Alanzoka Reactions. Textos editoriais; não são transcrição de fala ou música.",
            str(rendered),
        ], cwd=work, check=True)
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(rendered)
        ]))
        if abs(float(probe["format"]["duration"]) - 23) > 0.1:
            raise RuntimeError("Duração final inesperada.")
        with target.open("xb") as destination, rendered.open("rb") as content:
            shutil.copyfileobj(content, destination)
    result = {
        "source_url": "https://x.com/alanzokareact/status/2123039497860321295",
        "source_file": str(source), "output_file": str(target),
        "source_interval_seconds": [0, 23], "actual_duration_seconds": probe["format"]["duration"],
        "layout": "fixed_source_crops_camera_above_gameplay", "text_origin": "editorial_not_transcript",
        "sha256": hashlib.file_digest(target.open("rb"), "sha256").hexdigest(),
        "full_watch_with_audio_done": False, "delivery_status": "not_delivered",
        "limitations": ["Crops específicos desta fonte; não há rastreamento.",
                        "Revisão técnica e de quadros não equivalem a revisão integral com áudio."],
    }
    with manifest.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

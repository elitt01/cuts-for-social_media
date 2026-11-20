# Exemplos sintéticos

Estes arquivos exercitam contratos e ferramentas. Não representam lives reais, tendências ou inspeções de pessoas. As declarações de candidatos são fictícias; o render usa padrão visual e tom sonoro gerados localmente.

## Avaliador

```bash
python3 scripts/score_candidates.py examples/candidatos.sinteticos.json
```

O candidato `a-completo-75` deve ser escolhido. O candidato incompleto conserva um intervalo de potencial; o candidato com gancho fraco não se torna elegível apenas por ter nota total alta. A pontuação é uma heurística, não uma probabilidade.

## Render de 18 segundos

Executar a partir da raiz, em uma pasta de demonstração ainda sem outputs. Requer FFmpeg/ffprobe disponíveis. Usar o equivalente de `mkdir` do sistema quando necessário.

```bash
mkdir -p runs/demo
ffmpeg -hide_banner -loglevel error -nostdin -n -f lavfi -i "testsrc2=size=640x360:rate=30:duration=24" -f lavfi -i "sine=frequency=440:sample_rate=48000:duration=24" -c:v libx264 -preset ultrafast -crf 28 -c:a aac -shortest runs/demo/input.mp4
python3 scripts/media.py render examples/plano.sintetico.json --output-dir runs/demo/render
python3 scripts/media.py probe runs/demo/render/clip.mp4
```

O plano concatena os intervalos de 1–10s e 14–23s: (10 − 1) + (23 − 14) = 9 + 9 = 18s. As legendas estão na timeline final. O exemplo exporta 720×1280 para reduzir o custo do teste; o default da ferramenta é 1080×1920.

A pasta de render recebe MP4, SRT, ASS e manifesto técnico. A revisão audiovisual permanece pendente mesmo após o teste. Não usar esse vídeo como demonstração de seleção viral, qualidade de fala ou edição de uma live real. A mídia em runs/ fica fora do Git.

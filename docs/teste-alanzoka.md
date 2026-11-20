# Correção editorial: momento real do Alanzoka

Em 20/11/2026, após o usuário rejeitar o trailer, foi produzido um corte de **23s** com Alanzoka jogando, expressão/reação e um acontecimento da partida. A nova edição foi disponibilizada para avaliação. Aprovação do usuário e revisão integral com áudio permanecem pendentes.

## Origem e repercussão observada

- Publicação: https://x.com/alanzokareact/status/2123039497860321295 .
- Publicador: **Alanzoka Reactions, uma fanpage**, não a conta oficial do streamer. Participante identificado na fonte: Alanzoka.
- Publicado em 18/11/2026 às 13:03:55 UTC. Coleta registrada em 20/11/2026 às 23:23:41 UTC.
- Embed oficial do X: `favorite_count=24011`, `conversation_count=83`. São contadores da publicação, não da nossa edição.
- Views: indisponíveis. O zero do embed não foi tratado como zero real; contadores de espelhos não foram promovidos a confirmação primária.
- A identificação GTA 6 vem da publicação e do contexto consultado, sem identificação independente da build por pixels.
- A [Quenty](https://quenty.com.br/resumo/18-novembro-2026/alanzoka-curte-vibe-no-gta-6-ao-som-de-justin-bieber-bate-em-tudo-e-vira-meme-na-live-antecipada) localizou o post, mas resume comentários desse mesmo post com IA: não é confirmação independente das métricas.

Rótulo sustentado: **tração observada sem base comparável**. Não afirmar viralidade comprovada, retenção ou compartilhamentos. A seleção corrige o formato ausente no trailer e parte de um momento com repercussão observada; não garante desempenho da nova edição.

## Momento e edição

Fonte: 35,307s, H264 1080×720 a 60fps, áudio AAC estéreo 48kHz. Nos quadros inspecionados, há veículo no trânsito e expressão do streamer; manobra atravessada entre carros em 7–12s; aproximação de poste/obstrução com poeira/fumaça em 19–20,5s; retomada da rua em 21–22s. O intervalo **0–23s** conserva apresentação, acontecimento e retomada. O contraste entre curtir a rádio e dirigir mal é uma interpretação editorial, não medição da causa da repercussão.

A câmera foi ampliada acima do jogo, preservando ação e reação simultâneas. Textos brancos/amarelos de abertura e desfecho são **editoriais**, sem falsa citação ou letra de música. Há ajuste leve de luminosidade noturna e normalização do áudio original com alvo −16 LUFS/−1,5dBTP e fades breves. Alvo do filtro não é medição de loudness integrada. Não foi inserida reação de outro momento.

## Reproduzir a receita

Salvar a mídia correspondente em `media/alanzoka-gta6-radio.mp4`, após conferir origem e condições de uso:

```bash
python3 examples/render_alanzoka_radio.py media/alanzoka-gta6-radio.mp4 --output outputs/gta6-alanzoka-corte.mp4
```

Requer FFmpeg com drawtext/libx264/AAC e ffprobe. Em outro sistema, usar `--font` e `--bold-font` com fontes TTF locais. A [receita](../examples/render_alanzoka_radio.py) usa crops fixos desta fonte 1080×720. Não implementa rastreamento, download ou suporte genérico de câmera+jogo na CLI.

## Transcrição e verificação

faster-whisper small, CPU INT8, idioma solicitado `pt`, foi executado na fonte. O ASR reconheceu música em inglês, sem diálogo PT-BR confiável; não foi usado como legenda de fala. Nenhuma letra foi adicionada. Uma segunda fonte diurna também foi transcrita, com trechos de baixa confiança e alinhamentos de duração zero; não foi usada nesta edição. ASR e quadros não equivalem a escuta/reprodução integral.

| Verificação | Resultado |
| --- | --- |
| Arquivo | gta6-alanzoka-corte-v2.mp4 |
| Duração | 23,000s / 690 frames |
| Vídeo / áudio | 1080×1920, 30fps, H264/yuv420p; AAC estéreo, 48kHz |
| Tamanho | 16.759.420 bytes |
| Decodificação FFmpeg integral | Passou sem erros |
| Quadros finais | 0,5s; 8s; 19,95s; 21,5s: texto, rosto, ação e retomada visíveis |
| Revisão independente | Conferiu quadros/crops e evidências; sem bugs materiais encontrados |
| Revisão integral com áudio | Pendente; `full_watch_with_audio_done=false` |
| Avaliação do usuário | Pendente |

SHA-256 da fonte: `d8c714d9ebc9002872f9b62e09736505d70c501b3d42175d268c6c931c2703d0`.

SHA-256 do MP4 final: `df0de3c1e85b9de43ccf605a55190bd44c5648fde2215d4e0575610571b8726c`.

O arquivo foi disponibilizado na conversa. Mídia, transcrições, modelos e destinos pessoais ficam fora do Git. Não houve publicação social; condições de música/republicação por plataforma não foram presumidas pelo acesso público à postagem.

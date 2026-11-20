# Teste real: GTA 6

Pedido em 20/11/2026: produzir um corte de GTA 6 para testar e aperfeiçoar as ferramentas. Resultado: uma edição de trailer de **23,5s**, preparada para avaliação do usuário. Não é uma reação ou corte de live e não comprova desempenho viral.

## Fonte e acesso

- Autor: Rockstar Games.
- Página original consultada: https://www.rockstargames.com/VI/media/videos .
- Arquivo listado no HTML dessa página: https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Out_Now/GTAVI_Out_Now.mp4 .
- Coleta: 20/11/2026. Fonte: 29,133s, 3840×2160, 30fps, H264/AAC, SAR 1:1.
- Candidatos públicos de live foram procurados; a mídia/API do Kick retornou HTTP 403. O teste continuou com material oficial acessível, sem contornar bloqueios.
- O download público identifica a origem e o acesso; não foi tratado como comprovação de licença de republicação ou liberação da música nas três plataformas. Nenhuma publicação social foi feita.

## Decisões editoriais

O intervalo 2,7–26,2s remove a abertura escura e mantém a montagem e o encerramento com o logo nativo. Não houve seleção semântica automática nem pontuação baseada em métricas de audiência. A disponibilidade de arquivo utilizável definiu o escopo deste teste.

O enquadramento `contain_blur` preserva todo o quadro horizontal no centro de uma tela vertical, com uma cópia desfocada ao fundo. Isso evita cortar a ação nas bordas. Legendas estáticas por bloco usam alto contraste e destaques literais em amarelo. Título e detalhes em rosa são escolhas editoriais experimentais.

Os textos em português foram escritos para essa montagem: **não são transcrição, tradução nem citação das falas originais**. Não houve voz gerada, meme inserido ou efeito atribuído a um criador brasileiro. O áudio original foi mantido, com normalização e fades.

## Receita e limites da CLI

O [plano de render](../examples/plano.gta6-trailer.json) reproduz o corte, o enquadramento e os blocos de texto quando a fonte for salva em `media/gta6-out-now-source.mp4`:

```bash
python3 scripts/media.py render examples/plano.gta6-trailer.json --output-dir outputs/gta6-base
```

O arquivo entregue recebeu uma segunda passagem manual por FFmpeg, depois do render da CLI. Essa etapa acrescentou os elementos abaixo; não se deve interpretar `editing.overlays` como implementado.

| Acabamento | Parâmetros usados em 1080×1920 |
| --- | --- |
| Identificação | “EDIÇÃO DE TESTE”, 26px, centralizada em y=142 |
| Título | “GTA 6”, DejaVu Sans Bold 180px, centralizado em y=230 |
| Subtítulo | “O CAOS DE LEONIDA”, rosa, 48px, centralizado em y=435 |
| Detalhe | Linha rosa, 240×4px em y=512 |
| Crédito | “IMAGENS OFICIAIS • ROCKSTAR GAMES”, 24px em y=1310 |
| Áudio | FFmpeg loudnorm com alvo I=−16 LUFS, TP=−1,5dBTP, LRA=11; fades de 0,08s e 0,25s |
| Vídeo | Fades de 0,10s e 0,25s; H264/yuv420p, AAC estéreo, faststart |

O alvo de normalização é um parâmetro, não uma medição confirmada de LUFS integrado. Fontes instaladas e dimensões de saída precisam ser consideradas para reproduzir a composição manual em outro ambiente.

## Resultado verificado

| Campo | Observado |
| --- | --- |
| Arquivo | gta6-corte-teste.mp4 |
| Duração | 23,500s / 705 frames |
| Vídeo | 1080×1920, 30fps, H264, yuv420p |
| Áudio | AAC, 48kHz, estéreo |
| Tamanho | 15995371 bytes |
| Decodificação integral | Sem erros reportados pelo FFmpeg |
| Inspeção visual final | Quadros em 0,7s, 5,5s, 11,5s e 20,5s; texto legível na amostra |
| volumedetect | Média −18,2dB; máximo −3,1dB. Estas medidas não são LUFS nem true peak |
| Revisão integral com áudio | Pendente; `full_watch_with_audio_done=false` |

SHA-256 do MP4 final: `51bcff34519ab84ce6e93bc32323c07186f5533afe34093861060c2e7487afb8`.

O arquivo de vídeo foi disponibilizado para avaliação na conversa; mídia, modelos e destinos pessoais de entrega ficam fora do repositório público. O plano de exemplo conserva um estado de entrega próprio e não serve como recibo do arquivo final.

## Melhorias incorporadas e o que falta

1. Layout `contain_blur` para preservar informação horizontal em saída vertical; `cover` permanece o padrão.
2. `--language pt|en|auto` na transcrição; português continua como default.
3. Dependência opcional PyAV 16.1.0: com faster-whisper 1.2.1, PyAV 19.0.2 falhou em `av.open(metadata_errors=...)`. A combinação corrigida decodificou áudio real e executou VAD.
4. Testes de regressão do layout, do encaminhamento de idioma e da preservação de proporção visual em fontes com pixels não quadrados. A revisão corrigiu a distorção causada por alterar SAR para 1:1 sem normalizar os pixels; o MP4 de GTA 6 já tinha SAR 1:1 e não foi afetado.
5. A suite completa passou com 32 testes. Inferência ASR não foi executada: VAD detecta possíveis trechos de voz e pode responder a música; não fornece palavras nem comprova idioma.

Ainda falta validar uma live com fala, transcrição real PT-BR, referências assistidas com áudio e revisão integral do arquivo exportado. Este teste não valida retenção, viralidade, aprovação da edição pelo usuário, execução no Claude ou publicação nas plataformas.

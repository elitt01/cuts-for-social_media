# Ferramentas locais de mídia

Esta CLI faz inspeção, transcrição opcional e render técnico. A escolha do momento, a pesquisa de tendências, a edição semântica e a revisão audiovisual continuam sendo trabalho do agente. Render concluído não significa vídeo revisado ou entregue.

Executar os comandos a partir da raiz do repositório. A base usa Python 3.11+ e biblioteca padrão; `ffmpeg` e `ffprobe` precisam estar no PATH. Os comandos recebem argumentos como lista, sem shell. Não baixam lives, não importam cookies e não publicam vídeos.

## Conferir o ambiente

```bash
python3 scripts/media.py preflight
python3 scripts/media.py probe /caminho/fonte.mp4
python3 scripts/media.py probe /caminho/fonte.mp4 --output /caminho/probe.json
```

`preflight` informa caminhos, versões, filtros, encoders, espaço livre e presença de faster-whisper. Não instala dependências nem baixa modelos. Para render são necessários libx264/AAC e, com legendas, filtro subtitles/libass. Um erro informa o componente ausente; não tentar usar o pacote Python chamado ffmpeg como substituto dos binários.

## Preencher o plano

O formato segue `templates/plano.example.json`. O template vazio não pode ser renderizado. Os demais objetos editoriais do plano são preservados pelo agente; esta CLI consome os campos abaixo.

```json
{
  "schema_version": "0.1.0",
  "run_id": "exemplo-local",
  "duration_target_seconds": {"min": 15, "max": 30},
  "editing": {
    "source_files": [{"id": "live", "path": "/caminho/fonte.mp4"}],
    "segments": [
      {"source_id": "live", "source_in_seconds": 10, "source_out_seconds": 20},
      {"source_id": "live", "source_in_seconds": 30, "source_out_seconds": 38}
    ],
    "captions_output_timeline": [
      {"start_seconds": 0.2, "end_seconds": 2.5, "text": "Olha o que aconteceu!", "highlight_word": "aconteceu"},
      {"start_seconds": 10.2, "end_seconds": 12.5, "text": "Agora vem a reação.\nSem perder o contexto."}
    ],
    "crops": [],
    "overlays": [],
    "audio_assets": [],
    "output": {"width": 1080, "height": 1920, "fps": 30, "video_codec": "h264", "audio_codec": "aac", "pixel_format": "yuv420p"}
  }
}
```

| Campo | Contrato |
| --- | --- |
| source_files | Lista de `{id, path}`; IDs únicos. Arquivos locais existentes, caminhos relativos à pasta do plano ou absolutos. Não aceita URLs. |
| segments | Ordem final de concatenação. Cada item usa `source_id`, `source_in_seconds`, `source_out_seconds`. Aceita aliases `source_in` e `source_out`. Início/fim são da fonte, em segundos. |
| output_in_seconds | Opcional em cada segmento; se fornecido, deve coincidir com a soma das durações anteriores. O alias legado `output_in` também é validado; se ambos forem fornecidos, ambos precisam corresponder. Sem lacunas, repetições implícitas ou velocidades diferentes de 1. |
| duration_target_seconds | Faixa explícita validada sobre a soma dos segmentos. Template padrão: 15–30 s. Um pedido diferente pode fornecer outra faixa. Se omitida, a CLI não aplica uma duração editorial automaticamente. |
| captions_output_timeline | Lista ordenada de `{start_seconds,end_seconds,text,highlight_word?}`. Tempos na saída final, sem sobreposição e sem ultrapassar sua duração. Não fornecer tempos brutos da live. |
| highlight_word | Trecho literal do texto; destaca em amarelo sua primeira ocorrência durante a legenda inteira. Não é animação por palavra nem alinhamento automático. |
| crops | Opcional: `{segment_index,x,y,width,height,units:"pixels"}`. Índice começa em zero. Pode usar `crop` dentro do próprio segmento; nesse caso ele tem prioridade. |
| output | Dimensões pares de 16 a 4096 px; fps de 1 a 120. Defaults: 1080×1920, 30 fps. `fps:null` usa 30. Só H264/AAC/yuv420p nesta V1. |
| output.fit_mode | `cover` (default): preenche e recorta ao centro. `contain_blur`: mantém o quadro inteiro centralizado, com fundo preenchido do mesmo vídeo, desfocado e levemente escurecido; legendas vêm por cima. Valores diferentes são rejeitados. |
| overlays / audio_assets | Precisam estar vazios nesta V1. Elementos não suportados geram erro; não são ignorados silenciosamente. |

O exemplo concatena 10 s com 8 s e totaliza 18 s. Portanto, fonte de 30–38 s aparece na saída de 10–18 s. O manifesto gera `time_mapping` a partir dos segmentos; legendas devem ser alinhadas a esse resultado antes do render. `editing.time_mapping` preenchido por outro sistema não substitui a sequência de segmentos.

Para cortes fracionários, cada duração de saída é arredondada para o frame mais próximo no fps escolhido, com mínimo de um frame. O manifesto registra `output_frames`, `output_duration_seconds` e os limites reais de concatenação; o áudio é preenchido/aparado ao mesmo intervalo. Isso evita acumular diferenças de frames entre cortes. Exemplo: 0,66 s a 10 fps resulta em 7 frames, ou 0,7 s. Use esse mapeamento ao alinhar as legendas; para preservar limites exatos, escolha os cortes em múltiplos de 1/fps.

O crop é geométrico: aplica a área solicitada, escala para cobrir a tela e faz crop central no aspecto final. Não encontra rosto, falante, bola ou ação de jogo. Inspecionar os frames para escolher uma área adequada; divisão rosto/jogo e movimento de câmera exigem implementação adicional. A ausência de stream de áudio gera silêncio naquele segmento e exige revisão.

Para trailers e outros quadros em que as bordas contêm informação, usar `"fit_mode":"contain_blur"` em `editing.output`. O crop explícito, se houver, é aplicado antes dos dois layouts; `contain_blur` preserva a área resultante. O foreground mantém seu aspecto e fica centralizado; o fundo utiliza uma cópia do próprio vídeo com blur e escurecimento de 0,10. `cover` conserva o comportamento anterior. Nenhum dos modos reconhece automaticamente pessoas ou objetos.

As coordenadas de crop usam pixels da fonte. Depois do crop, fontes com pixels não quadrados têm o SAR normalizado antes do layout, preservando a proporção visual em vez de apenas trocar o metadado para 1:1. A regressão inclui entrada 160×90 com SAR 2:1 (proporção visual 32:9).

Os streams selecionados usam os índices reais do ffprobe, ignorando capas `attached_pic` na escolha de vídeo. Áudio e vídeo são ancorados no mesmo início de segmento; offsets de áudio presentes na fonte são preservados com preenchimento de silêncio pelos timestamps, em vez de adiantar a primeira fala ao zerar o primeiro pacote. A verificação sintética inclui vídeo de 2 s com áudio começando em 1 s.

## Renderizar

```bash
python3 scripts/media.py render /caminho/plano.json --output-dir /caminho/saida
```

Para substituir outputs existentes de propósito, adicionar `--overwrite`. Sem essa opção, a CLI preserva a saída anterior. Fontes com espaços e caracteres de shell não são executadas como comandos.

A pasta recebe:

- `clip.mp4`: H264/AAC, yuv420p e faststart; legendas queimadas quando fornecidas.
- `clip.srt`: texto simples na timeline final.
- `clip.ass`: fonte clara com contorno escuro e destaque opcional. A fonte deve existir no sistema; conferir aparência e quebras no render.
- `render-manifest.json`: duração esperada/observada, streams, mapeamento dos cortes, hashes SHA-256 e caminhos.

O estado técnico é `technically_verified/audiovisual_pending`; `delivery.status` permanece `not_delivered`. A verificação técnica atual confere a duração por ffprobe; diferenças de até o maior entre 0,2 s e dois frames são toleradas. Metadados e checksums ficam disponíveis para a revisão seguinte.

Não há trilha, normalização de volume, remoção semântica de pausas, memes, efeitos narrativos automáticos, rastreamento ou exportação automática por plataforma. As legendas são estáticas por bloco, com destaque literal; o SRT permanece sem estilo. Não interpretar esses defaults como uma receita comprovada de viralidade ou garantia de aceitação por qualquer plataforma.

## Transcrever em PT-BR, opcional

```bash
python3 -m pip install -r requirements-optional.txt
python3 scripts/media.py transcribe /caminho/fonte.mp4 --output /caminho/transcricao.json --model-dir /caminho/modelo-ctranslate2 --language pt
```

A instalação é uma ação separada; `preflight`, `probe` e `render` não a fazem. O modelo local precisa estar no formato compatível com faster-whisper/CTranslate2. Para autorizar explicitamente o download de um modelo pelo faster-whisper:

```bash
python3 scripts/media.py transcribe /caminho/fonte.mp4 --output /caminho/transcricao.json --model small --allow-model-download --language auto
```

Sem modelo local ou autorização explícita, não há download automático. A execução usa CPU INT8, timestamps de palavras e VAD para transcrição. `--language pt|en|auto` usa português por default, aceita inglês e passa idioma não fixado ao motor em `auto`. O JSON registra idioma pedido e detectado. Não apaga pausas da mídia. O JSON aponta `time_reference:input_file`: os timestamps são relativos ao arquivo fornecido. Se esse arquivo já é um trecho, o agente precisa registrar seu offset na live e remapear para a edição final. Revisar nomes, gírias e sincronismo; transcrição não vem aprovada.

Compatibilidade verificada em áudio real: faster-whisper 1.2.1 com PyAV 16.1.0 decodificou WAV e executou o VAD incluído. A combinação com PyAV 19.0.2 falhou em `av.open(metadata_errors=...)`; por isso a dependência opcional fixa `av==16.1.0`. Essa verificação não comprova transcrição ASR: não foi baixado um modelo de reconhecimento nem inventada uma transcrição a partir da detecção de atividade vocal.

A existência do arquivo de saída é conferida antes de importar o motor, baixar modelo ou iniciar inferência. Escolher outro caminho se já existir; a transcrição não substitui arquivos anteriores.

Nenhum modelo ASR foi baixado para validar este toolkit. A inferência de reconhecimento com faster-whisper não foi executada nesta rodada; foram testados a mensagem de erro quando a dependência não existe e o encaminhamento dos idiomas com mock. O VAD incluído no pacote foi executado sobre áudio real, separadamente. Instalação e desempenho dependem do sistema e do modelo.

## Testes executáveis

```bash
python3 -m unittest discover -s tests -p test_media.py -v
```

Os testes criam mídia sintética local com lavfi. Exercitam corte de duas regiões em ordem trocada, cores dos frames de saída, concatenação, duração, exportação vertical H264/AAC/yuv420p, legibilidade estrutural ASS/SRT, faixas explícitas, erros de timeline, preservação da saída anterior e ausência da dependência opcional. Não baixam mídia nem modelos. Passar nesses testes não substitui a revisão audiovisual de um corte real.

## Documentação primária consultada em 20/11/2026

- [FFprobe](https://ffmpeg.org/ffprobe.html): metadados de streams e JSON.
- [FFmpeg CLI](https://ffmpeg.org/ffmpeg.html): arquivos de entrada, render e parâmetros.
- [FFmpeg filtros](https://ffmpeg.org/ffmpeg-filters.html): trim/atrim, concat, scale/crop e subtitles/libass.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): CPU INT8, VAD e timestamps por palavra.

Guardar fontes, modelos, transcrições privadas e vídeos fora do Git. O manifesto técnico não substitui a persistência do vídeo e sua entrega com link verificado ao usuário.

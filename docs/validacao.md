# Validação desta versão

Executada em 20/11/2026, em executor Linux com Python 3.12.14 e FFmpeg/ffprobe 7.1.5. Os resultados comprovam o comportamento técnico descrito; não comprovam alcance viral, execução no PC do usuário ou integração funcional com uma sessão do Claude.

## Verificações executadas

- `python3 -m unittest discover -s tests -v`: **32 testes aprovados**, sendo 16 de mídia e 16 de seleção.
- Exemplo de candidatos fictícios: selecionado `a-completo-75`; incompletos e registros bloqueados não venceram pelo limite superior ou por nota isolada.
- Exemplo de render: dois intervalos de 9s produziram 18,0s, com quatro blocos de legenda.
- Probe do exemplo: vídeo H264, 720×1280, 30fps, yuv420p e áudio AAC.
- Um quadro do exemplo foi inspecionado visualmente: duas linhas, acentos/ç, contorno e destaque legíveis. O vídeo completo com áudio não foi revisado por essa inspeção de quadro.
- JSONs, links locais, manifesto do pacote e estrutura da skill conferidos. Mídia de teste e modelos ficam fora do Git.
- [Teste real GTA 6](teste-gta6.md): 23,5s, 1080×1920, 30fps, H264/AAC; decodificação completa sem erro e quatro quadros finais inspecionados. Textos editoriais, sem transcrição de fala nem revisão integral com áudio.
- faster-whisper 1.2.1 e PyAV 16.1.0: decodificação de áudio real e VAD executados. PyAV 19.0.2 falhou com `metadata_errors`; a dependência compatível foi fixada. Nenhum modelo de ASR foi baixado.

## Casos cobertos pelos testes

Mídia: múltiplos cortes e ordem de cenas; exportação vertical; preservação das bordas após crop com `contain_blur`; proporção visual de fonte com pixels não quadrados (SAR 2:1); rejeição de modo de enquadramento inválido; encaminhamento de idioma pt/en/auto sem rede; duração padrão de 15s; limites explícitos; quantização de trechos fracionários por frames; legenda na timeline final; escape de texto ASS; atraso real de áudio preservado com silêncio inicial; seleção do stream correto quando há capa; aliases validados; rejeição de edições não suportadas; preservação das fontes e das saídas existentes; falha clara da dependência opcional.

Seleção: soma ponderada; campos desconhecidos; intervalos sem renormalização; evidência obrigatória; entradas inválidas; contexto e fonte declarados; empate determinístico; métricas observadas separadas da nota; JSON inválido ou com campos duplicados.

## Limites da evidência

- O avaliador valida a estrutura declarada pelo agente, não a veracidade de uma inspeção.
- faster-whisper foi instalado em ambiente isolado no teste real. Decodificação e VAD não equivalem a reconhecimento de fala; não houve inferência ASR nem avaliação de precisão de legendas faladas.
- O render não implementa rastreamento de rosto, composição câmera+jogo, inserção automática de memes, trilha ou efeitos. Esses elementos exigem ferramentas adicionais; campos não suportados geram erro.
- A [pesquisa brasileira](referencias-observadas.md) observou quadros públicos de quatro publicações. Não houve áudio nem reprodução integral; as técnicas derivadas são hipóteses editoriais.
- O manifesto técnico conserva revisão audiovisual pendente e entrega não concluída. Um agente deve verificar o corte real e sua entrega antes de mudar esses estados.

Os comandos e os exemplos reproduzíveis estão nos guias de [mídia](ferramentas-cli.md), [seleção](selecao-cli.md) e [exemplos](../examples/README.md).

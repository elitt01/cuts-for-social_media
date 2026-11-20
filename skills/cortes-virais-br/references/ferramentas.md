# Arquitetura proposta — cortes de lives
Consulta: 20/11/2026. O repositório contém instruções, avaliação de candidatos e ferramentas básicas de mídia testadas com material sintético. Isso não comprova um plugin instalado, execução no Claude ou qualidade editorial de um corte real.

## Decisão recomendada
Começar com instruções compartilhadas e planejar ferramentas para Work e PC: Python coordenará arquivos JSON, FFmpeg fará corte/render e faster-whisper fará transcrição. Preparar uso pelo Claude quando solicitado com o link do repo, mantendo os mesmos contratos e verificando o ambiente real da sessão. Navegação/pesquisa do agente gera evidências de tendências. Adicionar yt-dlp apenas para fontes que permitem ingestão; Remotion apenas quando legendas e composições animadas justificarem a manutenção.

Não criar um servidor MCP para o V1 sem necessidade concreta: uma skill orienta o agente, mas não fornece, por si, acesso a vídeos, APIs, GPU ou armazenamento. Contratos de arquivo permitem migrar para MCP depois.

## Ferramentas e limites confirmados

| Etapa | Ferramenta | Capacidade confirmada | Limite prático / decisão proposta |
| --- | --- | --- | --- |
| Inspeção | ffprobe | Emite metadados de contêiner e streams em formatos de máquina, inclusive JSON. | Checar duração, streams, resolução, fps e saída; metadados corretos não substituem assistir. |
| Corte e exportação | FFmpeg | Documenta filtros de crop, escala, mixagem, loudnorm e subtitles. Render de subtitles depende da compilação com libass. | Verificar filtros e codecs instalados. Reencodar cortes precisos; não assumir precisão de corte copiando streams. |
| Ingestão opcional | yt-dlp | Documenta seleção de intervalo por --download-sections com FFmpeg; suporta muitas fontes com extratores. A documentação consultada pede Python 3.11+ e recomenda FFmpeg, ffprobe, yt-dlp-ejs e runtime JS para YouTube. | Disponibilidade técnica não significa autorização de uso. Login, bloqueios, formato e extratores mudam. Não prometer que toda URL funciona nem importar cookies automaticamente. |
| Transcrição | faster-whisper | Oferece CPU INT8, timestamps por palavra e VAD. Decodifica via PyAV e aceita Python 3.9+. Execução CUDA depende de bibliotecas NVIDIA compatíveis. | Basear dependências do projeto em Python 3.11+ pelo yt-dlp. Testar modelo multilíngue em PT; transcrição e timestamps exigem revisão. VAD para transcrição não autoriza apagar pausas dramáticas. |
| Animação opcional | Remotion + @remotion/captions | Agrupa tokens em páginas e permite destacar palavra ativa; recebe timestamps em ms. | Tokens exigem espaços corretos. Render em React adiciona Node/browser e dependências. Não é necessário para uma primeira entrega com ASS. |
| Pesquisa | Navegação e fontes oficiais | Pode buscar tendências públicas e guardar URLs/janelas de coleta. | Não equivale a feed completo, busca universal de lives nem acesso a dados privados de retenção. Tratar ausência como desconhecida. |

Fontes primárias verificadas:
- FFprobe: https://ffmpeg.org/ffprobe.html
- FFmpeg CLI (seek e saída): https://www.ffmpeg.org/ffmpeg.html
- Filtros: https://ffmpeg.org/ffmpeg-filters.html
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- Runtime JS / EJS: https://github.com/yt-dlp/yt-dlp/wiki/EJS
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- Remotion captions: https://www.remotion.dev/docs/captions/create-tiktok-style-captions
- Remotion Caption: https://www.remotion.dev/docs/captions/caption
- Licença: https://www.remotion.dev/docs/license/pricing e https://www.remotion.dev/docs/license/faq

## Execução Work, local e uso pelo Claude

Decisão confirmada: Work e computador local. Claude é outro agente que pode usar as instruções quando o usuário pedir com o link do repo; não constitui por si só um terceiro serviço de render. Consultar docs/execucao.md a partir da raiz do projeto.

| Ambiente | Uso adequado | Limitação |
| --- | --- | --- |
| Work com executor | Pesquisa, inspeção de arquivos anexados, scripts, transcrição/render quando dependências e recursos existem. | GPU, duração máxima de processos, espaço, downloads e rede não são garantidos. Fazer preflight por sessão. |
| PC do usuário | Arquivos grandes locais, modelos em cache e renders demorados. | Requer Python/FFmpeg e instalação controlada; não presumir acesso do agente ao PC. |
| Sessão do Claude | Ler o projeto e seguir a mesma receita; executar etapas se a sessão oferecer as ferramentas necessárias. | Acesso ao repo, terminal, arquivos, pesquisa e mídia devem ser conferidos; receber um link não instala dependências nem comprova render funcional. |
| API paga / servidor | Futuro uso contínuo, escala ou integração externa. | Só acrescentar depois de definir demanda e orçamento. Não contratar ou criar infraestrutura só para guardar instruções. |

Fato observado neste executor em 20/11/2026: Python 3.12.14, ffmpeg e ffprobe em /usr/bin, Node e npm disponíveis; yt-dlp não está no PATH. Não foi feita instalação nem teste de transcrição/render. Não afirmar desempenho no computador de destino a partir de benchmarks de outro hardware.

Custo: FFmpeg/yt-dlp/faster-whisper não exigem uma API de transcrição paga para o fluxo local proposto; computação, armazenamento e tráfego continuam existindo. Remotion permite uso grátis para indivíduos e empresas de até três pessoas segundo a licença consultada; conferir elegibilidade antes de uso organizacional. Não congelar preços no código; guardar URL e data da consulta.

## Organização atual e implementação planejada

Caminhos abaixo são relativos à raiz do repositório. Um componente planejado ainda não existe nem pode ser executado.

| Caminho | Estado | Responsabilidade |
| --- | --- | --- |
| README.md | Atual | Escopo, estado, navegação e limites |
| AGENTS.md | Atual | Regras de trabalho e fidelidade das evidências |
| CLAUDE.md e docs/execucao.md | Atual | Entrada do Claude e roteiro compartilhado para cada ambiente |
| docs/briefing.md e config/project.json | Atual | Respostas e política de vários nichos |
| docs/roadmap.md | Atual | Pendências e critérios da primeira entrega funcional |
| skills/cortes-virais-br/SKILL.md | Atual | Orquestração da tarefa |
| skills/cortes-virais-br/references/selecao.md | Atual | Descoberta e critérios de potencial |
| skills/cortes-virais-br/references/edicao-br.md | Atual | Estilo, presets e revisão audiovisual |
| skills/cortes-virais-br/references/ferramentas.md | Atual | Esta proposta de ferramentas, fluxo e QA |
| config/brief.example.json e templates/ | Atual | Modelos em branco para briefing, referência e plano |
| .gitignore | Atual | Exclusão de mídia, modelos e dados privados |
| START_HERE.md | Atual | Entrada operacional e padrões já decididos |
| scripts/media.py | Atual | Subcomandos preflight, probe, transcribe opcional e render |
| scripts/score_candidates.py | Atual | Pontuação, intervalos de evidência e escolha entre candidatos elegíveis |
| docs/ferramentas-cli.md e docs/selecao-cli.md | Atual | Comandos e contratos exatos das CLIs |
| docs/referencias-observadas.md | Atual | Observações visuais de quatro publicações, com áudio pendente |
| examples/ e tests/ | Atual | Contratos fictícios e testes com mídia/dados sintéticos |
| schemas/ | Planejado | Formalizar e validar contratos de dados |
| .github/workflows/validate.yml | Planejado | Executar validação estrutural no CI |

Não versionar MP4s de lives, chaves, cookies, modelos ou transcrições pessoais. Os arquivos finais pertencem ao armazenamento de entrega do usuário, fora do Git. Manter só referências permitidas e metadados mínimos.

## Fluxo e condições de passagem

1. **Brief.** Capturar o tema da tarefa, público, plataformas-alvo, fonte própria/autorizada ou de terceiros, quantidade, duração, estilo e orçamento. Respeitar a política de vários nichos: seguir o pedido ou descobrir oportunidades quando aberto. Continuar pesquisa independente enquanto faltam preferências; não fabricar uma identidade editorial.
2. **Radar.** Registrar consulta, região BR, janela temporal, hora da coleta e fontes. Guardar também ausência de dados. Separar novidade, velocidade observada e adequação ao público.
3. **Busca.** Registrar candidatos com URL original, criador, timestamps, fala relevante, motivo, confiança e estado de acesso. Comparar internamente e avançar para o melhor trecho sem exigir escolha do usuário; apresentar opções antes da edição somente quando isso for pedido. Comparar sinais dentro de contexto semelhante, sem tratar views totais como chance futura.
4. **Inspeção.** Assistir/ouvir candidato, incluindo margem antes/depois. Só carimbar visto quando mídia foi realmente inspecionada. Transcrição sozinha não prova enquadramento, ironia, contexto ou reação.
5. **Seleção.** Escolher arco completo: promessa, contexto mínimo, momento e resolução. Rejeitar título que contradiz a fala; registrar o que foi preservado.
6. **Ingestão.** Priorizar arquivo original oferecido pelo usuário ou download autorizado. Se URL falhar, registrar erro e usar arquivo fornecido, sem contornar controles de acesso.
7. **Transcrição e alinhamento.** Usar PT explicitamente no caso adequado, revisar nomes/gírias e ajustar intervalos. Conservar transcrição bruta e revisão para auditoria.
8. **Plano de edição.** Definir sequência, crop por trecho, títulos, legendas, áudio e origem/licença dos assets. Separar storyboard proposto de render produzido.
9. **Render.** Gerar MP4 e SRT coerentes com a timeline final. ASS é arquivo intermediário para legendas estilizadas; SRT simples permite reaproveitamento. Evitar render repetido quando nada mudou.
10. **QA.** Validar arquivos automaticamente, depois assistir integralmente e verificar legibilidade no celular, áudio e fidelidade contextual.
11. **Entrega sob pedido.** Fornecer arquivo/link do vídeo final e, se útil, SRT, título sugerido e crédito. Não publicar, agendar ou enviar a terceiros sem ordem explícita.

## Contratos atuais e extensões propostas

Os modelos de configuração e tarefa incluem schema_version. run_id identifica uma execução real: no modelo de plano permanece null até iniciar o trabalho; configurações permanentes e fichas de referência reutilizáveis não exigem run_id. Timestamps numéricos usam segundos, salvo campos terminados em _ms. Datas de observação usam ISO 8601 com timezone. Nunca misturar timeline da fonte, trecho bruto e saída editada. As CLIs validam seus campos operacionais; JSON Schemas completos ainda não foram implementados. Os contratos exatos estão nos guias de CLI, que prevalecem sobre sugestões de extensões futuras.

### config/brief.example.json — modelo atual
- audience: locale, region, age_band (pode ser null), interests.
- niche_policy e requested_topic: política adaptativa e tema daquela tarefa.
- target_platforms, source_policy, approved_creators, reference_urls.
- duration_target_seconds: min/max; count; style_preset.
- delivery: mp4/srt, destination, publish=false.
- budget: paid_services_allowed=false até outra indicação.
- unknowns e assumptions como listas separadas.

### candidates.json — contrato atual do avaliador
- Lista ou objeto com candidates; candidate_id textual único.
- source_url ou source_file; source_start_seconds e source_end_seconds.
- context_reviewed: start_seconds, end_seconds e mode: audiovisual/transcript_only/unavailable.
- potential.criteria: sete chaves com {score,evidence,timecode_seconds} ou null.
- observed_performance.snapshots: métricas realmente observadas e observed_at com fuso.
- Metadados extras de criador, tendências, acesso e uso podem acompanhar a ficha; o avaliador não prova que essas declarações são verdadeiras.
- Consultar docs/selecao-cli.md para elegibilidade, desempate e resposta research_required.

### transcript.json — saída atual da transcrição opcional
- source_file, language, engine, model e review_status: pending.
- time_reference: input_file; source_offset_seconds: 0 para o arquivo fornecido.
- segments: start_seconds/end_seconds/text; words inclui tempos/text/probability.
- O agente deve registrar o offset da live quando transcrever um recorte e remapear para a montagem final; a CLI não faz essa revisão nem o alinhamento de cortes automaticamente.
- A inferência real depende de faster-whisper e de um modelo disponível; ainda não foi executada nesta validação.

### templates/plano.example.json — modelo atual de plano e execução
- candidate: fonte, timecodes, contexto revisto, evidências, potencial e desempenho observado.
- narrative: hook, context, development e payoff.
- editing.output: width/height/fps/video_codec/audio_codec/pixel_format.
- duration_target_seconds: faixa por pedido; default de min=15/max=30 segundos.
- editing.source_files: objetos id/path; caminhos locais relativos ao plano ou absolutos.
- editing.segments: source_id, source_in_seconds/source_out_seconds e output_in_seconds opcional; sequência concatenada sem lacunas. Consultar os aliases aceitos no guia de mídia.
- editing.crops: segmento e retângulo normalizado ou pixels declarados.
- editing.captions_output_timeline: start_seconds/end_seconds/text e highlight_word opcional; tempos da saída, em ordem e sem sobreposição nesta V1.
- editing.overlays e editing.audio_assets: vazios na CLI atual; elementos adicionais exigem ferramentas externas e não podem ser ignorados.
- O manifesto do render calcula time_mapping e registra a quantização por frames. editing.time_mapping pré-preenchido não substitui os segmentos. Velocidades diferentes de 1 não são suportadas.
- qa: technical_checks, full_watch_with_audio_done, context_fidelity, captions_reviewed, mobile_readability e blockers. Usar pass/fail/not_checked nos resultados dos checks; não afirmar revisão integral a partir de metadados.
- delivery: requested, status, artifact_paths e checksums. Usar not_prepared/prepared/delivered; só marcar delivered após verificar entrega.

### templates/referencia.example.json — modelo atual de referência
- Identificar URL, criador, plataforma, nicho, datas e métricas realmente disponíveis.
- Registrar full_video_watched_with_audio, observações temporais e parâmetros estimados separadamente.
- Distinguir hypotheses, unavailable_information e techniques_to_reproduce.

## Defaults propostos para testar, sem alegar regra das plataformas
MP4 H.264 + AAC, yuv420p, 1080×1920, 30 fps ou frequência apropriada à fonte, faststart. Estes são defaults de interoperabilidade propostos; não substituem requisitos atuais de upload do destino. Conservar um master antes de marca d'água e exportar variantes quando houver diferenças reais de interface.

Usar ASS para borda e destaque e gerar SRT legível à parte. Se desejar karaokê por palavra, comparar legibilidade entre ASS e Remotion antes de escolher. Não criar zoom contínuo nem trilha automática por default.

## Verificação proporcional

Executar `python3 -m unittest discover -s tests -v` para a suíte atual. Ela usa material sintético, sem baixar lives ou modelos. Testes de inferência real e revisão audiovisual de cortes reais permanecem separados.

Testes úteis:
- Schema rejeita fim antes do início, duração negativa, NaN, fonte inexistente e caminhos fora da pasta de trabalho.
- Transformação de timestamps preserva sincronismo após duas remoções e mudança de velocidade; compara resultado esperado em fixture sintética.
- Legendas não ultrapassam a duração final e referências a fontes/assets existem.
- Vídeo sintético com marcador visual e sinal sonoro exercita corte e exportação; ffprobe mede resolução/duração/streams.
- QA registra not_checked quando não foi possível assistir/ouvir.
- Nome de arquivo malicioso nunca vira comando shell; scripts passam argumentos como lista, não shell=True.

Revisão humana/agente multimodal:
- Assistir começo, final e vídeo completo; conferir que o gancho é entregue.
- Não cobrir rosto, placar, item de jogo, texto essencial ou elementos de interface do destino.
- Reouvir nomes, ironia, sobreposição de falas e palavras corrigidas.
- Verificar que texto e memes não fazem parecer que alguém disse o oposto.
- Atribuição e assets correspondem à origem registrada.

## V1 sugerido
A. Fechar brief e 3–5 referências reais do nicho.
B. Fazer radar documentado e 3 candidatos, sem prometer viralidade.
C. Produzir um corte a partir de arquivo próprio/autorizado, com preset limpo e legendas revisadas.
D. Comparar resultado com referências, ajustar parâmetros e documentar uma receita reproduzível.
E. Só então automatizar repetição, busca em fontes adicionais e plugin empacotado.

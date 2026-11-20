# Cuts for Social Media

Projeto: **Cortes Virais BR**. Repositório: [elitt01/cuts-for-social_media](https://github.com/elitt01/cuts-for-social_media). Entrada para agentes: [START_HERE.md](START_HERE.md).

Base de instruções e pesquisa para um agente descobrir momentos reais de criadores e lives, verificar tração já observada, editar cortes em português brasileiro e entregar o vídeo quando solicitado.

Conteúdo padrão: **criador, streamer ou famoso diante de um acontecimento engraçado, estranho ou inesperado, com reação e contexto**. Em games, isso significa a pessoa efetivamente jogando. Preferir momentos cuja viralidade já tenha evidência registrada com URL, datas e contexto; fama ou tema em alta não comprovam que um clipe viralizou. Sem um limiar universal inventado de views.

Trailer, compilação publicitária e reação a trailer só substituem gameplay quando o usuário escolhe explicitamente esse formato. Em bloqueio de acesso, manter tema e formato e procurar outro candidato válido, ou expor a limitação concreta.

Destinos confirmados: **TikTok, Instagram Reels e YouTube Shorts**. Preparar um master e ajustar variantes quando necessário para interfaces, legendas e requisitos atuais de cada plataforma.

Fontes confirmadas: **busca livre + seus links e arquivos**. O agente pode descobrir candidatos sem lista fixa de criadores e deve priorizar o material que você indicar para editar.

Fluxo confirmado: **escolher o melhor trecho → editar → revisar → entregar pronto**. A seleção entre candidatos é feita pelo agente, sem exigir uma aprovação antes de editar, salvo pedido diferente naquela tarefa.

Edição confirmada: **adaptar ao clipe, usando memes e efeitos quando ajudarem**. O agente pesquisa referências por conta própria e também pode usar exemplos enviados pelo usuário; a intensidade deve preservar fala, contexto e desfecho.

Duração padrão: **15–30 segundos**. Outro pedido explícito prevalece. Como padrões reversíveis, adotar um corte por pedido, identidade neutra e entrega na sessão atual ou pasta local.

Uso previsto: **ChatGPT Work e computador local**. Para usar no **Claude**, envie o link do repositório junto com o pedido e siga o [guia de execução](docs/execucao.md). As instruções são compartilhadas; a execução depende das ferramentas e do acesso disponíveis em cada sessão.

**Estado: versão 0.3.1, com ferramentas básicas e primeiro corte de momento real de criador.** Os 32 testes automatizados da base passaram. O [trailer de GTA 6](docs/teste-gta6.md) foi rejeitado editorialmente pelo usuário. A correção produziu um [corte de 23s do Alanzoka](docs/teste-alanzoka.md), com câmera acima da gameplay e tração observada na publicação. ASR small foi executado em duas fontes; os textos do corte são editoriais, pois o áudio desse trecho é predominantemente musical. A precisão de transcrição PT-BR, a revisão integral com áudio e a aprovação da nova edição pelo usuário ainda não foram validadas.

O pacote está organizado para uso a partir do repositório. Não houve instalação de plugin nem execução de uma sessão do Claude. O novo arquivo tem verificação técnica e inspeção de quadros; a revisão integral com áudio permanece pendente. Curtidas observadas não comprovam, sozinhas, viralidade ou desempenho da edição resultante.

## Começar

```bash
git clone https://github.com/elitt01/cuts-for-social_media.git
cd cuts-for-social_media
python3 scripts/media.py preflight
python3 scripts/score_candidates.py examples/candidatos.sinteticos.json
python3 -m unittest discover -s tests -v
```

Usar `python` se esse for o comando disponível no sistema. O exemplo de seleção é explicitamente fictício e serve para conferir a lógica. A base usa biblioteca padrão Python; o render requer FFmpeg/ffprobe com libx264, AAC e subtitles/libass para legendas. Ver os [comandos de mídia](docs/ferramentas-cli.md) e o [avaliador de candidatos](docs/selecao-cli.md).

## Resultado pretendido

1. Identificar o pedido e escolher o nicho daquela tarefa: seguir o tema solicitado ou pesquisar oportunidades em vários nichos quando o pedido for aberto.
2. Localizar momentos reais do tema, preferindo viralidade já observada e registrando URL, publicação/coleta, métricas disponíveis e contexto; usar tendências como apoio à busca.
3. Encontrar candidatos adequados ao formato e assistir ao contexto da live original; em games, conferir pessoa jogando, reação e acontecimento.
4. Comparar gancho, compreensão, desfecho, atualidade e qualidade audiovisual.
5. Criar um plano com timestamps, enquadramento, legendas PT-BR, áudio e efeitos com função.
6. Renderizar, revisar e entregar MP4 e legenda revisada quando pedidos.

A nota de potencial é uma heurística editorial, nunca uma probabilidade de viralização. Views observadas, interesse de busca e retenção são sinais diferentes. Dados indisponíveis permanecem desconhecidos.

## Onde encontrar

| Arquivo | Uso |
| --- | --- |
| [START_HERE.md](START_HERE.md) | Como iniciar e executar um pedido de corte |
| [AGENTS.md](AGENTS.md) | Regras para trabalhar neste projeto |
| [CLAUDE.md](CLAUDE.md) | Ponto de entrada para o Claude, ligado às instruções compartilhadas |
| [Guia de execução](docs/execucao.md) | Como iniciar no Work, no computador ou no Claude |
| [Skill principal](skills/cortes-virais-br/SKILL.md) | Ordem de execução para o agente |
| [Descoberta e seleção](skills/cortes-virais-br/references/selecao.md) | Pesquisa de tendências, critérios e comparação de desempenho |
| [Edição para o Brasil](skills/cortes-virais-br/references/edicao-br.md) | Legendas, ritmo, composição, áudio, presets e estudo de referências |
| [Referências observadas](docs/referencias-observadas.md) | Amostra visual brasileira com alcance e limites da inspeção |
| [Ferramentas e arquitetura](skills/cortes-virais-br/references/ferramentas.md) | FFmpeg, transcrição, ingestão, contratos e limitações |
| [Ferramentas de mídia](scripts/media.py) | Preflight, probe, transcrição opcional e render |
| [Avaliador](scripts/score_candidates.py) | Notas, intervalos de evidência e seleção determinística |
| [Briefing](docs/briefing.md) | Decisões confirmadas e suposições reversíveis |
| [Roadmap](docs/roadmap.md) | O que existe e o que falta implementar |
| [Validação](docs/validacao.md) | Testes executados, exemplo renderizado e limites da evidência |
| [Teste GTA 6](docs/teste-gta6.md) | Teste técnico com trailer rejeitado editorialmente e correções do fluxo |
| [Corte real do Alanzoka](docs/teste-alanzoka.md) | Publicação, tração observada, receita câmera+jogo e limites de revisão |
| [Configuração inicial](config/brief.example.json) | Defaults prontos; preencher o material e o tema da tarefa |
| [Decisões do projeto](config/project.json) | Política de vários nichos confirmada pelo usuário |
| [Ficha de referência](templates/referencia.example.json) | Registro de um vídeo realmente inspecionado |
| [Plano de corte](templates/plano.example.json) | Contrato inicial para fonte, timeline, edição e QA |
| [Exemplos](examples/README.md) | Testes sintéticos, teste de trailer rejeitado e receita do corte real |

## Edição baseada em evidências

O projeto atende a **vários nichos**, conforme o pedido e as tendências. Uma tarefa sobre games não deve virar um corte de futebol só porque futebol liderou uma busca geral. Em pedidos abertos, comparar oportunidades de temas diferentes e justificar a escolha com evidências atuais.

Foram inspecionados quadros públicos de quatro publicações oficiais brasileiras: conversa com imagens complementares, reação com composição simples e gameplay com câmera/textos/efeitos pontuais. O [relatório](docs/referencias-observadas.md) registra fonte, datas e o que foi observado. O áudio não foi ouvido e os vídeos não foram assistidos integralmente; a amostra não comprova viralidade nem uma preferência universal do Brasil.

Os presets de conversa, humor e gameplay são pontos de partida experimentais. Estudar referências atuais com áudio do nicho em cada tarefa e adaptar a técnica ao momento, preservando o padrão de 15–30 segundos.

Orientações de publicidade do TikTok estão identificadas como publicidade. Não são apresentadas como prova de desempenho de cortes orgânicos. Cada referência inclui seu alcance e limitações.

## Ferramentas e limites

Base atual: Python + FFmpeg/ffprobe. O render aceita cortes múltiplos, crop em pixels, exportação vertical, quadro completo com fundo desfocado (`contain_blur`), ASS/SRT e um manifesto técnico. faster-whisper é opcional para transcrição local; a combinação testada fixa PyAV 16.1.0. Download de lives, rastreamento de rosto, layouts de câmera+jogo, inserção de memes, trilha e efeitos não são automatizados pela CLI atual; o agente precisa usar ferramentas adicionais para esses elementos. Pedidos não suportados pela CLI devem gerar erro claro, sem ignorar elementos da edição.

yt-dlp e Remotion são opções documentadas para evoluir ingestão e composição. Não há servidor MCP nem serviço pago obrigatório. As dependências e modelos não são instalados pelo preflight.

Uma skill orienta o agente; ela não fornece acesso a vídeos, pesquisa, GPU ou execução por si só. O ambiente precisa disponibilizar essas capacidades.

## Entrega

Entregar um arquivo MP4 que exista e possa ser aberto, acompanhado de SRT quando útil. Preservar a origem e a fidelidade do contexto. Separar material planejado, renderizado, revisado e entregue. Publicação automática não faz parte do escopo atual.

Manter vídeos, modelos, credenciais e transcrições privadas fora do Git. Não instalar nem publicar o pacote apenas porque seus arquivos estão no repositório.

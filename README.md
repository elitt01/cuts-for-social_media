# Cuts for Social Media

Plugin em desenvolvimento: **Cortes Virais BR**. Repositório: [elitt01/cuts-for-social_media](https://github.com/elitt01/cuts-for-social_media).

Base de instruções e pesquisa para um agente descobrir momentos de lives, avaliar seu potencial, editar cortes em português brasileiro e entregar o vídeo quando solicitado.

Destinos confirmados: **TikTok, Instagram Reels e YouTube Shorts**. Preparar um master e ajustar variantes quando necessário para interfaces, legendas e requisitos atuais de cada plataforma.

**Estado: briefing em construção.** Este repositório contém um pacote de instruções em rascunho e referências pesquisadas em 20/11/2026. Não há plugin instalado, busca automatizada, pipeline de render implementado ou corte real validado nesta versão.

## Resultado pretendido

1. Identificar o pedido e escolher o nicho daquela tarefa: seguir o tema solicitado ou pesquisar oportunidades em vários nichos quando o pedido for aberto.
2. Consultar assuntos atuais relevantes, registrando região, janela e fontes.
3. Encontrar candidatos e assistir ao contexto da live original.
4. Comparar gancho, compreensão, desfecho, atualidade e qualidade audiovisual.
5. Criar um plano com timestamps, enquadramento, legendas PT-BR, áudio e efeitos com função.
6. Renderizar, revisar e entregar MP4 e legenda revisada quando pedidos.

A nota de potencial é uma heurística editorial, nunca uma probabilidade de viralização. Views observadas, interesse de busca e retenção são sinais diferentes. Dados indisponíveis permanecem desconhecidos.

## Onde encontrar

| Arquivo | Uso |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Regras para trabalhar neste projeto |
| [Skill principal](skills/cortes-virais-br/SKILL.md) | Ordem de execução para o agente |
| [Descoberta e seleção](skills/cortes-virais-br/references/selecao.md) | Pesquisa de tendências, critérios e comparação de desempenho |
| [Edição para o Brasil](skills/cortes-virais-br/references/edicao-br.md) | Legendas, ritmo, composição, áudio, presets e estudo de referências |
| [Ferramentas e arquitetura](skills/cortes-virais-br/references/ferramentas.md) | FFmpeg, transcrição, ingestão, contratos e limitações |
| [Briefing](docs/briefing.md) | Perguntas pendentes, uma decisão de cada vez |
| [Roadmap](docs/roadmap.md) | O que existe e o que falta implementar |
| [Configuração inicial](config/brief.example.json) | Preferências ainda não respondidas |
| [Decisões do projeto](config/project.json) | Política de vários nichos confirmada pelo usuário |
| [Ficha de referência](templates/referencia.example.json) | Registro de um vídeo realmente inspecionado |
| [Plano de corte](templates/plano.example.json) | Contrato inicial para fonte, timeline, edição e QA |

## Edição baseada em evidências

O projeto atende a **vários nichos**, conforme o pedido e as tendências. Uma tarefa sobre games não deve virar um corte de futebol só porque futebol liderou uma busca geral. Em pedidos abertos, comparar oportunidades de temas diferentes e justificar a escolha com evidências atuais.

Não foi assistida uma amostra audiovisual brasileira nesta rodada. Os três presets — conversa, humor e gameplay — são hipóteses iniciais detalhadas, não um estilo brasileiro já comprovado. Estudar referências reais com áudio do nicho escolhido em cada tarefa, incluindo cortes de desempenho comum; não aplicar a mesma edição a todos os assuntos.

Orientações de publicidade do TikTok estão identificadas como publicidade. Não são apresentadas como prova de desempenho de cortes orgânicos. Cada referência inclui seu alcance e limitações.

## Ferramentas previstas

V1 proposta: Python + FFmpeg/ffprobe + faster-whisper. yt-dlp é opcional para ingestão compatível com acesso e condições de uso; Remotion é opcional para animações mais complexas. Dependências, comandos e testes ainda serão implementados após o briefing.

Uma skill orienta o agente; ela não fornece acesso a vídeos, pesquisa, GPU ou execução por si só. O ambiente precisa disponibilizar essas capacidades.

## Entrega

Entregar um arquivo MP4 que exista e possa ser aberto, acompanhado de SRT quando útil. Preservar a origem e a fidelidade do contexto. Separar material planejado, renderizado, revisado e entregue. Publicação automática não faz parte do escopo atual.

Manter vídeos, modelos, credenciais e transcrições privadas fora do Git. Não instalar nem publicar o pacote apenas porque seus arquivos estão no repositório.

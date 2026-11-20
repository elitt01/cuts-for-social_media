---
name: cortes-virais-br
description: "Orientar pesquisa, seleção, edição e entrega de cortes de lives em português brasileiro. Usar ao buscar momentos com potencial de alcance, avaliar clipes, estudar referências de edição, planejar legendas e efeitos ou produzir um corte solicitado. Requer acesso às fontes e ferramentas de mídia no ambiente."
---

# Cortes Virais BR

## Identificar a tarefa

Distinguir descoberta de assunto, busca de momento em live fornecida, edição de clipe escolhido e entrega de arquivo existente. Executar as etapas pertinentes ao pedido, sem refazer descoberta ao apenas entregar um vídeo já pronto.

Ler a configuração do usuário quando existir. Respeitar a política confirmada: atender vários nichos conforme tendências e o pedido de cada tarefa. Não pedir um nicho permanente. Para outra escolha determinante ainda desconhecida, fazer uma pergunta por vez com opções. Continuar trabalho independente dessa resposta e registrar o que permanece desconhecido.

Consultar [seleção](references/selecao.md) para descoberta/ranking, [edição](references/edicao-br.md) para estilo/legendas e [ferramentas](references/ferramentas.md) para execução, contratos e QA. Carregar apenas o necessário.

Para a operação do repositório, ler [START_HERE.md](../../START_HERE.md). As ferramentas executáveis e seus contratos estão em [mídia](../../docs/ferramentas-cli.md) e [seleção](../../docs/selecao-cli.md); usar a raiz que contém config/project.json como diretório de trabalho.

## 1. Definir briefing e capacidade

Identificar tema/nicho da tarefa, público, plataformas, fontes, quantidade, duração, estilo e local de entrega conforme o pedido. Separar respostas do usuário de defaults experimentais.

O briefing do projeto está fechado. Adotar duração de 15–30 segundos quando o pedido não especificar outra; selecionar um arco completo que caiba nessa faixa. Como defaults reversíveis, produzir um corte por pedido, usar identidade visual neutra e entregar na sessão atual ou pasta local de saída. Não voltar a perguntar essas escolhas apenas porque os campos específicos de uma nova tarefa ainda não foram preenchidos.

Adotar TikTok, Instagram Reels e YouTube Shorts como destinos confirmados, salvo escopo diferente em uma tarefa. Conferir requisitos e interface atuais de cada destino; manter um master e produzir variantes quando houver diferença real de enquadramento, legendas, áudio ou assets. Não exigir novamente a escolha de plataforma nem presumir licença de música válida entre plataformas.

Adotar busca livre e aceitar links/arquivos enviados pelo usuário, sem exigir lista fixa de criadores. Distinguir material a editar de referência de estilo. Quando houver uma fonte explícita para a tarefa, priorizá-la; quando o pedido for de descoberta, procurar candidatos adequados em fontes acessíveis e registrar a origem. Não repetir a pergunta sobre liberdade de busca já respondida.

Se houver tema, criador ou nicho pedido, dar prioridade a esse escopo e pesquisar oportunidades relevantes dentro dele. Se o pedido for aberto, descobrir oportunidades em vários nichos e selecionar pela evidência atual, qualidade do momento e adequação ao público; justificar a escolha. Não usar só o ranking geral de buscas como critério. Não interpretar vários nichos como obrigação de misturar assuntos sem relação em um vídeo.

Verificar pesquisa, acesso audiovisual, arquivos, FFmpeg/ffprobe e transcrição disponíveis. Não prometer render ou coleta completa de plataformas sem essas capacidades. Usar arquivo fornecido quando uma URL não puder ser acessada.

Respeitar a execução híbrida confirmada: ChatGPT Work e computador local. Quando o usuário solicitar no Claude com o link deste repositório, carregar as mesmas decisões e instruções; usar CLAUDE.md e docs/execucao.md quando disponíveis. Distinguir o agente do ambiente executor. Não presumir que um link instala ferramentas, transfere arquivos entre serviços ou dá acesso ao computador. Identificar recursos da sessão e executar as etapas possíveis; registrar a dependência concreta quando outra etapa precisar de ambiente diferente.

## 2. Descobrir oportunidade atual

Pesquisar sinais recentes ligados ao nicho. Registrar fonte, data/hora com fuso, região e janela. Buscar confirmação independente quando possível. Distinguir interesse de busca, assunto em alta numa plataforma e desempenho de um clipe.

Não apresentar listas antigas como tendências atuais. Registrar dados indisponíveis como desconhecidos. Não prometer ranking TikTok sem acesso nem API Twitch sem autenticação configurada.

## 3. Encontrar e examinar candidatos

Localizar a fonte original e registrar criador, URL e timestamps. Assistir e ouvir o trecho com contexto anterior e posterior suficiente para entender premissa, ironia, participantes e resposta. Não usar título de reupload como prova do conteúdo.

Identificar gancho → contexto mínimo → desenvolvimento → desfecho. Descrever por que funciona para aquele público. Rejeitar montagem que depende de distorção ou oculta uma resposta que altera o sentido.

## 4. Comparar e escolher

Usar a matriz heurística versionada da referência de seleção. Justificar cada nota com observação/timecode. Manter intervalo e cobertura quando houver critérios desconhecidos; não preencher com zero nem apresentar nota como probabilidade.

Quando as fichas estiverem preenchidas, usar scripts/score_candidates.py para conferir a nota, a cobertura e a escolha determinística. A CLI valida declarações estruturadas: não assiste à fonte nem comprova as evidências. Preencher context_reviewed.mode=audiovisual somente após inspeção audiovisual real.

Separar a nota de potencial das métricas observadas. Comparar tração com contexto equivalente; não inferir retenção de vídeos de terceiros. Escolher a quantidade pedida e apresentar motivos e limitações de forma breve quando fizer parte do pedido.

Seguir o fluxo automático confirmado: escolher o melhor trecho entre os candidatos viáveis, editar, revisar e entregar o arquivo pronto. Fazer comparação e planejamento internamente, sem criar uma aprovação intermediária de candidatos. Mostrar opções antes de editar apenas se o usuário pedir. Se nenhum candidato viável for encontrado, ampliar a pesquisa dentro do escopo e relatar um impedimento concreto quando necessário; não substituir a entrega por uma promessa de viralidade.

## 5. Estudar e aplicar estilo

Aplicar a política confirmada: adaptar a edição ao clipe e usar memes/efeitos quando ajudarem. Ajustar intensidade ao nicho, à ação e ao momento, sem impor efeitos frequentes por padrão. Pesquisar referências de edição autonomamente; aceitar exemplos do usuário quando fornecidos, sem torná-los uma exigência para começar.

Estudar referências audiovisuais reais do nicho e formato escolhidos para aquela tarefa antes de afirmar que reproduz um estilo. Manter fichas por tipo de conteúdo, sem transferir automaticamente ritmo e efeitos de gameplay para entrevista ou notícia. Registrar técnicas e timing; extrair parâmetros próprios sem copiar identidade ou inventar nomes de fontes tipográficas.

Consultar a [amostra visual observada](../../docs/referencias-observadas.md) como ponto de partida. Ela usa quadros públicos e mantém áudio/reprodução integral pendentes; não a tratar como referência audiovisual já revisada ou prova de preferência do público.

Usar presets conversa, humor ou gameplay como defaults experimentais, refinando-os com referências realmente inspecionadas para a tarefa. O agente pode selecionar essas referências; não exigir aprovação de estilo em cada corte. Preservar ação e reação. Usar zoom, meme, música e texto quando contribuírem para compreensão ou efeito narrativo.

Transcrever PT-BR, revisar nomes/gírias/negações e sincronizar na timeline de saída. Conservar a transcrição bruta e o mapeamento de cortes para corrigir sincronismo.

## 6. Renderizar e conferir

Definir plano com entradas/saídas, crops, legendas, assets e áudio. Usar ferramentas realmente instaladas e registrar versões. Não transformar pseudocódigo em alegação de execução.

Usar scripts/media.py preflight/probe e render conforme o contrato documentado. A ferramenta atual corta, concatena, enquadra geometricamente e aplica ASS/SRT; transcrição é opcional. Para efeitos, memes, trilha ou layouts não suportados, aplicar ferramentas adicionais disponíveis e validar o resultado, sem prometer que a CLI implementa esses elementos. Registrar o mapeamento por frames gerado pelo render e alinhar as legendas à saída real.

Gerar MP4 e legenda revisada quando solicitado. Verificar reprodução, streams, duração e codecs; assistir e ouvir integralmente o exportado, conferir celular/interface, começo, final e contexto. Registrar explicitamente `not_checked` quando uma revisão não puder ser feita.

## 7. Entregar e aprender

Entregar arquivo/link verificado no destino pedido, com SRT e crédito quando úteis. Distinguir planejado, renderizado, revisado e entregue. Não publicar, agendar ou enviar a terceiros sem pedido.

Quando houver resultados reais autorizados, comparar desempenho por plataforma e janela equivalente. Atualizar hipóteses/pesos com versão e evidência; não atribuir causalidade a efeitos com base em um sucesso isolado. Nunca garantir viralidade.

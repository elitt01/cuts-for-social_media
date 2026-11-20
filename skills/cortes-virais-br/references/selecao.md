# Descoberta e seleção de cortes — pesquisa e proposta

Consulta: 20/11/2026, America/Sao_Paulo. Escopo: público brasileiro; vários nichos conforme tendências e o pedido; TikTok, Instagram Reels e YouTube Shorts. Política de fontes: busca livre com links/arquivos do usuário, sem lista fixa de criadores.

## O que o agente deve distinguir

1. **Potencial editorial**: avaliação do conteúdo antes de publicar, apoiada em contexto, gancho, compreensão e desfecho. Uma nota heurística ajuda a priorizar; não é probabilidade de viralizar.
2. **Tração observada**: visualizações, crescimento e outras métricas realmente vistas ou fornecidas, sempre com instante de coleta e referência comparável. O total de views sozinho não permite afirmar que um corte viralizou.
3. **Tendência de assunto**: aumento de interesse por um tema numa região e janela. Não comprova que qualquer vídeo sobre o assunto terá bom desempenho.

O resultado operacional deve dizer: “candidato com potencial alto, evidência parcial de tendência, desempenho ainda não observado”, em vez de “este vídeo vai viralizar”.

## Fontes e possibilidades reais

### Adequação antes da nota

O padrão confirmado é um momento real de criador, streamer ou famoso diante de um acontecimento engraçado, estranho ou inesperado. Em games, conferir pessoa jogando, acontecimento e reação. Trailer, publicidade e reação a trailer não substituem gameplay sem escolha explícita do usuário. Descartar formatos incompatíveis antes de comparar notas; disponibilidade de download não compensa conteúdo errado.

O usuário prefere um momento cuja repercussão já tenha sido observada. Registrar o upload exato, quem publica, quem aparece, datas e métricas disponíveis. Distinguir fanpage de conta do criador. Um embed da publicação é evidência primária de seus campos; contadores de espelhos são secundários e não devem substituir silenciosamente campos indisponíveis. Campo zero suspeito/ausente não comprova ausência de views. Publicação de um fã pode localizar o momento, mas exige rastrear o contexto e indicar sua origem.

Se houver apenas tração observada sem base comparável, usar esse rótulo e continuar a busca por confirmação; não apresentar potencial ou celebridade como viralidade comprovada. Em falha de acesso, manter tema e formato e tentar outra fonte ou candidato válido. Não trocar por um trailer por ser fácil de obter.

| Fonte | O que obter | Limitação importante |
| --- | --- | --- |
| Google Trends — Em alta, Brasil | Assuntos com crescimento recente; janela de 4h, 24h, 48h ou 7d, estado ativo/finalizado e volume em faixas. Exportação CSV/RSS descrita oficialmente. | Interesse de busca não equivale a consumo de cortes. A página tem agrupamentos de consultas; não somar variantes como assuntos independentes. |
| Google Trends — Explorar | Comparação relativa entre termos/tópicos na mesma consulta e região. | Índice normalizado de 0 a 100, não número absoluto de buscas. Zero pode ser volume insuficiente. |
| YouTube público | Conteúdo, título, canal, data e métricas que estiverem visíveis; localizar live original e cortes recentes. | Busca indexada pode atrasar; não fornece retenção de canais de terceiros. Resultados não são amostra representativa do Brasil. |
| YouTube Data API, se configurada | Busca com filtros de publicação, canal e lives concluídas; metadados e estatísticas por recursos apropriados. | `regionCode=BR` indica disponibilidade para assistir no Brasil; não prova audiência brasileira. `relevanceLanguage=pt` prioriza relevância linguística, mas admite outros idiomas. |
| Twitch — páginas públicas de clipes | Assistir e ler o que estiver publicamente acessível. | Não prometer coleta estruturada integral sem autenticação. |
| Twitch Get Clips, se configurada | Filtrar por canal/jogo e período; ler data, views, idioma, duração e referência ao VOD quando existente. | A API exige token de app ou usuário; o ranking devolvido por canal/jogo usa contagem de views, não aceleração. |
| TikTok Creative Center | Documentação descreve tendências por setor/período e análises de hashtags/regiões. | A documentação atual manda fazer login. A URL BR abriu apenas a estrutura de página e um botão de login nesta pesquisa; não afirmar que o ranking foi coletado. |
| Analytics autorizado do próprio perfil | Retenção, duração média, continuidade após os segundos iniciais e métricas nativas disponíveis. | Dados privados: usar conexão autorizada ou exportação do usuário; não estimar a partir das métricas públicas. |

### Registro do acesso público nesta pesquisa

`https://trends.google.com/trending?geo=BR` retornou Brasil, janela “Past 24 hours”, e linhas de tendências. Exemplos observados na resposta: “vasco da gama x internacional”, “são paulo x fluminense” e “ec vitória x bragantino”. São exemplos de coleta, **não recomendações de nicho** e não ficam gravados como tendências permanentes do plugin. O conteúdo está sujeito a cache da busca e deve ser reconfirmado quando um corte real for solicitado.

`https://ads.tiktok.com/creative/creativeCenter/trends?countryCode=BR&period=7` não apresentou ranking legível ao coletor. Registrar `unavailable`, com esse motivo, em vez de fabricar hashtags.

## Processo recomendado para cada pedido

### 1. Ler o briefing e delimitar a busca

Ler público, política de nichos, objetivo, plataforma de entrega, canais permitidos e restrições editoriais. Seguir tema, criador ou nicho explicitamente pedido. Quando o pedido for aberto, pesquisar oportunidades em vários nichos e comparar qualidade do momento e evidência atual; não voltar a exigir um nicho fixo. Perguntar uma decisão por vez apenas quando outra escolha desconhecida mudar materialmente o resultado. Não escolher política, esportes, games ou celebridades apenas porque aparecem no ranking geral.

Identificar o pedido: descobrir assunto, encontrar um trecho numa live fornecida, editar um clipe já escolhido ou entregar um arquivo existente. Evitar refazer toda a descoberta em pedidos de simples edição/entrega.

### 2. Registrar um retrato datado das tendências

Proposta operacional, não lei de plataforma: iniciar com Brasil/24h, comparar 7d para distinguir pico de assunto duradouro e consultar 4h quando a atualidade for relevante. Fixar a mesma região e janela nos dados comparados. Registrar atualização da fonte quando ela aparecer, além do horário de acesso.

Buscar confirmação em outra fonte de origem independente e ligada ao nicho: canal oficial do acontecimento, publicação original do criador ou outra plataforma. Duas matérias copiadas da mesma agência não contam como duas confirmações independentes. Se só houver uma fonte, rotular evidência limitada e seguir sem inventar corroboradores.

Aceitar um assunto apenas se houver uma ponte explícita com o público e com o conteúdo real da live. Uma palavra no título ou hashtag não basta.

### 3. Levantar candidatos e preservar contexto

Proposta inicial ajustável: descobrir 10–20 candidatos, examinar 3–5 em profundidade e selecionar conforme a quantidade pedida. Esses números são orçamento de trabalho, não metas empíricas de viralidade.

Para cada candidato, localizar a fonte original, assistir ao trecho com áudio e rever contexto anterior/posterior suficiente para entender participantes, premissa, ironia e desfecho. Registrar os timecodes exatos do trecho e da janela de contexto examinada. Não declarar avaliação audiovisual se só houver transcrição.

Na falta de acesso à fonte, manter como candidato não verificado. Não usar título provocativo de um reupload como prova do que a pessoa disse.

### 4. Exigir um arco reconhecível

Descrever em uma frase cada parte: **gancho → contexto mínimo → desenvolvimento → entrega/desfecho**. O desfecho pode ser uma piada, reação, demonstração, informação útil, surpresa ou resposta completa. Falta de desfecho não deve ser compensada por legenda chamativa.

Tipos de gancho a procurar, como hipóteses editoriais a testar: pergunta concreta respondida no trecho; contradição aparente resolvida; erro e correção; reação com causa compreensível; desafio com resultado; demonstração visual; relato com consequência. Evitar “você não vai acreditar” quando o conteúdo não cumpre a promessa.

### 5. Avaliar potencial com notas ancoradas

Todos os pesos e limiares abaixo são **heurísticas iniciais**, a calibrar com histórico real do usuário. Usar notas inteiras de 0–4: 0 ausente; 1 fraco; 2 aceitável; 3 forte; 4 excepcional, com evidência e timecode. Uma nota sem justificativa observável não é válida.

| Critério | Peso | Nota 4 exige |
| --- | ---: | --- |
| Gancho claro e fiel | 20 | A abertura apresenta imediatamente a tensão/pergunta real e o trecho cumpre a promessa. |
| Desfecho e satisfação | 20 | Existe entrega completa identificável, compreensível sem assistir à live inteira. |
| Compreensão sem contexto externo | 15 | Quem nunca viu o canal entende quem faz o quê e por que aquilo importa. |
| Adequação ao público escolhido | 15 | Linguagem, tema e situação correspondem ao briefing, com justificativa específica. |
| Relevância no momento | 10 | Há ligação real com evidência atual e datada do nicho, ou motivo editorial explícito para ser atemporal. |
| Distinção e novidade | 10 | O momento tem informação, reação ou perspectiva específica; não depende apenas de um nome famoso. |
| Viabilidade audiovisual | 10 | Fala inteligível e enquadramento vertical viável preservando a ação relevante. |

`potencial = soma(peso × nota / 4)`, entre 0 e 100. Nunca exibir como “chance de viralizar”.

Não substituir dado faltante por zero. Produzir intervalo: limite inferior soma apenas contribuições conhecidas; limite superior acrescenta todo o peso dos critérios ainda não avaliados. Exemplo fictício: 60 pontos conhecidos e peso desconhecido 20 ⇒ intervalo 60–80, não nota 75 normalizada nem nota 60 final. Informar cobertura de evidência de 80%.

Proposta de triagem quando todos os critérios estiverem avaliados: 80–100 priorizar; 65–79 considerar com ajuste; abaixo de 65 não priorizar. Gancho, desfecho e viabilidade abaixo de 2 exigem revisão mesmo com total alto. Esses cortes são convenção interna, não validação estatística.

### 6. Calcular tração apenas com dados observados

Guardar snapshots, não só totais. Com dois snapshots válidos: `velocidade = (views_t2 − views_t1) / horas_decorridas`. Com um snapshot, `views / idade_em_horas` é média desde a publicação e deve receber esse nome; não chamá-la de aceleração atual.

Comparar, preferencialmente, com mediana de peças do mesmo perfil, plataforma, formato, faixa de duração e idade desde a publicação. Não comparar um vídeo de 30 minutos há 3 anos com um Short publicado ontem. Não misturar contagens de plataformas distintas numa tabela de posições sem explicar as diferenças de definição.

Sem histórico em idades equivalentes, declarar base imperfeita ou tração indeterminada. Dados insuficientes para comprovar viralidade não impedem avaliar o potencial editorial.

Proposta de rótulos: `desempenho_desconhecido`, `tracao_observada_sem_base`, `acima_da_base`, `abaixo_da_base`. “Viral observado” requer que o projeto defina previamente o limiar contextual e que os dados realmente o cumpram. Não estabelecer “100 mil views = viral” como regra universal.

Retenção, compartilhamentos, salvamentos e conclusão só entram quando a fonte de fato os fornece. Likes/comments públicos são sinais parciais. Muitos comentários podem refletir confusão ou disputa, não satisfação. Não inferir retenção de um clipe de terceiros por meio de views.

## Rejeições e revisão necessária

- Falta de fonte audiovisual acessível ou timecodes verificáveis: manter na fila de pesquisa; não aprovar como trecho validado.
- Gancho exige distorcer fala, esconder uma negação ou unir frases fora de contexto: rejeitar essa montagem.
- Momento só funciona para quem acompanhou horas de live: ampliar contexto se couber; caso contrário, escolher outro momento.
- Trecho em outra língua/registro não atende ao briefing: não tratá-lo como aderente ao Brasil por estar disponível aqui.
- Assunto apenas aparece em ranking geral sem conexão com o público: despriorizar, mantendo alternativa atemporal.
- Material sem acesso/condição de uso resolvida: registrar pendência; usar fonte fornecida/autorizada quando necessária para renderizar e entregar.
- Cortes duplicados do mesmo momento: agrupar e avaliar o original; popularidade de reuploads não equivale a novidade.

## Contrato mínimo de evidência

```json
{
  "candidate_id": "identificador-estavel",
  "source_url": null,
  "source_file": null,
  "platform": "youtube|twitch|arquivo|outro",
  "creator": "nome conferido",
  "published_at": null,
  "observed_at": "ISO-8601 com fuso",
  "source_start_seconds": null,
  "source_end_seconds": null,
  "context_reviewed": {"start_seconds": null, "end_seconds": null, "mode": "unavailable"},
  "trend_evidence": [{"url": "URL consultada", "geo": "BR", "window": "24h", "observed_at": "ISO-8601", "source_updated_at": null, "status": "available|unavailable", "claim": "o que foi observado", "metric_name": null, "metric_value": null}],
  "potential": {"heuristic_version": "0.1", "criteria": {"gancho": null, "desfecho": null, "compreensao": null, "adequacao": null, "relevancia": null, "novidade": null, "viabilidade": null}},
  "observed_performance": {"snapshots": [], "label": "desempenho_desconhecido", "comparison_cohort": null},
  "decision": "research|shortlist|reject",
  "reason": "justificativa concreta",
  "missing_data": []
}
```

Esta é uma ficha a preencher, não uma prova de inspeção nem um conector de busca. Para usar o avaliador, fornecer uma lista dessas fichas ou o objeto {candidates:[...]}; uma nota conhecida usa {score,evidence,timecode_seconds}, enquanto notas ausentes são null. O [guia do avaliador](../../../docs/selecao-cli.md) documenta o contrato executável; os campos extras de pesquisa são preservados no registro do agente. Guardar consultas, período e limitações de acesso. Nunca marcar modo audiovisual a partir de storyboards ou transcrição isolada.

## Aprendizado posterior

Quando o usuário fornecer resultados, comparar previsões editoriais com as métricas reais do próprio perfil. Coletar snapshots em marcos consistentes definidos pelo projeto e preservar plataforma, duração e tamanho da amostra. Testar uma mudança de edição por vez quando possível. Atualizar pesos com versão e justificativa; manter contraexemplos, incluindo cortes aprovados que foram mal. Não atribuir causalidade a um efeito de edição só porque um vídeo teve mais views.

## Fontes primárias verificadas

1. Google, Em alta: https://support.google.com/trends/answer/3076011?hl=pt-BR — janelas, estados, atualização e exportações.
2. Google Trends BR, página observada: https://trends.google.com/trending?geo=BR — exemplos do retrato público, sujeitos a cache e nova verificação.
3. Google, FAQ dos dados Trends: https://support.google.com/trends/answer/4365533?hl=pt-BR — normalização e amostragem.
4. YouTube, desempenho do conteúdo: https://support.google.com/youtube/answer/12220281?hl=pt-BR — distinções de visualizações e métricas disponíveis no Analytics.
5. Google for Developers, busca YouTube: https://developers.google.com/youtube/data/reference/rest/v3/search/list — parâmetros, limitações e semântica de região/idioma.
6. Twitch Developers, Get Clips: https://dev.twitch.tv/docs/api/reference/clips — autenticação, filtros e metadados.
7. TikTok, Como utilizar as tendências: https://ads.tiktok.com/resources/help/article/how-to-use-trends?lang=pt — atualização julho/2026, login e filtros.
8. TikTok Creative Center BR: https://ads.tiktok.com/creative/creativeCenter/trends?countryCode=BR&period=7 — acesso não forneceu ranking legível nesta consulta.

Os critérios, pesos, limiares e quantidades de candidatos são propostas do projeto, não afirmações empíricas extraídas dessas fontes. Não foi executado experimento de desempenho de cortes nesta pesquisa.

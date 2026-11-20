# Comece aqui — pedido de corte pronto

Este projeto orienta um agente com acesso às ferramentas necessárias a encontrar, avaliar, editar e entregar um corte. O briefing está fechado. Ler o estado de implementação no [README](README.md), sem confundir instruções e testes técnicos com uma validação de viralidade.

## Carregar o projeto

1. Ler [AGENTS.md](AGENTS.md), [config/project.json](config/project.json) e a [skill principal](skills/cortes-virais-br/SKILL.md).
2. Usar [CLAUDE.md](CLAUDE.md) como entrada quando o pedido estiver no Claude; seguir o mesmo fluxo e a mesma configuração.
3. Identificar a tarefa: descobrir uma oportunidade, editar o material enviado, avaliar um trecho ou entregar um arquivo já existente. Fazer somente as etapas que o pedido exige.
4. Conferir quais ferramentas e arquivos estão acessíveis na sessão. O [guia de execução](docs/execucao.md) explica Work, computador local e Claude.

## Decisões prontas para usar

| Aspecto | Padrão |
| --- | --- |
| Público | Brasileiro, português brasileiro |
| Assunto | Seguir o pedido; descobrir oportunidades em vários nichos se o pedido for aberto |
| Fontes | Busca livre e links/arquivos enviados pelo usuário |
| Destinos | TikTok, Instagram Reels e YouTube Shorts |
| Seleção | O agente compara candidatos e escolhe o melhor viável |
| Duração | 15–30 segundos, salvo outro pedido explícito |
| Edição | Adaptar ao clipe; memes e efeitos quando ajudarem |
| Revisão | Conferência técnica e audiovisual antes de declarar o corte revisado |
| Entrega | Vídeo pronto quando solicitado; publicação automática fora do escopo |

Como suposições reversíveis, adotar um corte por pedido, identidade neutra e entrega na sessão atual ou pasta local. Um pedido explícito pode mudar quantidade, estilo, duração e destino. Não reabrir o briefing para confirmar esses padrões a cada tarefa.

## Executar a tarefa

1. Consultar tendências atuais quando forem relevantes, registrando URL, região, janela e data. Uma lista antiga não serve como radar atual.
2. Localizar o material original e verificar contexto anterior/posterior. Separar o que foi assistido, lido, inferido e ainda não foi conferido.
3. Comparar candidatos com a [matriz de seleção](skills/cortes-virais-br/references/selecao.md). Uma nota organiza potencial editorial; não representa chance de viralizar.
4. Escolher um trecho com gancho, contexto mínimo e desfecho que caiba em 15–30 segundos. Se o momento depender de contexto maior, procurar outro intervalo completo; não esconder a resposta nem acelerar a fala apenas para caber.
5. Pesquisar referências audiovisuais do nicho e definir uma receita de edição. Seguir o [guia editorial](skills/cortes-virais-br/references/edicao-br.md), distinguindo preferências, hipóteses e observações reais.
6. Preencher um plano a partir do [modelo](templates/plano.example.json), com fonte, intervalos, crop, legenda na timeline final e formato de saída.
7. Transcrever/revisar PT-BR e renderizar com ferramentas realmente disponíveis. Não prometer uma etapa que o ambiente não consegue executar.
8. Conferir o arquivo exportado: reprodução, duração, streams, legendas, enquadramento, fidelidade e áudio. Um manifesto técnico não prova revisão audiovisual.
9. Entregar o MP4 e, quando útil, SRT e crédito. Registrar o que foi efetivamente revisado e o caminho/link de entrega confirmado.

Comparar candidatos e preparar a edição internamente. Mostrar uma lista para aprovação antes de editar apenas se o usuário pedir esse fluxo.

## Pedido pronto para copiar

```text
Use https://github.com/elitt01/cuts-for-social_media e comece por START_HERE.md.
Siga config/project.json e as instruções compartilhadas do projeto.
Quero um corte pronto sobre [assunto] / deste material: [link ou arquivo].
Se eu não definir um assunto ou uma fonte, busque uma oportunidade atual.
Escolha o melhor trecho, edite e revise. Use 15–30 segundos por padrão.
Entregue o vídeo; relate apenas bloqueios concretos e verificações pendentes.
```

Não é necessário enviar uma live inteira apenas para pedir descoberta. Para editar um arquivo local, o agente precisa conseguir acessar esse arquivo no ambiente executor; um link do repositório não transfere a mídia entre serviços.

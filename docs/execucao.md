# Execução no Work, no computador e pelo Claude

Decisão confirmada em 20/11/2026: usar o ambiente do ChatGPT Work e o computador local conforme a tarefa. Preparar também uso no Claude quando o usuário pedir e fornecer o link do repositório.

Esta versão fornece instruções compartilhadas e um ponto de entrada. O pipeline de vídeo ainda será implementado e não houve teste de execução no Claude. Consultar o [roadmap](roadmap.md) para distinguir componentes atuais de planejados.

## Início comum

1. Ler [AGENTS.md](../AGENTS.md), [README.md](../README.md), [config/project.json](../config/project.json) e a [skill principal](../skills/cortes-virais-br/SKILL.md).
2. Identificar se a tarefa é descobrir, selecionar, editar material fornecido ou entregar um resultado existente.
3. Aplicar as decisões confirmadas: vários nichos; TikTok/Reels/Shorts; busca livre com links e arquivos do usuário; escolher o melhor trecho, editar, revisar e entregar pronto sem exigir escolha intermediária de candidatos.
4. Conferir capacidades reais: leitura da fonte e contexto, áudio/vídeo, terminal, dependências, espaço e modo de entregar arquivos.
5. Executar as etapas autorizadas que forem possíveis. Registrar uma dependência concreta quando outra etapa precisar de recursos ausentes.

Não presumir compartilhamento automático de arquivos, modelos, contas ou resultados entre ambientes. Uma mudança de agente deve retomar os mesmos dados e decisões, sem inventar uma execução anterior.

## No ChatGPT Work

Usar o executor disponível e os anexos acessíveis na sessão. Conferir FFmpeg/ffprobe, transcrição e acesso à rede antes de planejar download ou render. Não presumir GPU, dependências instaladas, acesso ao PC local ou persistência de arquivos de outra sessão.

## No computador local

Usar uma cópia do repositório e os arquivos realmente acessíveis ao agente nessa máquina. Conferir sistema operacional, dependências e recursos. Reaproveitar os mesmos formatos de plano, referência e evidência. Não tratar instruções planejadas em scripts/ como comandos já implementados.

## No Claude com o link do repo

Enviar o endereço junto com uma tarefa explícita. Exemplo de pedido:

```text
Use este projeto: https://github.com/elitt01/cuts-for-social_media
Leia README.md, AGENTS.md, config/project.json e
skills/cortes-virais-br/SKILL.md. Confira as ferramentas disponíveis
e siga as decisões confirmadas do projeto.
Minha tarefa: [descreva o corte, a busca ou a edição desejada].
```

Se a sessão puder ler o repositório, usar [CLAUDE.md](../CLAUDE.md) como entrada para os arquivos compartilhados. Se o link não permitir acessar um arquivo necessário, indicar qual arquivo falta e a etapa que depende dele; não afirmar que todo o repo foi carregado. Executar comandos de mídia apenas se houver ambiente e ferramentas apropriados naquela sessão.

Para Claude Code, a documentação oficial descreve CLAUDE.md como um arquivo de instruções de projeto. O arquivo deste repo direciona a leitura para a configuração e o fluxo compartilhados; não instala plugin nem servidor. Essa orientação não presume que toda interface do Claude carregue o arquivo automaticamente ao receber um link.

## Continuidade e entrega

Registrar o material de origem, identificação do trabalho, intervalos usados, evidências, estado das revisões e caminhos dos artefatos. Preservar planos e legendas com a mesma referência temporal ao mudar de ambiente. Identificar quais arquivos precisarão estar acessíveis no ambiente de destino; manter mídia e dados privados fora do Git.

Entregar somente arquivos existentes no destino solicitado, após a revisão possível. Dizer quais verificações foram feitas. Receber uma saída de outro agente não comprova por si que o vídeo foi assistido ou entregue.

## Fonte técnica

Documentação oficial do Claude Code, consultada em 20/11/2026: [How Claude remembers your project](https://code.claude.com/docs/en/memory). A referência sustenta o uso de CLAUDE.md para contexto de projeto no Claude Code; o roteiro de execução e as condições acima são decisões deste projeto.

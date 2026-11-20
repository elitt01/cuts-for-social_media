# Estado e evolução do projeto

## Disponível nesta versão

- Briefing fechado: vários nichos, três plataformas, busca livre com links/arquivos, execução híbrida, seleção automática, edição adaptativa e duração padrão de 15–30s.
- Instruções compartilhadas, START_HERE.md e entrada CLAUDE.md.
- Avaliador de candidatos com evidências, dados ausentes, intervalos de nota e elegibilidade documentados.
- Ferramentas de preflight, probe e render com cortes múltiplos, crop geométrico, enquadramento `cover`/`contain_blur`, ASS/SRT e manifesto técnico.
- Wrapper de transcrição opcional com faster-whisper e idioma pt/en/auto; português por padrão. ASR small CPU INT8 executado em duas fontes reais; precisão de fala PT-BR ainda não validada por escuta.
- 32 testes com dados e mídia sintéticos, incluindo sincronismo, proporção visual e preservação de fontes.
- Primeiro [teste com trailer oficial de GTA 6](teste-gta6.md): rejeitado editorialmente pelo usuário; conserva validação técnica.
- [Corte do Alanzoka](teste-alanzoka.md): 23s, 1080×1920, câmera+jogo por receita específica; tração observada, inspeção de quadros e decodificação completa. Revisão integral com áudio e avaliação do usuário pendentes.
- Observação visual parcial de quatro publicações brasileiras oficiais; fontes, datas e limites registrados.

## Validações e capacidades ainda pendentes

1. Assistir a referências atuais e a um corte real com áudio; os storyboards não substituem essa revisão.
2. Avaliar nomes, gírias, falantes e timestamps da transcrição em PT-BR; inferência executada não significa precisão aprovada.
3. Completar revisão audiovisual e avaliação do corte real do Alanzoka. Não tratar o trailer rejeitado como sucesso editorial.
4. Validar a mesma receita em uma sessão do Claude e no computador escolhido pelo usuário; portabilidade documental não comprova dependências instaladas.

## Evoluções opcionais

- Ingestão assistida por yt-dlp ou APIs oficiais, conforme acesso disponível.
- Composição câmera+jogo, rastreamento, inserção de memes, trilha e efeitos; os campos não suportados pela CLI atual geram erro.
- Integração de modelos de legenda animada, se necessária e compatível com recursos/licença.
- JSON Schemas completos e validação em CI.
- Empacotamento e instalação do plugin quando solicitados; o repositório não foi instalado automaticamente.

## Para declarar um corte pronto

- O arquivo MP4 existe, reproduz e atende ao pedido, com legendas revisadas.
- Fonte, timestamps, motivo da escolha e limites dos dados estão registrados.
- A edição preserva contexto e desfecho; cortes mantêm sincronismo de áudio e legenda.
- Revisões técnica e audiovisual foram feitas e registradas honestamente.
- A entrega é confirmada no destino pedido. O manifesto de render permanece pendente até a revisão/entrega real do agente.

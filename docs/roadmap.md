# Estado e evolução do projeto

## Disponível nesta versão

- Briefing fechado: vários nichos, três plataformas, busca livre com links/arquivos, execução híbrida, seleção automática, edição adaptativa e duração padrão de 15–30s.
- Instruções compartilhadas, START_HERE.md e entrada CLAUDE.md.
- Avaliador de candidatos com evidências, dados ausentes, intervalos de nota e elegibilidade documentados.
- Ferramentas de preflight, probe e render com cortes múltiplos, crop geométrico, ASS/SRT e manifesto técnico.
- Wrapper de transcrição PT-BR opcional com faster-whisper; sem inferência real validada nesta rodada.
- Testes com dados e mídia sintéticos, incluindo sincronismo e preservação de fontes.
- Observação visual parcial de quatro publicações brasileiras oficiais; fontes, datas e limites registrados.

## Validações e capacidades ainda pendentes

1. Assistir a referências atuais e a um corte real com áudio; os storyboards não substituem essa revisão.
2. Executar inferência de transcrição com modelo disponível e avaliar nomes, gírias e timestamps em PT-BR.
3. Fazer uma entrega real a partir de material acessível, registrando fonte, contexto, revisão e destino.
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

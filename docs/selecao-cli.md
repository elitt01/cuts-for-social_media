# Avaliar candidatos no terminal

O avaliador usa Python 3 e biblioteca padrão. Ele recebe avaliações feitas pelo agente e produz uma seleção determinística. Não pesquisa tendências, não assiste a vídeos e não mede probabilidade de viralização. As afirmações de inspeção e as evidências precisam ser verificadas pelo agente antes de preencher o arquivo.

```bash
python3 scripts/score_candidates.py /caminho/candidatos.json --output /caminho/ranking.json
python3 -m unittest discover -s tests -p 'test_selection.py' -v
```

Omitir `--output` imprime o resultado. Erros de JSON, tipos, notas, evidências, timestamps ou intervalos encerram com código 2 e explicação em stderr; não produzem ranking parcial. Um resultado válido sem vencedor usa `status: research_required` e código 0.

## Contrato de entrada

Aceitar uma lista de candidatos ou `{ "candidates": [...] }`. `candidate_id` deve ser texto único. Notas ficam em `potential.criteria`; usar estas sete chaves sem acentos: `gancho`, `desfecho`, `compreensao`, `adequacao`, `relevancia`, `novidade`, `viabilidade`.

Cada nota conhecida é um objeto com `score` inteiro 0–4, `evidence` textual não vazia e `timecode_seconds` numérico na timeline da fonte. Esse instante aponta o momento do corte que sustenta a justificativa; uma avaliação de relevância deve citar na evidência a fonte/datada do assunto ou explicar seu valor atemporal. Critérios ausentes ou `null` ficam desconhecidos. `0` é uma avaliação conhecida de ausência do atributo e também exige evidência.

Exemplo fictício completo, sem alegar inspeção real:

```json
{
  "candidates": [{
    "candidate_id": "exemplo-ficticio",
    "source_url": "https://example.org/live",
    "source_start_seconds": 10,
    "source_end_seconds": 30,
    "context_reviewed": {"start_seconds": 0, "end_seconds": 45, "mode": "audiovisual"},
    "potential": {"criteria": {
      "gancho": {"score": 3, "evidence": "Exemplo: pergunta concreta inicia o trecho.", "timecode_seconds": 10},
      "desfecho": {"score": 3, "evidence": "Exemplo: a resposta conclui a pergunta.", "timecode_seconds": 29},
      "compreensao": {"score": 3, "evidence": "Exemplo: participantes e situação estão claros.", "timecode_seconds": 12},
      "adequacao": {"score": 3, "evidence": "Exemplo: vocabulário corresponde ao briefing.", "timecode_seconds": 14},
      "relevancia": {"score": 3, "evidence": "Exemplo: situação tem valor atemporal, com motivo registrado.", "timecode_seconds": 15},
      "novidade": {"score": 3, "evidence": "Exemplo: resposta contém demonstração específica.", "timecode_seconds": 23},
      "viabilidade": {"score": 3, "evidence": "Exemplo: fala e ação ficam legíveis no vertical.", "timecode_seconds": 20}
    }},
    "observed_performance": {"snapshots": []}
  }]
}
```

Arquivos locais podem ser identificados por `source_file` em vez de `source_url`. O avaliador apenas valida a estrutura declarada; não abre a fonte nem testa sua disponibilidade. Não há bloqueio por um campo de direitos desconhecido.

## Cálculo e escolha

Os pesos seguem a [matriz editorial](../skills/cortes-virais-br/references/selecao.md): 20/20/15/15/10/10/10. Calcular `soma(peso × score / 4)` sem arredondamento intermediário. A versão heurística é `0.1`.

- Todos os critérios conhecidos: `score` contém o resultado final e o intervalo é fechado nesse valor.
- Algum critério desconhecido: `score` permanece `null`; `range_min` soma contribuições conhecidas e `range_max` acrescenta os pesos desconhecidos. A cobertura é a soma dos pesos conhecidos, não a fração de campos preenchidos. Não renormalizar.
- Elegibilidade exige fonte informada, intervalo válido, inspeção `audiovisual` com contexto cobrindo o corte, todas as notas conhecidas, gancho/desfecho/viabilidade pelo menos 2 e total pelo menos 65. Entre 65 e 79, a categoria é `considerar_com_ajuste`; a edição deve tratar os ajustes. Acima ou igual a 80, `priorizar`.
- Ordenar elegíveis primeiro, depois completos bloqueados, depois incompletos. Dentro do grupo, usar limite inferior decrescente, cobertura decrescente e `candidate_id` crescente. O limite superior nunca escolhe um vencedor. Se ninguém for elegível, informar `research_required` e os motivos individuais.

Os limiares são convenções iniciais do projeto. Uma nota alta não substitui qualidade do material nem garante audiência. O CLI não comprova que as evidências textuais são verdadeiras.

`potential.assessment_status` distingue `complete` de `incomplete`. Cobertura de evidência não é confiança estatística nem probabilidade; `selection_eligible` e `selection_blockers` indicam se o registro está pronto para a escolha ou precisa de pesquisa/ajuste editorial.

## Desempenho observado separado

`observed_performance.snapshots` é opcional. Cada snapshot exige `observed_at` ISO-8601 com fuso e aceita contagens inteiras não negativas ou `null` em `views`, `likes`, `comments`, `shares` e `saves`. Sem métricas conhecidas, retornar `desempenho_desconhecido`; com contagens, `tracao_observada_sem_base`.

Preservar os snapshots e `comparison_cohort`, mas não validar comparabilidade de coortes nem inferir “viral observado”, retenção, velocidade ou aceleração. Um rótulo de entrada não é confirmação e será substituído. Contagens nunca entram na nota nem no desempate editorial. Contagem zero é um dado observado; ausência é `null`.

## Ponte para o plano de edição

Usar `selected_candidate_id` para localizar o candidato original. Copiar os campos compatíveis de fonte, intervalo, contexto, potencial e desempenho para `candidate` em [plano.example.json](../templates/plano.example.json). Registrar `selection_reason` com as evidências que motivaram a escolha. Preencher narrativa, montagem e QA em seguida; o ranking não é um plano pronto nem uma revisão de mídia. Preservar evidências adicionais e consultas no registro da descoberta.

Guardar JSONs de trabalhos reais fora do Git, conforme as regras de mídia e privacidade do projeto.

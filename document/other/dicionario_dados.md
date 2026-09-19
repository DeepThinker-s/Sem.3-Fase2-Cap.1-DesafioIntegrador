# Dicionário de dados

## Ontologia de sintomas

Arquivo: `src/database/ontologia_sintomas.csv`.

| Campo | Descrição |
|---|---|
| `sintoma_id` | Identificador estável e sem acentos |
| `sintoma_principal` | Nome legível do sintoma |
| `sinonimos` | Expressões equivalentes separadas por `|` |
| `doenca_associada` | Possível associação usada na simulação |
| `risco_sugerido` | Classe de prioridade ligada à entrada |
| `justificativa` | Explicação curta da associação |

## Dataset de risco

Arquivo: `src/database/relatos_risco.csv`.

| Campo | Descrição |
|---|---|
| `frase` | Relato clínico sintético e sem dados pessoais |
| `situacao` | Rótulo binário: `baixo_risco` ou `alto_risco` |

Os 60 relatos foram escritos para fins acadêmicos e divididos igualmente entre
as duas classes. Eles não são prontuários e não representam prevalência clínica.

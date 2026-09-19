# Plano para aprovação — CardioAI Fase 2

> Status: plano executado. Manter este arquivo apenas durante a validação interna e removê-lo antes da entrega, se não houver mais necessidade.

## Resumo da entrega proposta

A entrega principal seguirá estritamente o enunciado antes de incluir desafios
opcionais. A CardioAI receberá relatos clínicos sintéticos, reconhecerá sintomas
por uma ontologia simples, exibirá a justificativa da sugestão e classificará o
risco com TF-IDF e aprendizado supervisionado.

### Parte 1 — regras e ontologia

- `docs/frases_sintomas.txt`: pelo menos 10 relatos completos e variados,
  informando o sintoma, quando ocorre e impacto na rotina.
- `src/database/ontologia_sintomas.csv`: relações rastreáveis entre sintomas e
  doenças associadas.
- código Python para normalizar texto, identificar sintomas e apresentar uma
  sugestão assistida, sem se declarar diagnóstico médico.
- testes para acentos, maiúsculas, negação e relatos sem correspondência.

### Parte 2 — classificação de risco

- `src/database/relatos_risco.csv`: relatos sintéticos com rótulos `baixo_risco`
  e `alto_risco`, com origem e caráter sintético documentados.
- `notebooks/cardioai_classificacao_risco.ipynb`: análise, divisão estratificada,
  TF-IDF, treino, avaliação e análise de erros/limitações.
- comparação enxuta de modelos simples; escolha baseada em métricas geradas na
  execução, com prioridade clínica discutida para recall da classe de alto risco.
- semente fixa e pipeline sem vazamento entre treino e teste.

### Documentação e demonstração

- README com instalação, execução, estrutura, limitações e links públicos reais.
- relatório em `document/ai_project_document_fiap.md`, seguindo o template FIAP.
- repositório público criado em
  `https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador`;
- vídeo não listado de até quatro minutos, gravado somente após a versão final.

## Continuidade com a Fase 1

- Nome oficial: **CardioAI**.
- Grupo preservado: **Grupo 8**, com os três integrantes e professores já
  registrados no README.
- A Fase 1 permanece como fonte de proveniência e contexto; esta fase não
  substituirá os datasets anteriores nem afirmará que relatos sintéticos são
  prontuários reais.
- A exclusão de localização, idade, sexo e outros dados pessoais das imagens é
  uma decisão ética deliberada, discutida pelo grupo para reduzir riscos de
  reidentificação e evitar atalhos demográficos na análise. Essa escolha e suas
  limitações devem ser defendidas no relatório, sem alegar análises demográficas
  que a base não permite realizar.
- A métrica clínica prioritária continuará sendo discutida como sensibilidade
  (recall) para alto risco, sem esconder precisão, F1, matriz de confusão ou
  limitações da amostra.

## Correções necessárias nos materiais de proposta

1. trocar “Grupo 8” por **Grupo 28** e remover os cinco integrantes fictícios;
2. padronizar o nome da solução como **CardioAI**;
3. substituir a árvore improvisada pela estrutura FIAP (`document/`, `src/`,
   `scripts/`, `config/` e `assets/`), estendida apenas por `docs/` e `notebooks/`;
4. remover URLs fictícias do GitHub, YouTube e Drive; links ainda inexistentes
   devem aparecer como pendentes, não como links publicados;
5. retirar métricas pré-preenchidas e selos “10/10”: resultados só serão
   documentados depois de executar o pipeline;
6. implementar validação estratificada de verdade ou não alegar “k=5”;
7. reformular a análise de vieses para explicar que a retirada de atributos
   demográficos foi intencional e que a avaliação se restringe às classes de
   risco `baixo_risco` e `alto_risco`, linguagem, cobertura clínica e falsos
   negativos;
8. tratar o portal React e o MLP de ECG como opcionais. As versões descritas em
   `MELHORIAS.docx` estão incompletas e não atendem integralmente aos desafios
   “Ir Além”.

## Links das fases

- Fase 2, entrega atual: https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador
- Fase 1, atividade anterior: https://github.com/DeepThinker-s/Sem.3-Cap.1-CardioAI

## Decisão solicitada

Se este escopo for aprovado, a ordem recomendada de construção é: dados e
critérios de rotulagem, extrator por regras, testes, notebook de classificação,
relatório, README final e vídeo. Os desafios opcionais ficam para depois da
entrega principal estar reproduzível e validada.

<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="30%">

# AI Project Document - Módulo 1 - FIAP

## Grupo 8 - CardioAI

### Integrantes

- André Pessoa Gaidzakian - RM 567877
- Guilherme Ferreira Santos - RM 568523
- Viviane de Castro Silva - RM 567367

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A Inteligência Artificial aplicada à saúde pode organizar textos clínicos,
identificar padrões e apoiar processos de triagem. Relatos escritos apresentam
variações de vocabulário, acentuação, intensidade e negação; por isso, mesmo uma
solução educacional precisa tornar explícitas suas regras, dados e limitações.

Este projeto dá continuidade à Fase 1 da CardioAI, na qual o Grupo 8 pesquisou e
documentou fontes de dados cardiovasculares. A Fase 2 concentra-se em
Processamento de Linguagem Natural, classificação supervisionada e análise
responsável de vieses, conforme o Desafio Integrador da FIAP.

### 1.1.2. Descrição da Solução Desenvolvida

A CardioAI simula apoio à triagem cardiovascular a partir de relatos escritos.
A Parte 1 compara dez relatos sintéticos com uma ontologia de sintomas,
expressões equivalentes e doenças associadas. A Parte 2 transforma frases com
TF-IDF e compara classificadores para indicar `baixo_risco` ou `alto_risco`.

As associações permanecem rastreáveis e todas as saídas informam que o uso é
exclusivamente educacional. A solução não produz diagnóstico médico, não
substitui profissionais de saúde e não deve orientar decisões clínicas.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

- criar dez relatos completos, variados e sem dados pessoais;
- estruturar um mapa de conhecimento rastreável;
- extrair sintomas considerando acentos, caixa, pontuação e negações simples;
- criar e validar um dataset textual binário;
- aplicar TF-IDF e comparar modelos supervisionados sem vazamento de dados;
- avaliar acurácia, precisão, recall, F1, erros e limitações;
- disponibilizar uma execução simples e reproduzível.

## 2.2. Público-Alvo

O projeto destina-se à avaliação acadêmica da FIAP e ao aprendizado de
estudantes de Inteligência Artificial. Ele não foi desenvolvido para pacientes,
profissionais de saúde ou utilização em serviços clínicos.

## 2.3. Metodologia

Foram redigidos dez relatos sintéticos contendo sintoma, período aproximado e
impacto na rotina. Em seguida, foi construída uma ontologia CSV com conceitos,
sinônimos, doença associada, risco sugerido e justificativa.

Para a classificação, foram produzidos 60 relatos sintéticos e únicos, sendo 30
por classe. Uma divisão estratificada reservou 20% para o teste final. Nos 80%
restantes, validação cruzada estratificada com cinco partições comparou Regressão
Logística, SVM Linear e Naive Bayes Complementar. A vetorização TF-IDF foi
encapsulada no mesmo `Pipeline` de cada modelo para impedir que informações do
teste participassem do treinamento.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

- Python 3.12;
- pandas para leitura e validação das bases;
- scikit-learn para TF-IDF, modelos e métricas;
- matplotlib para visualizações do notebook;
- Jupyter e nbconvert para análise reproduzível;
- pytest para testes automatizados;
- GitHub Actions para validação contínua.

As versões compatíveis estão declaradas em `requirements.txt` e
`pyproject.toml`.

## 3.2. Modelagem e Algoritmos

### Extração baseada em ontologia

O módulo `cardioai.texto` remove acentos, normaliza caixa e pontuação e preserva
limites de palavras. O `AnalisadorSintomas` carrega a ontologia, registra
sintomas encontrados e negados e agrupa evidências por doença associada. As
associações de alto risco e com mais evidências aparecem primeiro.

### Classificação supervisionada

O TF-IDF utiliza minúsculas, remoção de acentos, unigramas, bigramas e frequência
sublinear. Foram comparados:

- Regressão Logística com balanceamento de classes;
- SVM Linear com balanceamento de classes;
- Naive Bayes Complementar.

O modelo é selecionado pelo maior recall médio de `alto_risco`, seguido por F1
macro e acurácia. Essa regra prioriza a redução de falsos negativos sem ocultar
as demais métricas.

## 3.3. Treinamento e Teste

O dataset contém 60 frases: 30 `baixo_risco` e 30 `alto_risco`. A divisão
treino-teste usa `random_state=42`, estratificação e 20% dos registros para teste.
A validação cruzada de cinco partições é executada apenas nos dados de treino.

| Modelo | Acurácia média | Precisão alto risco | Recall alto risco | F1 macro |
|---|---:|---:|---:|---:|
| Naive Bayes Complementar | 0,753 | 0,696 | 0,880 | 0,749 |
| Regressão Logística | 0,771 | 0,743 | 0,840 | 0,769 |
| SVM Linear | 0,729 | 0,700 | 0,790 | 0,728 |

O Naive Bayes Complementar foi selecionado pelo maior recall médio de alto
risco. O teste reservado contém 12 frases e não participa dessa seleção.

## 3.4. Governança de Dados, Ética e Vieses

Todos os relatos e rótulos desta fase são sintéticos e foram criados pelo grupo.
Não há prontuários ou dados pessoais. O Grupo 8 decidiu deliberadamente não
associar localização, idade, sexo ou outros identificadores às imagens e aos
relatos. A escolha reduz riscos de reidentificação e dificulta o uso de atalhos
demográficos, mas impede avaliar disparidades entre esses grupos.

A ausência desses atributos não é um esquecimento: foi uma decisão discutida e
documentada. O projeto não reivindica equidade demográfica e restringe sua
análise ao equilíbrio entre classes de risco, diversidade linguística, cobertura
de sintomas e falsos negativos.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

No teste reservado, o modelo selecionado alcançou:

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,917 |
| Precisão de alto risco | 1,000 |
| Recall de alto risco | 0,833 |
| F1 de alto risco | 0,909 |

A matriz de confusão, na ordem `baixo_risco`, `alto_risco`, foi `[[6, 0], [1,
5]]`: onze acertos e um falso negativo de alto risco. O resultado confirma o
funcionamento técnico, mas não representa eficácia clínica. O teste contém
somente 12 exemplos sintéticos, portanto cada erro altera as métricas de forma
relevante.

Dez testes automatizados verificam normalização, limites de palavra, negação,
ausência de correspondência, priorização, esquema e equilíbrio do dataset,
treinamento e formato das métricas. O notebook foi salvo com todas as células
executadas e sem saídas de erro.

## 4.2. Feedback dos Usuários

Não foi conduzido teste com pacientes, profissionais de saúde ou usuários
externos, pois a solução é exclusivamente acadêmica e não clínica. A avaliação
realizada foi técnica e interna: revisão dos relatos pelo grupo, execução dos
scripts, testes automatizados e conferência das métricas. Não são apresentados
depoimentos ou feedbacks fictícios.

Como melhoria futura, qualquer avaliação com profissionais deverá ocorrer com
protocolo ético, escopo educacional explícito e dados devidamente autorizados.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

A implementação atingiu os objetivos acadêmicos: organizou relatos e
conhecimento, produziu associações explicáveis, aplicou TF-IDF, treinou e testou
classificadores e analisou erros e limitações. Seus principais pontos fortes são
a rastreabilidade, a execução reproduzível e a documentação da decisão ética
sobre dados demográficos.

As principais limitações são a base pequena e sintética, a ausência de revisão
clínica dos rótulos e a inexistência de validação externa. Palavras como
“desmaio”, “leve” ou “repouso” podem funcionar como atalhos linguísticos.

Trabalhos futuros incluem revisão dos relatos por especialista, expansão do
dataset, testes com textos mais variados, análise sistemática de falsos
negativos, calibração do risco e validação externa antes de qualquer hipótese de
uso além do ambiente acadêmico.

# <a name="c6"></a>6. Referências

- [CardioAI - Fase 2](https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador)
- [CardioAI - Fase 1](https://github.com/DeepThinker-s/Sem.3-Cap.1-CardioAI)
- [UCI Heart Disease Dataset](https://archive.ics.uci.edu/dataset/45/heart+disease)
- [Diretriz Brasileira de Prevenção Cardiovascular 2019](https://www.scielo.br/j/abc/a/SMSYpcnccSgRnFCtfkKYTcp/?lang=pt)
- [scikit-learn - TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn - avaliação de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html)

# <a name="c7"></a>Anexos

- `document/other/frases_sintomas.txt`: dez relatos clínicos sintéticos;
- `src/database/ontologia_sintomas.csv`: mapa de conhecimento;
- `src/database/relatos_risco.csv`: dataset rotulado;
- `src/notebooks/cardioai_classificacao_risco.ipynb`: classificação e avaliação;
- `document/other/dicionario_dados.md`: definição dos campos;
- `document/other/etica_e_vieses.md`: decisão ética e limitações.

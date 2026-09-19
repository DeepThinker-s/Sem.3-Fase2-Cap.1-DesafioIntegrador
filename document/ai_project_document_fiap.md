# CardioAI - Diagnóstico Automatizado

## 1. Introdução

### 1.1 Contexto e problema

A CardioAI é uma solução acadêmica desenvolvida pelo Grupo 8 para a série de
projetos integradores da FIAP. A Fase 1 reuniu e documentou fontes de dados
cardiovasculares. A Fase 2 avança para uma simulação de apoio à triagem baseada
em relatos escritos, combinando regras explicáveis e aprendizado supervisionado.

Relatos livres apresentam variações de vocabulário, acentuação e negação. Um
sistema básico precisa reconhecer essas variações, manter a justificativa de
cada associação e distinguir relatos potencialmente urgentes dos menos graves.

### 1.2 Solução proposta

A solução possui duas partes complementares. A primeira compara os relatos com
uma ontologia simples de sintomas e doenças associadas. A segunda utiliza TF-IDF
e classificadores do scikit-learn para estimar as classes `baixo_risco` e
`alto_risco`. Ambas são simulações educacionais e não diagnósticos médicos.

## 2. Visão geral

### 2.1 Objetivos

- criar dez relatos completos, variados e sem dados pessoais;
- estruturar um mapa de conhecimento rastreável;
- extrair sintomas, inclusive diante de acentos, maiúsculas e negações simples;
- criar e validar um dataset textual binário;
- comparar modelos simples com TF-IDF sem vazamento entre treino e teste;
- avaliar acurácia, precisão, recall, F1, erros e limitações.

### 2.2 Público-alvo

O projeto destina-se à avaliação acadêmica e ao aprendizado de estudantes de IA.
Não foi projetado para pacientes, profissionais ou uso em serviços de saúde.

### 2.3 Metodologia

Foram escritos dez relatos sintéticos com sintoma, duração e impacto na rotina.
A ontologia contém 21 conceitos, sinônimos, possível doença associada, risco e
justificativa. O extrator normaliza texto com a biblioteca padrão, busca termos
como palavras completas e identifica negações em uma janela anterior à expressão.

Para classificação, foram escritos 60 relatos sintéticos e únicos: 30 por classe.
Uma divisão estratificada reservou 20% para teste. Nos 80% restantes, validação
cruzada estratificada com cinco partições comparou Regressão Logística, SVM
Linear e Naive Bayes Complementar. Cada modelo foi encapsulado em um `Pipeline`
com TF-IDF de unigramas e bigramas, impedindo que o vocabulário do teste participe
do ajuste.

## 3. Tecnologias, modelagem e treinamento

### 3.1 Tecnologias

- Python 3.12;
- pandas 3.0.5;
- scikit-learn 1.9.1;
- matplotlib 3.11.2;
- Jupyter/nbconvert para o notebook;
- pytest para testes automatizados;
- GitHub Actions para validação contínua.

### 3.2 Preparação e proveniência dos dados

Os relatos e rótulos desta fase são inteiramente sintéticos e foram criados pelo
grupo para o experimento. Não contêm prontuários nem dados pessoais. O dicionário
de dados está em `document/other/dicionario_dados.md`.

Por decisão ética deliberada, as imagens herdadas do planejamento da Fase 1 não
são associadas a localização, idade, sexo ou outros identificadores. A escolha
reduz reidentificação e atalhos demográficos, mas impede medir disparidades por
esses grupos. O projeto não reivindica equidade demográfica e avalia somente o
que os dados permitem: classes de risco, linguagem, cobertura e falsos negativos.

### 3.3 Extração de sintomas por regras

O módulo `cardioai.texto` remove acentos, normaliza caixa e pontuação e preserva
limites de palavra. O `AnalisadorSintomas` carrega a ontologia CSV, registra
sintomas encontrados e negados e agrupa evidências por doença associada. As
sugestões de alto risco e com mais evidências aparecem primeiro. Todas as saídas
incluem aviso de uso educacional.

Na execução com os dez relatos, todos produziram pelo menos um sintoma e uma
associação. Um exemplo com “não apresentei dor no peito” registrou a expressão
como negada e não a utilizou como evidência positiva.

### 3.4 Vetorização e modelos

O TF-IDF utiliza minúsculas, remoção de acentos, unigramas, bigramas e frequência
sublinear. O modelo é selecionado pelo maior recall médio de `alto_risco`, seguido
por F1 macro e acurácia. Essa regra prioriza a redução de falsos negativos sem
ocultar as demais métricas.

## 4. Resultados e feedback

### 4.1 Validação cruzada

| Modelo | Acurácia média | Precisão alto risco | Recall alto risco | F1 macro |
|---|---:|---:|---:|---:|
| Naive Bayes Complementar | 0,753 | 0,696 | 0,880 | 0,749 |
| Regressão Logística | 0,771 | 0,743 | 0,840 | 0,769 |
| SVM Linear | 0,729 | 0,700 | 0,790 | 0,728 |

O Naive Bayes Complementar foi selecionado por apresentar o maior recall médio
de alto risco, embora a Regressão Logística tenha maior acurácia e F1 médias.

### 4.2 Teste reservado

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,917 |
| Precisão de alto risco | 1,000 |
| Recall de alto risco | 0,833 |
| F1 de alto risco | 0,909 |

A matriz `[[6, 0], [1, 5]]`, na ordem `baixo_risco`, `alto_risco`, mostra onze
acertos e um falso negativo de alto risco. Esse erro confirma que a saída não
deve ser usada para decisões clínicas.

### 4.3 Verificação técnica

Dez testes automatizados validaram normalização, limites de palavra, negação,
ausência de correspondência, priorização, esquema e equilíbrio do dataset,
treinamento e formato das métricas. Os scripts e o notebook foram executados do
início ao fim.

### 4.4 Distorções e limitações

A base é pequena, balanceada e redigida pelo próprio grupo. Palavras como
“desmaio”, “leve” ou “repouso” podem funcionar como atalhos. O teste possui apenas
12 frases, fazendo cada erro alterar as métricas de forma relevante. Não existe
validação externa, revisão clínica dos rótulos ou estimativa de prevalência real.

## 5. Conclusões

A implementação atende ao fluxo técnico solicitado: organiza relatos e
conhecimento, produz associações explicáveis, converte texto com TF-IDF, treina e
testa classificadores e discute erros. A principal evidência de conclusão é a
execução reproduzível acompanhada de testes. O principal risco é interpretar
métricas sintéticas como desempenho clínico; por isso, os limites de uso aparecem
no código, no notebook e na documentação.

Os próximos passos acadêmicos são revisão humana dos relatos e rótulos, gravação
do vídeo de até quatro minutos e publicação dos arquivos no repositório oficial.

## 6. Referências

- [CardioAI - Fase 2, entrega atual](https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador)
- [CardioAI - Fase 1, atividade anterior](https://github.com/DeepThinker-s/Sem.3-Cap.1-CardioAI)
- [UCI Heart Disease Dataset](https://archive.ics.uci.edu/dataset/45/heart+disease)
- [Diretriz Brasileira de Prevenção Cardiovascular 2019](https://www.scielo.br/j/abc/a/SMSYpcnccSgRnFCtfkKYTcp/?lang=pt)
- [scikit-learn - TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn - avaliação de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html)

## 7. Anexos

- `docs/frases_sintomas.txt`;
- `src/database/ontologia_sintomas.csv`;
- `src/database/relatos_risco.csv`;
- `notebooks/cardioai_classificacao_risco.ipynb`;
- `document/other/dicionario_dados.md`;
- `document/other/etica_e_vieses.md`.

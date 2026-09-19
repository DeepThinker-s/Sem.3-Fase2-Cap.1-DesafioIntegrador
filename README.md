![FIAP](assets/logo-fiap.png)

# CardioAI - Diagnóstico Automatizado

Projeto acadêmico do **Desafio Integrador FIAP - Fase 2, Capítulo 1**. A CardioAI
simula apoio à triagem cardiovascular a partir de relatos escritos. A Parte 1
usa uma ontologia rastreável para identificar sintomas e apresentar possíveis
associações. A Parte 2 transforma frases com TF-IDF e compara classificadores
supervisionados para priorizar relatos como `baixo_risco` ou `alto_risco`.

> Uso exclusivamente educacional. O sistema não produz diagnóstico médico e não
> substitui avaliação por profissional de saúde.

## Grupo 8

- André Pessoa Gaidzakian - RM 567877 - [LinkedIn](https://www.linkedin.com/in/andregaidzakian/)
- Guilherme Ferreira Santos - RM 568523 - [LinkedIn](https://www.linkedin.com/in/guilherme-ferreira-santos-94619b23a/)
- Viviane de Castro Silva - RM 567367 - [LinkedIn](https://www.linkedin.com/in/viviane-de-castro-98764656/)

## Professores

- Tutor: Prof. Leonardo Ruiz Orabona - [LinkedIn](https://www.linkedin.com/in/leonardoorabona/)
- Coordenador: Prof. André Godoi, PhD - [LinkedIn](https://www.linkedin.com/in/andregodoichiovato/)

## Entregáveis implementados

- 10 relatos clínicos sintéticos completos em `docs/frases_sintomas.txt`;
- ontologia com 21 sintomas e respectivas expressões equivalentes;
- extrator com normalização de acentos, correspondência por palavras e negação;
- dataset sintético com 60 frases, igualmente dividido entre as classes de risco;
- comparação entre Regressão Logística, SVM Linear e Naive Bayes Complementar;
- notebook executado com TF-IDF, validação cruzada, métricas e análise de erros;
- dez testes automatizados e validação contínua no GitHub Actions.

## Estrutura

```text
.
├── .github/workflows/ci.yml
├── assets/logo-fiap.png
├── config/README.md
├── docs/frases_sintomas.txt
├── document/
│   ├── ai_project_document_fiap.md
│   └── other/
├── notebooks/cardioai_classificacao_risco.ipynb
├── scripts/run_checks.ps1
├── src/
│   ├── cardioai/
│   ├── database/
│   ├── extrair_diagnosticos.py
│   └── treinar_classificador.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── LICENSE
```

## Instalação

Use Python 3.10 ou superior. No Windows, prefira clonar o projeto em um caminho
curto, como `C:\Projetos`, para evitar a limitação de caminhos longos.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Como executar

Parte 1 - extração de sintomas e associações:

```powershell
python src/extrair_diagnosticos.py
```

Parte 2 - treinamento e avaliação:

```powershell
python src/treinar_classificador.py
```

Notebook executável:

```powershell
python -m nbconvert --to notebook --execute --inplace notebooks/cardioai_classificacao_risco.ipynb
```

Validação completa no Windows:

```powershell
.\scripts\run_checks.ps1
```

## Resultados reproduzidos

O dataset tem 60 relatos sintéticos: 30 `baixo_risco` e 30 `alto_risco`. A
seleção usa validação cruzada estratificada com cinco partições somente no
conjunto de treinamento. O Naive Bayes Complementar obteve o maior recall médio
de alto risco nessa etapa (`0,880`) e foi selecionado.

No teste reservado de 12 frases, o modelo alcançou:

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,917 |
| Precisão de alto risco | 1,000 |
| Recall de alto risco | 0,833 |
| F1 de alto risco | 0,909 |

A matriz de confusão, na ordem `baixo_risco`, `alto_risco`, foi `[[6, 0], [1,
5]]`: um relato de alto risco foi classificado incorretamente como baixo risco.
Como o teste tem apenas 12 exemplos e todos os dados são sintéticos, as métricas
demonstram funcionamento técnico, não eficácia clínica.

## Ética, privacidade e limitações

O grupo decidiu deliberadamente não associar localização, idade, sexo ou outros
dados pessoais às imagens e relatos. A decisão reduz riscos de reidentificação e
atalhos demográficos, mas também impede avaliar disparidades entre esses grupos.
Por isso, a análise se limita ao equilíbrio entre `baixo_risco` e `alto_risco`,
diversidade linguística, cobertura de sintomas e falsos negativos. Consulte
`document/other/etica_e_vieses.md` para a justificativa completa.

## Links públicos

- Fase 2 - entrega atual: [repositório oficial](https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador)
- Fase 1 - atividade anterior: [repositório histórico](https://github.com/DeepThinker-s/Sem.3-Cap.1-CardioAI)
- Vídeo de demonstração: **pendente de gravação e publicação como não listado**

## Licença

Código distribuído sob a [Licença MIT](LICENSE). Bases externas mantêm suas
próprias licenças e condições de uso.

## Histórico de versões

- `0.2.0` - Partes 1 e 2 implementadas e validadas localmente.
- `0.1.0` - Estrutura e plano inicial.

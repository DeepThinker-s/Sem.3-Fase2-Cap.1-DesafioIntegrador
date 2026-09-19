# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>

# CardioAI - Diagnóstico Automatizado

## Grupo 8

## 👨‍🎓 Integrantes

- [André Pessoa Gaidzakian](https://www.linkedin.com/in/andregaidzakian/) - RM 567877
- [Guilherme Ferreira Santos](https://www.linkedin.com/in/guilherme-ferreira-santos-94619b23a/) - RM 568523
- [Viviane de Castro Silva](https://www.linkedin.com/in/viviane-de-castro-98764656/) - RM 567367

## 👩‍🏫 Professores

### Tutor

- [Prof. Leonardo Ruiz Orabona](https://www.linkedin.com/in/leonardoorabona/)

### Coordenador

- [Prof. André Godoi, PhD](https://www.linkedin.com/in/andregodoichiovato/)

## 📜 Descrição

A CardioAI é a entrega do Desafio Integrador FIAP - Fase 2, Capítulo 1. O
projeto simula apoio à triagem cardiovascular a partir de relatos escritos e é
dividido em duas partes. Na primeira, dez relatos clínicos sintéticos são
comparados com uma ontologia rastreável de sintomas, expressões equivalentes e
doenças associadas. Na segunda, um dataset textual balanceado é transformado com
TF-IDF e usado para comparar classificadores supervisionados capazes de indicar
`baixo_risco` ou `alto_risco`.

O sistema foi desenvolvido para fins acadêmicos, com regras explicáveis,
validação automatizada e análise explícita de limitações. Ele não produz
diagnóstico médico, não substitui profissionais de saúde e não deve orientar
decisões clínicas.

## 📦 Entregáveis implementados

- 10 relatos completos em `document/other/frases_sintomas.txt`;
- ontologia com 21 conceitos em `src/database/ontologia_sintomas.csv`;
- extrator de sintomas e associações por regras;
- dataset com 60 frases, igualmente dividido entre as classes de risco;
- comparação entre Regressão Logística, SVM Linear e Naive Bayes Complementar;
- notebook executado com TF-IDF, validação cruzada, métricas e análise de erros;
- 10 testes automatizados e validação contínua pelo GitHub Actions.

## 📁 Estrutura de pastas

- `.github`: automação de testes e orientações para relatos de problemas.
- `assets`: elementos visuais, incluindo o logotipo da FIAP.
- `config`: informações de configuração e requisitos do ambiente.
- `document`: documento principal exigido pelo template FIAP.
- `document/other`: relatos clínicos, dicionário de dados e documentação ética.
- `scripts`: script auxiliar para executar toda a validação no Windows.
- `src`: código-fonte, bases CSV e notebook da solução.
- `tests`: testes automatizados da extração e classificação.
- `README.md`: guia geral de instalação, execução e resultados.

```text
.
├── .github/
│   └── workflows/ci.yml
├── assets/
│   └── logo-fiap.png
├── config/
│   └── README.md
├── document/
│   ├── ai_project_document_fiap.md
│   └── other/
│       ├── dicionario_dados.md
│       ├── etica_e_vieses.md
│       └── frases_sintomas.txt
├── scripts/
│   └── run_checks.ps1
├── src/
│   ├── cardioai/
│   ├── database/
│   ├── notebooks/
│   │   └── cardioai_classificacao_risco.ipynb
│   ├── extrair_diagnosticos.py
│   └── treinar_classificador.py
├── tests/
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.10 ou superior;
- Git para clonar o repositório;
- PowerShell para executar o fluxo completo no Windows.

No Windows, prefira um caminho curto, como `C:\Projetos`, para evitar a
limitação de caminhos longos.

```powershell
git clone https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador.git
cd Sem.3-Fase2-Cap.1-DesafioIntegrador
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

### Parte 1 - extração de sintomas

```powershell
python src/extrair_diagnosticos.py
```

### Parte 2 - treinamento e avaliação

```powershell
python src/treinar_classificador.py
```

### Notebook

```powershell
python -m nbconvert --to notebook --execute --inplace src/notebooks/cardioai_classificacao_risco.ipynb
```

### Validação completa no Windows

```powershell
.\scripts\run_checks.ps1
```

## 📊 Resultados reproduzidos

O dataset possui 30 relatos `baixo_risco` e 30 `alto_risco`. A seleção usa
validação cruzada estratificada com cinco partições somente no conjunto de
treinamento. O Naive Bayes Complementar obteve o maior recall médio de alto
risco (`0,880`) e foi selecionado.

| Métrica no teste reservado | Resultado |
|---|---:|
| Acurácia | 0,917 |
| Precisão de alto risco | 1,000 |
| Recall de alto risco | 0,833 |
| F1 de alto risco | 0,909 |

A matriz de confusão, na ordem `baixo_risco`, `alto_risco`, foi `[[6, 0], [1,
5]]`. Como o teste contém apenas 12 exemplos sintéticos, os resultados comprovam
o funcionamento técnico, não eficácia clínica.

## ⚖️ Ética, privacidade e limitações

O Grupo 8 decidiu deliberadamente não associar localização, idade, sexo ou
outros dados pessoais às imagens e aos relatos. Essa decisão reduz riscos de
reidentificação e de atalhos demográficos, mas impede medir disparidades entre
esses grupos. A análise se limita ao equilíbrio entre classes de risco,
diversidade linguística, cobertura de sintomas e falsos negativos. Consulte
`document/other/etica_e_vieses.md` para a justificativa completa.

## 🔗 Repositório oficial e links públicos

- Fase 2: [repositório oficial](https://github.com/DeepThinker-s/Sem.3-Fase2-Cap.1-DesafioIntegrador)
- Fase 1: [atividade anterior](https://github.com/DeepThinker-s/Sem.3-Cap.1-CardioAI)
- Vídeo de demonstração no YouTube: **pendente de gravação e publicação como não listado**

## 🗃 Histórico de lançamentos

- `0.2.1` - 19/09/2026
  - adequação integral da estrutura e documentação ao template FIAP;
  - padronização para Grupo 8 e remoção de pastas documentais duplicadas.
- `0.2.0` - 19/09/2026
  - Partes 1 e 2 implementadas, testadas e publicadas.
- `0.1.0` - 13/09/2026
  - estrutura inicial e planejamento da entrega.

## 📋 Licença

Código distribuído sob a [Licença MIT](LICENSE). Bases externas mantêm suas
próprias licenças e condições de uso.

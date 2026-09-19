"""Treinamento reproduzível do classificador textual de risco."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

ROTULOS = ("baixo_risco", "alto_risco")
SEMENTE = 42


@dataclass
class ResultadoTreinamento:
    modelo_nome: str
    modelo: Pipeline
    comparacao_cv: pd.DataFrame
    metricas_teste: dict[str, float]
    matriz_confusao: list[list[int]]
    y_teste: pd.Series
    y_previsto: list[str]
    frases_teste: pd.Series


def carregar_dataset(caminho: str | Path) -> pd.DataFrame:
    dados = pd.read_csv(caminho)
    if list(dados.columns) != ["frase", "situacao"]:
        raise ValueError("O dataset deve conter exatamente as colunas frase e situacao.")
    if dados.isna().any().any() or (dados["frase"].str.strip() == "").any():
        raise ValueError("O dataset contém valores ausentes ou frases vazias.")
    if set(dados["situacao"]) != set(ROTULOS):
        raise ValueError("Os rótulos devem ser baixo_risco e alto_risco.")
    if dados["frase"].duplicated().any():
        raise ValueError("O dataset contém frases duplicadas.")
    return dados


def _pipeline(modelo: BaseEstimator) -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            ("modelo", modelo),
        ]
    )


def modelos_candidatos() -> dict[str, Pipeline]:
    return {
        "Regressão Logística": _pipeline(
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=SEMENTE)
        ),
        "SVM Linear": _pipeline(LinearSVC(class_weight="balanced", random_state=SEMENTE)),
        "Naive Bayes Complementar": _pipeline(ComplementNB()),
    }


def comparar_modelos(frases: pd.Series, rotulos: pd.Series) -> pd.DataFrame:
    validacao = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    pontuacoes = {
        "acuracia": "accuracy",
        "precisao_alto": make_scorer(
            precision_score, pos_label="alto_risco", zero_division=0
        ),
        "recall_alto": make_scorer(
            recall_score, pos_label="alto_risco", zero_division=0
        ),
        "f1_macro": "f1_macro",
    }
    linhas = []
    for nome, modelo in modelos_candidatos().items():
        resultado = cross_validate(modelo, frases, rotulos, cv=validacao, scoring=pontuacoes)
        linhas.append(
            {
                "modelo": nome,
                **{
                    metrica: float(resultado[f"test_{metrica}"].mean())
                    for metrica in pontuacoes
                },
            }
        )
    return pd.DataFrame(linhas).sort_values(
        ["recall_alto", "f1_macro", "acuracia"], ascending=False
    ).reset_index(drop=True)


def treinar_e_avaliar(dados: pd.DataFrame, tamanho_teste: float = 0.2) -> ResultadoTreinamento:
    treino_x, teste_x, treino_y, teste_y = train_test_split(
        dados["frase"],
        dados["situacao"],
        test_size=tamanho_teste,
        stratify=dados["situacao"],
        random_state=SEMENTE,
    )
    comparacao = comparar_modelos(treino_x, treino_y)
    melhor_nome = str(comparacao.iloc[0]["modelo"])
    melhor_modelo = modelos_candidatos()[melhor_nome]
    melhor_modelo.fit(treino_x, treino_y)
    previsto = list(melhor_modelo.predict(teste_x))

    metricas = {
        "acuracia": float(accuracy_score(teste_y, previsto)),
        "precisao_alto_risco": float(
            precision_score(teste_y, previsto, pos_label="alto_risco", zero_division=0)
        ),
        "recall_alto_risco": float(
            recall_score(teste_y, previsto, pos_label="alto_risco", zero_division=0)
        ),
        "f1_alto_risco": float(
            f1_score(teste_y, previsto, pos_label="alto_risco", zero_division=0)
        ),
    }
    matriz = confusion_matrix(teste_y, previsto, labels=list(ROTULOS)).tolist()
    return ResultadoTreinamento(
        modelo_nome=melhor_nome,
        modelo=melhor_modelo,
        comparacao_cv=comparacao,
        metricas_teste=metricas,
        matriz_confusao=matriz,
        y_teste=teste_y,
        y_previsto=previsto,
        frases_teste=teste_x,
    )

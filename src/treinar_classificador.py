"""Treina os modelos da Parte 2 e salva um resumo reproduzível."""

from __future__ import annotations

import json
from pathlib import Path

import joblib

from cardioai.classificador import carregar_dataset, treinar_e_avaliar


RAIZ = Path(__file__).resolve().parents[1]


def main() -> None:
    caminho_dados = RAIZ / "src" / "database" / "relatos_risco.csv"
    pasta_saida = RAIZ / "outputs"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    dados = carregar_dataset(caminho_dados)
    resultado = treinar_e_avaliar(dados)
    resumo = {
        "quantidade_registros": len(dados),
        "distribuicao_classes": dados["situacao"].value_counts().to_dict(),
        "modelo_selecionado": resultado.modelo_nome,
        "comparacao_validacao_cruzada": resultado.comparacao_cv.to_dict(orient="records"),
        "metricas_teste": resultado.metricas_teste,
        "matriz_confusao": resultado.matriz_confusao,
        "ordem_matriz": ["baixo_risco", "alto_risco"],
    }
    (pasta_saida / "metricas_classificador.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    joblib.dump(resultado.modelo, pasta_saida / "classificador_risco.joblib")
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

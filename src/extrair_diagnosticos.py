"""Executa a Parte 1 para todos os relatos do arquivo de entrada."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cardioai.extractor import AnalisadorSintomas


RAIZ = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Análise educacional de relatos clínicos")
    parser.add_argument("--frases", type=Path, default=RAIZ / "docs" / "frases_sintomas.txt")
    parser.add_argument(
        "--ontologia", type=Path, default=RAIZ / "src" / "database" / "ontologia_sintomas.csv"
    )
    parser.add_argument("--saida", type=Path, default=RAIZ / "outputs" / "analises_sintomas.json")
    args = parser.parse_args()

    analisador = AnalisadorSintomas(args.ontologia)
    frases = [linha.strip() for linha in args.frases.read_text(encoding="utf-8").splitlines() if linha.strip()]
    resultados = []
    for indice, frase in enumerate(frases, start=1):
        analise = analisador.analisar(frase)
        resultados.append(
            {
                "id": f"P{indice:02d}",
                "relato": analise.relato,
                "sintomas_encontrados": [s.sintoma_id for s in analise.sintomas],
                "sintomas_negados": list(analise.sintomas_negados),
                "sugestoes": list(analise.sugestoes),
                "aviso": analise.aviso,
            }
        )

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(resultados)} relatos analisados. Resultado salvo em {args.saida}")


if __name__ == "__main__":
    main()

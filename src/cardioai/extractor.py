"""Extração explicável de sintomas a partir da ontologia da CardioAI."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .texto import esta_negada, localizar_expressoes, normalizar


@dataclass(frozen=True)
class SintomaEncontrado:
    sintoma_id: str
    expressao: str
    doenca_associada: str
    risco_sugerido: str
    justificativa: str


@dataclass(frozen=True)
class ResultadoAnalise:
    relato: str
    sintomas: tuple[SintomaEncontrado, ...]
    sintomas_negados: tuple[str, ...]
    sugestoes: tuple[dict[str, object], ...]
    aviso: str = (
        "Simulação educacional: as associações não constituem diagnóstico e "
        "não substituem avaliação por profissional de saúde."
    )


class AnalisadorSintomas:
    """Reconhece sintomas e os relaciona às doenças registradas na ontologia."""

    def __init__(self, caminho_ontologia: str | Path):
        self.caminho_ontologia = Path(caminho_ontologia)
        self.entradas = self._carregar_ontologia()

    def _carregar_ontologia(self) -> list[dict[str, str]]:
        with self.caminho_ontologia.open(encoding="utf-8-sig", newline="") as arquivo:
            entradas = list(csv.DictReader(arquivo))
        campos = {
            "sintoma_id",
            "sintoma_principal",
            "sinonimos",
            "doenca_associada",
            "risco_sugerido",
            "justificativa",
        }
        if not entradas or not campos.issubset(entradas[0]):
            raise ValueError("A ontologia está vazia ou não contém as colunas obrigatórias.")
        return entradas

    def analisar(self, relato: str) -> ResultadoAnalise:
        texto = normalizar(relato)
        encontrados: dict[str, SintomaEncontrado] = {}
        negados: set[str] = set()

        for entrada in self.entradas:
            expressoes = [entrada["sintoma_principal"], *entrada["sinonimos"].split("|")]
            encontrou_positivo = False
            for expressao in sorted(expressoes, key=len, reverse=True):
                for posicao in localizar_expressoes(texto, expressao):
                    if esta_negada(texto, posicao[0]):
                        negados.add(entrada["sintoma_principal"])
                        continue
                    encontrados[entrada["sintoma_id"]] = SintomaEncontrado(
                        sintoma_id=entrada["sintoma_id"],
                        expressao=expressao,
                        doenca_associada=entrada["doenca_associada"],
                        risco_sugerido=entrada["risco_sugerido"],
                        justificativa=entrada["justificativa"],
                    )
                    encontrou_positivo = True
                    break
                if encontrou_positivo:
                    break

        por_doenca: dict[str, list[SintomaEncontrado]] = defaultdict(list)
        for sintoma in encontrados.values():
            por_doenca[sintoma.doenca_associada].append(sintoma)

        sugestoes = []
        for doenca, sintomas in por_doenca.items():
            risco = "alto_risco" if any(s.risco_sugerido == "alto_risco" for s in sintomas) else "baixo_risco"
            sugestoes.append(
                {
                    "doenca_associada": doenca,
                    "risco_sugerido": risco,
                    "quantidade_evidencias": len(sintomas),
                    "sintomas": [s.sintoma_id for s in sintomas],
                }
            )
        sugestoes.sort(
            key=lambda item: (item["risco_sugerido"] == "alto_risco", item["quantidade_evidencias"]),
            reverse=True,
        )

        return ResultadoAnalise(
            relato=relato,
            sintomas=tuple(encontrados.values()),
            sintomas_negados=tuple(sorted(negados)),
            sugestoes=tuple(sugestoes),
        )

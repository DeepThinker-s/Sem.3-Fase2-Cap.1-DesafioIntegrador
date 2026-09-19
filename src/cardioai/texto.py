"""Normalização e busca de expressões clínicas em português."""

from __future__ import annotations

import re
import unicodedata

NEGACOES = {"nao", "nega", "negou", "sem", "nunca", "jamais"}
QUEBRAS_NEGACAO = {"mas", "porem", "contudo", "entretanto"}


def normalizar(texto: str) -> str:
    """Converte texto para uma forma comparável, preservando apenas palavras."""
    decomposicao = unicodedata.normalize("NFKD", texto.casefold())
    sem_acentos = "".join(char for char in decomposicao if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", sem_acentos))


def localizar_expressao(texto_normalizado: str, expressao: str) -> tuple[int, int] | None:
    """Localiza uma expressão como sequência completa de palavras."""
    posicoes = localizar_expressoes(texto_normalizado, expressao)
    return posicoes[0] if posicoes else None


def localizar_expressoes(texto_normalizado: str, expressao: str) -> tuple[tuple[int, int], ...]:
    """Localiza todas as ocorrências de uma expressão como palavras completas."""
    expressao_normalizada = normalizar(expressao)
    padrao = rf"(?<![a-z0-9]){re.escape(expressao_normalizada)}(?![a-z0-9])"
    return tuple(correspondencia.span() for correspondencia in re.finditer(padrao, texto_normalizado))


def esta_negada(texto_normalizado: str, inicio: int, janela: int = 4) -> bool:
    """Detecta negação simples imediatamente antes de uma expressão."""
    trecho = texto_normalizado[:inicio].split()
    contexto = trecho[-janela:]
    if any(palavra in QUEBRAS_NEGACAO for palavra in contexto):
        ultima_quebra = max(
            indice for indice, palavra in enumerate(contexto) if palavra in QUEBRAS_NEGACAO
        )
        contexto = contexto[ultima_quebra + 1 :]
    return any(palavra in NEGACOES for palavra in contexto)

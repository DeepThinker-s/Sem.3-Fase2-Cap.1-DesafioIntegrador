from cardioai.texto import esta_negada, localizar_expressao, normalizar


def test_normalizar_remove_acentos_e_pontuacao():
    assert normalizar("Pressão no TÓRAX!") == "pressao no torax"


def test_busca_respeita_limites_de_palavra():
    assert localizar_expressao("estou sem ar", "sem ar") == (6, 12)
    assert localizar_expressao("palpitacao", "pita") is None


def test_negacao_imediata_e_quebra_de_contexto():
    texto = normalizar("Não sinto dor no peito")
    inicio, _ = localizar_expressao(texto, "dor no peito")
    assert esta_negada(texto, inicio)

    texto_com_quebra = normalizar("Não tive febre, mas sinto dor no peito")
    inicio, _ = localizar_expressao(texto_com_quebra, "dor no peito")
    assert not esta_negada(texto_com_quebra, inicio)

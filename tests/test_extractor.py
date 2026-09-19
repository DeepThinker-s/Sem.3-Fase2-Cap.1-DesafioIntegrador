from pathlib import Path

from cardioai.extractor import AnalisadorSintomas


RAIZ = Path(__file__).resolve().parents[1]
ONTOLOGIA = RAIZ / "src" / "database" / "ontologia_sintomas.csv"


def test_reconhece_sintoma_com_acentos_e_maiusculas():
    resultado = AnalisadorSintomas(ONTOLOGIA).analisar(
        "Estou com PRESSÃO no peito ao esforço e preciso parar."
    )
    assert "dor_peito_esforco" in {s.sintoma_id for s in resultado.sintomas}
    assert resultado.sugestoes[0]["doenca_associada"] == "Angina"


def test_nao_contabiliza_sintoma_negado():
    resultado = AnalisadorSintomas(ONTOLOGIA).analisar(
        "Tenho dor de cabeça, mas não sinto dor no peito ao esforço."
    )
    assert "dor_peito_esforco" not in {s.sintoma_id for s in resultado.sintomas}
    assert "dor no peito ao esforço" in resultado.sintomas_negados


def test_relato_sem_correspondencia_retorna_listas_vazias():
    resultado = AnalisadorSintomas(ONTOLOGIA).analisar("Hoje acordei disposto e sem queixas.")
    assert resultado.sintomas == ()
    assert resultado.sugestoes == ()


def test_prioriza_associacao_de_alto_risco():
    resultado = AnalisadorSintomas(ONTOLOGIA).analisar(
        "Sinto dor no peito em repouso e suor frio desde a madrugada."
    )
    assert resultado.sugestoes[0]["risco_sugerido"] == "alto_risco"


def test_considera_ocorrencia_positiva_depois_de_uma_negada():
    resultado = AnalisadorSintomas(ONTOLOGIA).analisar(
        "Ontem não senti dor no peito ao esforço, mas hoje sinto dor no peito ao esforço."
    )
    assert "dor_peito_esforco" in {s.sintoma_id for s in resultado.sintomas}

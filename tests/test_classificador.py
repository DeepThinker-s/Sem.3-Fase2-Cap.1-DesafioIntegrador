from pathlib import Path

from cardioai.classificador import carregar_dataset, treinar_e_avaliar


RAIZ = Path(__file__).resolve().parents[1]
DATASET = RAIZ / "src" / "database" / "relatos_risco.csv"


def test_dataset_tem_esquema_e_classes_balanceadas():
    dados = carregar_dataset(DATASET)
    assert len(dados) == 60
    assert dados["situacao"].value_counts().to_dict() == {
        "alto_risco": 30,
        "baixo_risco": 30,
    }


def test_pipeline_treina_e_retorna_metricas_validas():
    resultado = treinar_e_avaliar(carregar_dataset(DATASET))
    assert len(resultado.comparacao_cv) == 3
    assert set(resultado.metricas_teste) == {
        "acuracia",
        "precisao_alto_risco",
        "recall_alto_risco",
        "f1_alto_risco",
    }
    assert all(0.0 <= valor <= 1.0 for valor in resultado.metricas_teste.values())
    assert sum(sum(linha) for linha in resultado.matriz_confusao) == 12

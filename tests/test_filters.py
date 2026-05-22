from src.filters import filter_by_min_genes, filter_by_type


# Verifica que filter_by_min_genes conserva solo reguladores
# que regulan al menos el número mínimo de genes especificado.
def test_filter_by_min_genes_filters_correctly():
    regulon = {
        "TF1": {"genes": ["G1", "G2", "G3"], "activados": 2, "reprimidos": 1},
        "TF2": {"genes": ["G4"], "activados": 1, "reprimidos": 0},
    }

    result = filter_by_min_genes(regulon, 2)
    assert "TF1" in result
    assert "TF2" not in result


# Verifica que filter_by_type retorna solo reguladores
# del tipo especificado: activador, represor o dual.
def test_filter_by_type_filters_correctly():
    regulon = {
        "TF1": {"genes": ["G1", "G2"], "activados": 2, "reprimidos": 0},
        "TF2": {"genes": ["G3"], "activados": 0, "reprimidos": 1},
        "TF3": {"genes": ["G4"], "activados": 1, "reprimidos": 1},
    }

    assert "TF1" in filter_by_type(regulon, "activador")
    assert "TF2" in filter_by_type(regulon, "represor")
    assert "TF3" in filter_by_type(regulon, "dual")

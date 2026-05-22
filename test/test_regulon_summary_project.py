import pytest

from src.core import build_regulon
from src.filters import filter_by_min_genes, filter_by_type
from src.io_utils import load_interactions


def test_build_regulon_unique_genes_and_effect_counts():
    interactions = [
        ("TF1", "G1", "+"),
        ("TF1", "G2", "-"),
        ("TF1", "G1", "+"),
        ("TF2", "G3", "+-"),
    ]

    expected = {
        "TF1": {"genes": ["G1", "G2"], "activados": 2, "reprimidos": 1},
        "TF2": {"genes": ["G3"], "activados": 1, "reprimidos": 1},
    }

    assert build_regulon(interactions) == expected


def test_filter_by_min_genes_returns_only_tfs_with_enough_genes():
    regulon = {
        "TF1": {"genes": ["G1", "G2"], "activados": 1, "reprimidos": 0},
        "TF2": {"genes": ["G3"], "activados": 0, "reprimidos": 1},
    }

    assert filter_by_min_genes(regulon, 2) == {"TF1": regulon["TF1"]}
    assert filter_by_min_genes(regulon, 1) == regulon


def test_filter_by_type_filters_tfs_by_regulator_role():
    regulon = {
        "TF1": {"genes": ["G1", "G2"], "activados": 2, "reprimidos": 0},
        "TF2": {"genes": ["G3"], "activados": 0, "reprimidos": 1},
        "TF3": {"genes": ["G4"], "activados": 1, "reprimidos": 1},
    }

    assert filter_by_type(regulon, "activador") == {"TF1": regulon["TF1"]}
    assert filter_by_type(regulon, "represor") == {"TF2": regulon["TF2"]}
    assert filter_by_type(regulon, "dual") == {"TF3": regulon["TF3"]}
    assert filter_by_type(regulon, None) == regulon


def test_load_interactions_reads_only_valid_rows(tmp_path):
    file_path = tmp_path / "interactions.tsv"
    file_path.write_text(
"""# comentario de prueba
1)regulatorId\tregulatorName\tcol3\tcol4\tcol5\tcol6\tcol7
1\ttf1\tC\tD\tgene1\t+\tX
2\ttf1\tC\tD\tgene2\t-\tX
3\ttf2\tC\tD\tgene3\tinvalid\tX
4\ttf2\tC\tD\tgene4\t+-\tX
"""
    )

    interactions = load_interactions(str(file_path))

    assert interactions == [
        ("tf1", "gene1", "+"),
        ("tf1", "gene2", "-"),
        ("tf2", "gene4", "+-"),
    ]


def test_load_interactions_raises_value_error_for_empty_filename():
    with pytest.raises(ValueError):
        load_interactions("")

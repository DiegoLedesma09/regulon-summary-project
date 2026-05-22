import pytest

from src.io_utils import load_interactions


# Verifica que load_interactions carga correctamente las interacciones
# desde un archivo TSV válido y filtra filas incorrectas.
def test_load_interactions_valid_file(tmp_path):
    file_path = tmp_path / "interactions.tsv"
    file_path.write_text(
        "1)regulatorId\tregulatorName\tcol3\tcol4\ttarget\teffect\tcol7\n"
        "1\tTF1\tX\tX\tgeneA\t+\tX\n"
        "2\tTF1\tX\tX\tgeneB\t-\tX\n"
        "3\tTF2\tX\tX\tgeneC\tinvalid\tX\n"
    )

    result = load_interactions(str(file_path))

    assert len(result) == 2
    assert ("TF1", "geneA", "+") in result
    assert ("TF1", "geneB", "-") in result


# Verifica que load_interactions lanza ValueError
# cuando se pasa un nombre de archivo vacío.
def test_load_interactions_raises_error_on_empty_filename():
    with pytest.raises(ValueError, match="filename vacío"):
        load_interactions("")

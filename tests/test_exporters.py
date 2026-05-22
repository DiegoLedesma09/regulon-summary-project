from src.exporters import write_summary, write_sif


# Verifica que write_summary crea un archivo con el resumen
# del regulón en formato TSV con encabezado y datos correctos.
def test_write_summary_creates_file_with_correct_format(tmp_path):
    output_file = tmp_path / "summary.tsv"
    
    regulon = {
        "TF1": {"genes": ["geneA", "geneB"], "activados": 1, "reprimidos": 1},
        "TF2": {"genes": ["geneC"], "activados": 1, "reprimidos": 0},
    }

    write_summary(regulon, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes" in content


# Verifica que write_sif traduce correctamente los efectos
# a términos SIF (activates, represses, regulates).
def test_write_sif_translates_effects(tmp_path):
    output_file = tmp_path / "network.sif"
    
    interactions = [
        ("TF1", "geneA", "+"),
        ("TF1", "geneB", "-"),
        ("TF2", "geneC", "+-"),
    ]

    write_sif(interactions, str(output_file))

    content = output_file.read_text()
    
    assert "TF1\tactivates\tgeneA" in content
    assert "TF1\trepresses\tgeneB" in content
    assert "TF2\tregulates\tgeneC" in content

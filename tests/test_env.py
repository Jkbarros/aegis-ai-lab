"""Sanidade do pacote e ambiente Python."""


def test_import_aegis() -> None:
    from aegis.lab import mensagem_boas_vindas, verificar_versao_python

    assert verificar_versao_python() is True
    assert "Aegis AI Lab" in mensagem_boas_vindas()

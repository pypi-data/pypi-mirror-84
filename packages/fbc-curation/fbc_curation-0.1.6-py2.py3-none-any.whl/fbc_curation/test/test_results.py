"""Testing result."""

import libsbml
import pandas as pd

from fbc_curation import EXAMPLE_PATH
from fbc_curation.constants import CuratorConstants
from fbc_curation.curator import CuratorResults
from fbc_curation.curator.cobrapy_curator import CuratorCobrapy


model_path = EXAMPLE_PATH / "models" / "e_coli_core.xml"
curator = CuratorCobrapy(model_path=model_path)
results = curator.run()
doc = libsbml.readSBMLFromFile(str(model_path))  # type: libsbml.SBMLDocument
model = doc.getModel()  # type: libsbml.Model


def _check_objective(df):
    """Check objective DataFrame."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.OBJECTIVE_FIELDS)
    for field in CuratorConstants.OBJECTIVE_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.OBJECTIVE_FIELDS):
        assert df.columns[k] == field

    obj_value = df["value"].values[0]
    assert obj_value > 0

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_objective():
    """Check objective."""
    df = results.objective
    _check_objective(df)


def _check_fva(df):
    """Check FVA."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.FVA_FIELDS)
    for field in CuratorConstants.FVA_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.FVA_FIELDS):
        assert df.columns[k] == field

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_fva():
    """Check FVA DataFrame."""
    df = results.fva
    _check_fva(df)


def _check_gene_deletion(df):
    """Check gene deletion."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.GENE_DELETION_FIELDS)
    for field in CuratorConstants.GENE_DELETION_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.GENE_DELETION_FIELDS):
        assert df.columns[k] == field

    fbc_model = model.getPlugin("fbc")  # type: libsbml.FbcModelPlugin
    assert len(df) == fbc_model.getNumGeneProducts()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_gene_deletion():
    """Check gene deletion."""
    df = results.gene_deletion
    _check_gene_deletion(df)


def _check_reaction_deletion(df):
    """Check reaction deletion."""
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == len(CuratorConstants.REACTION_DELETION_FIELDS)
    for field in CuratorConstants.REACTION_DELETION_FIELDS:
        assert field in df.columns
    for k, field in enumerate(CuratorConstants.REACTION_DELETION_FIELDS):
        assert df.columns[k] == field

    assert len(df) == model.getNumReactions()

    status_codes = df.status.unique()
    assert len(status_codes) <= 2
    assert "optimal" in status_codes


def test_reaction_deletion(tmp_path):
    """Check reaction deletion."""
    df = results.reaction_deletion
    _check_reaction_deletion(df)


def test_read_write_check1(tmp_path):
    """Test reading/writing of results."""
    results.write_results(tmp_path)
    results2 = CuratorResults.read_results(tmp_path)
    assert CuratorResults.compare({"res1": results, "res2": results2})


def test_read_write_check2(tmp_path):
    """Test reading/writing of results."""
    results.write_results(tmp_path)
    results2 = CuratorResults.read_results(tmp_path)
    assert results2.validate_objective()
    assert results2.validate_fva()
    assert results2.validate_gene_deletion()
    assert results2.validate_reaction_deletion()
    assert results2.validate()

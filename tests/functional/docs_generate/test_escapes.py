import pytest
from dbt.tests.util import run_dbt, get_manifest, rm_file

model_sql = """
select 1 as id
"""


class TestDocsGenerateEscapes:
    @pytest.fixture(scope="class")
    def models(self):
        return {"model.sql": model_sql}

    def test_include_schema(self, project):
        results = run_dbt(["run"])
        assert len(results) == 1
        rm_file(project.project_root, "target", "manifest.json")
        rm_file(project.project_root, "target", "run_results.json")

        run_dbt(["docs", "generate"])
        manifest = get_manifest(project.project_root)
        assert manifest
        assert manifest.nodes
        assert len(manifest.nodes) == 1
        assert "model.test.model" in manifest.nodes
        assert manifest.nodes["model.test.model"].schema == project.test_schema

import pytest
import pathlib
from cincanregistry import HubReadmeHandler
from unittest.mock import mock_open


def test_create_hub_readme_handler(mocker):

    paths = ["stable", "development", "unmaintained"]
    mocker.patch("cincanregistry.metafiles.MetaHandler.read_index_file", return_value=paths)
    # reg = HubReadmeHandler("/")
    # assert reg.max_size == 25000
    # assert reg.max_description_size == 100


def test_update_tool_readme(mocker, tmpdir):
    paths = ["stable", "development", "unmaintained"]
    mocker.patch("cincanregistry.metafiles.MetaHandler.read_index_file", return_value=paths)
    p = tmpdir.mkdir("my_tool").join("README.md")
    p.write("# This is useful example tool.")
    # reg = HubReadmeHandler("/")
    # mocker.patch.object(
    #     reg.client, "ping", return_value=True, autospec=True,
    # )
    # with pytest.raises(RuntimeError):
    #     reg.update_readme_all_tools()

    # mocker.patch.object(reg, "_get_hub_session_cookies", return_value=True)
    # reg.tools_repo_path = pathlib.Path("some/invalid/path")
    # TODO sometime

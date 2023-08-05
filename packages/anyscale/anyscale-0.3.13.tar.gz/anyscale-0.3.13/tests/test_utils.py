import datetime
import json
import tempfile
from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client import Session  # type: ignore
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.util import (
    canonicalize_remote_location,
    deserialize_datetime,
    download_anyscale_wheel,
    get_project_directory_name,
    get_working_dir,
    validate_cluster_configuration,
    wait_for_session_start,
)


@pytest.mark.parametrize(
    "working_dir, remote_location, result",  # type: ignore
    [
        ("test-working-dir", "/a/b/c", "/a/b/c"),
        ("~/test-working-dir", "/root/a/b/c", "~/a/b/c"),
        ("/root/test-working-dir", "~/a/b/c", "/root/a/b/c"),
        ("/root/test-working-dir", "/root/a/b/c", "/root/a/b/c"),
        ("~/test-working-dir", "~/a/b/c", "~/a/b/c"),
    ],
)
def test_canonicalize_remote_location(working_dir, remote_location, result):
    """Test that canonicalize_remote_location
    changes remote_location from being based
    in "~/" or "/root/" to match working_dir.
    """
    cluster_config = {
        "metadata": {"anyscale": {"working_dir": working_dir}},
        "docker": {"container_name": "test-container-name"},
    }
    project_id = "test-project-id"
    assert (
        canonicalize_remote_location(cluster_config, remote_location, project_id)
        == result
    )


def test_deserialize_datetime() -> None:
    date_str = "2020-07-02T20:16:04.000000+00:00"
    assert deserialize_datetime(date_str) == datetime.datetime(
        2020, 7, 2, 20, 16, 4, tzinfo=datetime.timezone.utc
    )


def test_download_anyscale_wheel(base_mock_api_client: Mock) -> None:
    temp_file = tempfile.NamedTemporaryFile("w")
    mock_http_ret_val = Mock()
    mock_http_ret_val.headers = {
        "content-disposition": f'attachment; filename="{temp_file.name}"'
    }
    # This is not UTF-8 decodeable, like the wheel
    mock_http_ret_val.data = b"\x1f\x8b\x08\x08\x1b7\x86_\x02\xffdist/anyscale"
    base_mock_api_client.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get = Mock(
        return_value=mock_http_ret_val
    )
    download_anyscale_wheel(base_mock_api_client, "session_id")
    with open(temp_file.name, "rb") as result:
        assert result.read() == mock_http_ret_val.data

    base_mock_api_client.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get.assert_called_once()


def test_wait_for_session_start(
    mock_api_client_with_session: Mock, session_test_data: Session
) -> None:
    result = wait_for_session_start(
        session_test_data.project_id, session_test_data.id, mock_api_client_with_session
    )
    assert result == session_test_data.id


def test_get_project_directory_name(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    dir_name = get_project_directory_name(project_test_data.id, mock_api_client)

    assert dir_name == project_test_data.directory_name
    mock_api_client.get_project_api_v2_projects_project_id_get.assert_called_once_with(
        project_test_data.id
    )


def test_get_working_dir(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value.result.directory_name = (
        project_test_data.directory_name
    )

    working_dir = get_working_dir({}, project_test_data.id, mock_api_client)
    assert working_dir == f"~/{project_test_data.directory_name}"

    working_dir = get_working_dir(
        {"metadata": {"anyscale": {"working_dir": "test_working_dir"}}},
        project_test_data.id,
        mock_api_client,
    )
    assert working_dir == "test_working_dir"


def test_validate_cluster_configuration(project_test_data: Project) -> None:
    mock_api_client = Mock()
    cluster_config = project_test_data.initial_cluster_config

    with patch("os.path.isfile", Mock(return_value=True)):
        validate_cluster_configuration(
            "tmp.yaml", cluster_config=cluster_config, api_instance=mock_api_client
        )

    mock_api_client.validate_cluster_api_v2_sessions_validate_cluster_post.assert_called_once_with(
        body={"config": json.dumps(cluster_config)}
    )

import json
from pathlib import Path

import pytest
from click import BadParameter
from typer.testing import CliRunner

from trainkit.hf_bucket.main import (
    app,
    bucket_relative_path,
    bucket_remote_path,
    ensure_subdirectory,
    find_bucket_root,
    read_bucket_config,
    resolve_bucket_directory,
    write_bucket_config,
)


def test_write_and_read_bucket_config(tmp_path: Path) -> None:
    write_bucket_config(tmp_path, "user/test-bucket")

    assert read_bucket_config(tmp_path) == {"bucket": "user/test-bucket"}
    assert json.loads((tmp_path / ".hf_bucket.json").read_text()) == {
        "bucket": "user/test-bucket"
    }


def test_find_bucket_root_walks_up_from_nested_directory(tmp_path: Path) -> None:
    write_bucket_config(tmp_path, "user/test-bucket")
    nested = tmp_path / "A" / "B"
    nested.mkdir(parents=True)

    assert find_bucket_root(nested) == tmp_path


def test_find_bucket_root_walks_up_from_nonexistent_directory(tmp_path: Path) -> None:
    write_bucket_config(tmp_path, "user/test-bucket")

    assert find_bucket_root(tmp_path / "A" / "B") == tmp_path


def test_ensure_subdirectory_rejects_paths_outside_root(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()

    with pytest.raises(BadParameter, match="is not inside initialized root"):
        ensure_subdirectory(outside, root)


def test_bucket_relative_path_handles_root_and_nested_directories(
    tmp_path: Path,
) -> None:
    nested = tmp_path / "nested" / "deeper"
    nested.mkdir(parents=True)

    assert bucket_relative_path(tmp_path, tmp_path) == ""
    assert bucket_relative_path(nested, tmp_path) == "nested/deeper"


def test_bucket_remote_path_handles_root_and_nested_directories() -> None:
    assert bucket_remote_path("user/test-bucket", "") == "hf://buckets/user/test-bucket"
    assert (
        bucket_remote_path("user/test-bucket", "nested/deeper")
        == "hf://buckets/user/test-bucket/nested/deeper"
    )


def test_resolve_bucket_directory_returns_root_bucket_directory_and_relative_path(
    tmp_path: Path,
) -> None:
    write_bucket_config(tmp_path, "user/test-bucket")
    directory = tmp_path / "A" / "B"

    root, bucket, resolved_directory, relative_path = resolve_bucket_directory(
        directory
    )

    assert root == tmp_path
    assert bucket == "user/test-bucket"
    assert resolved_directory == directory
    assert relative_path == "A/B"


def test_init_creates_directory_and_config_file(tmp_path: Path) -> None:
    runner = CliRunner()
    root = tmp_path / "bucket-root"

    result = runner.invoke(app, ["init", "user/test-bucket", str(root)])

    assert result.exit_code == 0, result.stdout
    assert root.is_dir()
    assert read_bucket_config(root) == {"bucket": "user/test-bucket"}


def test_init_fails_if_directory_already_exists(tmp_path: Path) -> None:
    runner = CliRunner()
    root = tmp_path / "bucket-root"
    root.mkdir()

    result = runner.invoke(app, ["init", "user/test-bucket", str(root)])

    assert result.exit_code != 0
    assert "already exists" in result.output

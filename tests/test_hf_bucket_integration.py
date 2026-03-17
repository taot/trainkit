import os
from pathlib import Path

import pytest
from huggingface_hub import (
    batch_bucket_files,
    create_bucket,
    download_bucket_files,
    list_bucket_tree,
)
from typer.testing import CliRunner

from trainkit.hf_bucket.main import app

TEST_BUCKET_NAME = "hf_bucket_test"
RUN_INTEGRATION_TESTS_ENV = "HF_BUCKET_RUN_INTEGRATION_TESTS"


def _integration_enabled() -> bool:
    return os.environ.get(RUN_INTEGRATION_TESTS_ENV) == "1"


pytestmark = pytest.mark.skipif(
    not _integration_enabled(),
    reason=(f"set {RUN_INTEGRATION_TESTS_ENV}=1 to run Hugging Face integration tests"),
)


@pytest.fixture
def bucket_id() -> str:
    bucket_url = create_bucket(TEST_BUCKET_NAME, exist_ok=True)
    return bucket_url.bucket_id


@pytest.fixture(autouse=True)
def clear_bucket(bucket_id: str) -> None:
    remote_files = [
        entry.path
        for entry in list_bucket_tree(bucket_id, recursive=True)
        if entry.type == "file"
    ]
    if remote_files:
        batch_bucket_files(bucket_id, delete=remote_files)


def test_sync_up_uploads_nested_directory(tmp_path: Path, bucket_id: str) -> None:
    runner = CliRunner()
    root = tmp_path / "bucket-root"

    init_result = runner.invoke(app, ["init", bucket_id, str(root)])
    assert init_result.exit_code == 0, init_result.stdout

    nested = root / "A" / "B"
    nested.mkdir(parents=True)
    (nested / "one.txt").write_text("one\n")
    (nested / "two.txt").write_text("two\n")

    sync_result = runner.invoke(app, ["sync", "up", str(nested)])
    assert sync_result.exit_code == 0, sync_result.stdout

    remote_files = sorted(
        entry.path
        for entry in list_bucket_tree(bucket_id, recursive=True)
        if entry.type == "file"
    )
    assert remote_files == ["A/B/one.txt", "A/B/two.txt"]

    download_dir = tmp_path / "downloaded"
    download_dir.mkdir()
    download_bucket_files(
        bucket_id,
        [
            ("A/B/one.txt", download_dir / "one.txt"),
            ("A/B/two.txt", download_dir / "two.txt"),
        ],
        raise_on_missing_files=True,
    )
    assert (download_dir / "one.txt").read_text() == "one\n"
    assert (download_dir / "two.txt").read_text() == "two\n"


def test_sync_down_downloads_nested_directory(tmp_path: Path, bucket_id: str) -> None:
    runner = CliRunner()
    root = tmp_path / "bucket-root"

    init_result = runner.invoke(app, ["init", bucket_id, str(root)])
    assert init_result.exit_code == 0, init_result.stdout

    batch_bucket_files(
        bucket_id,
        add=[
            (b"one\n", "A/B/one.txt"),
            (b"two\n", "A/B/two.txt"),
        ],
    )

    sync_result = runner.invoke(app, ["sync", "down", str(root / "A" / "B")])
    assert sync_result.exit_code == 0, sync_result.stdout
    assert (root / "A" / "B" / "one.txt").read_text() == "one\n"
    assert (root / "A" / "B" / "two.txt").read_text() == "two\n"

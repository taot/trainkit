import json
from pathlib import Path
from typing import Any

import typer
from huggingface_hub import sync_bucket

CONFIG_FILENAME = ".hf_bucket.json"

app = typer.Typer()
sync_app = typer.Typer()
app.add_typer(sync_app, name="sync")


def _normalize_directory(path: str | Path) -> Path:
    directory = Path(path).expanduser().resolve(strict=False)
    if directory.exists() and not directory.is_dir():
        raise typer.BadParameter(f"{directory} is not a directory")
    return directory


def _config_path(root: Path) -> Path:
    return root / CONFIG_FILENAME


def write_bucket_config(root: Path, bucket: str) -> Path:
    config_path = _config_path(root)
    config_path.write_text(json.dumps({"bucket": bucket}, indent=4) + "\n")
    return config_path


def read_bucket_config(root: Path) -> dict[str, Any]:
    with _config_path(root).open() as handle:
        return json.load(handle)


def find_bucket_root(start: str | Path) -> Path:
    current = _normalize_directory(start)

    for candidate in (current, *current.parents):
        if _config_path(candidate).is_file():
            return candidate

    raise typer.BadParameter(
        f"could not find {CONFIG_FILENAME} starting from {current}"
    )


def ensure_subdirectory(directory: Path, root: Path) -> Path:
    try:
        directory.relative_to(root)
    except ValueError as exc:
        raise typer.BadParameter(
            f"{directory} is not inside initialized root {root}"
        ) from exc

    return directory


def bucket_relative_path(directory: Path, root: Path) -> str:
    relative = ensure_subdirectory(directory, root).relative_to(root)
    if relative == Path("."):
        return ""
    return relative.as_posix()


def bucket_remote_path(bucket: str, relative_path: str) -> str:
    remote = f"hf://buckets/{bucket}"
    if relative_path:
        return f"{remote}/{relative_path}"
    return remote


def resolve_bucket_directory(directory: str | Path) -> tuple[Path, str, Path, str]:
    resolved_directory = _normalize_directory(directory)
    root = find_bucket_root(resolved_directory)
    config = read_bucket_config(root)
    bucket = config["bucket"]
    relative_path = bucket_relative_path(resolved_directory, root)
    return root, bucket, resolved_directory, relative_path


@app.command()
def init(bucket: str, local_path: str) -> None:
    """Initialize a local directory for a Hugging Face bucket."""
    root = Path(local_path).expanduser().resolve(strict=False)
    if root.exists():
        raise typer.BadParameter(f"{root} already exists")

    root.mkdir(parents=True)
    write_bucket_config(root, bucket)


@sync_app.command("up")
def sync_up(directory: str) -> None:
    """Sync a local directory to a Hugging Face bucket."""
    _, bucket, resolved_directory, relative_path = resolve_bucket_directory(directory)
    if not resolved_directory.exists():
        raise typer.BadParameter(f"{resolved_directory} does not exist")
    sync_bucket(
        source=str(resolved_directory), dest=bucket_remote_path(bucket, relative_path)
    )


@sync_app.command("down")
def sync_down(directory: str) -> None:
    """Sync a Hugging Face bucket directory to local storage."""
    _, bucket, resolved_directory, relative_path = resolve_bucket_directory(directory)
    resolved_directory.mkdir(parents=True, exist_ok=True)
    sync_bucket(
        source=bucket_remote_path(bucket, relative_path), dest=str(resolved_directory)
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()

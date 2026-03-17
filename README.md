# trainkit

Toolkits to help with training models on Cloud GPUs.

## Setup scripts for cloud GPU

## hf_bucket

### Setup

Install `uv`:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Inside the repo:
```bash
uv sync
```

Append this to `~/.bashrc`:
```
export PATH=$PATH:<repo_directory>/bin
```

### Initialize a bucket on local


```bash
hf_bucket init <bucket_id_or_name> <local_bucket_root>
```

Example:

```bash
hf_bucket init librakevin/hf_bucket_test ./hf_bucket_test
```

This creates a config file under <local_bucket_root>:

```json
{
    "bucket": "librakevin/hf_bucket_test"
}
```

### Sync

Sync a local directory from or to the bucket path with the **same relative path** under the initialized root:

```bash
# sync down (download)
hf_bucket sync down <directory>

# sync up (upload)
hf_bucket sync up <directory>
```


NOTES:
- `hf_bucket` walks upward from `<directory>` until it finds `.hf_bucket.json`, and treats that as the initialized root.
- `<directory>` must be inside that root (otherwise it errors).

## Development

### Run tests

```bash
uv run pytest
```

### Integration tests (Hugging Face)

Integration tests are skipped by default. To run them you must enable:

```bash
HF_BUCKET_RUN_INTEGRATION_TESTS=1 uv run pytest -k integration
```

They require working Hugging Face credentials and will create/use a test bucket named `hf_bucket_test`.

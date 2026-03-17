# hf_bucket

hf_bucket uses huggingface_hub python library to sync files between local directory and HuggingFace buckets.

Parse command line arguments with typer.

It supports the following commands:

## Commands

### hf_bucket init

```
hf_bucket init <bucket> <local_path>
```

e.g.

```
hf_bucket init librakevin/test-buckets ./test-buckets
```

1. Create a directory <local_path>. Raise an error if the directory already exists.
2. This <local_path> is the used in the description of the following commands.
3. Write a file <local_path>/.hf_bucket.json, storing bucket name like this:
```
{
    "bucket": "librakevin/test-buckets"
}
```
1. This bucket will be used as the bucket in the following commands

### hf_bucket sync up

```
hf_bucket sync up <directory>
```

1. Sync the content from <directory> to the bucket recursively. This works similar to upload.
2. <directory> can be a relative path or absolute path. It should be a sub-directory inside <local_path>. If not, raise an error.
3. The target path on the bucket should have the same relative path. For example, `hf_bucket sync up ./A/B` should sync the files inside local `./A/B` to bucket's `librakevin/test-buckets/A/B`

### hf_bucket sync down

```
hf_bucket sync down <directory>
```

1. Sync the content from the bucket to <directory> recursively. This works similar to download.
2. <directory> can be a relative path or absolute path. It should be a sub-directory inside <local_path>. If not, raise an error.
3. The source path on the bucket should have the same relative path. For example, `hf_bucket sync down ./A/B` should sync the files inside bucket's `librakevin/test-buckets/A/B` to local `./A/B`.


## Other details

Implement with use `huggingface_hub.sync_bucket` function.

The `hf_bucket sync up` and `hf_bucket sync down` should start from the <directory>, and go up in directories until it finds a `.hf_bucket.json` file. Then treat that directory as the <local_path> of the bucket.

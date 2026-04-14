# Run base eval on cloud GPU

Download checkpoints:

```bash
hf_bucket init librakevin/nanochat-training-checkpoints ~/nanochat-training-checkpoints
```

```bash
cd ~/nanochat-training-checkpoints
hf_bucket sync down 20260315
```


Create cache directory and copy checkpoints:

```bash
mkdir ~/.cache/nanochat -p
cp -r ~/nanochat-training-checkpoints/20260315/base_checkpoints/ ~/.cache/nanochat/
cp -r ~/nanochat-training-checkpoints/20260315/tokenizer/ /root/.cache/nanochat/
```

Activate venv:

```bash
source ~/.venvs/nanochat/bin/activate
```

Download base dataset:

```bash
python -m nanochat.dataset -n 170
```

Run fast evaluation, for example:

```bash
python -m scripts.base_eval --model-tag d24 --device-batch-size=16 --max-per-task=100 --split-tokens=524288
```

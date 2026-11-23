# Dependency lock

Install only from the hash-pinned lock. Direct `==` pins are not enough: transitive packages are locked too, and every distribution has a hash.

```shell
pip install --require-hashes -r requirements.txt
```

`uv sync --frozen` installs the same lock. Weights download uses a separate locked file so the example run does not need the Hub client:

```shell
pip install --require-hashes -r requirements-download.txt
```

`uv.lock` is the source of truth. `[tool.uv] exclude-newer = "7 days"` is recorded in the lock as a 7-day span, so a re-lock still refuses packages uploaded in the last 7 days. The lock covers CPython 3.9–3.12 on Linux, which is where the CUDA 12 `jaxlib` wheels exist.

To update the lock:

```shell
uv lock
uv export --frozen --no-emit-project --emit-find-links -o requirements.txt
uv export --frozen --only-group download --no-emit-project --emit-find-links -o requirements-download.txt
python scripts/check_lock.py
```

Review the diff before committing. CUDA `jaxlib` wheels come from the JAX find-links index, which does not publish hashes. `uv lock` keeps hashes that are already in `uv.lock`, but it will not fill them in for a newly added wheel URL. If a `jaxlib` URL changes, recompute `sha256` from the wheel bytes and put that hash on the wheel entry before committing. `scripts/check_lock.py` fails when any distribution has no hash.

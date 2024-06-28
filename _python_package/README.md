# README

## Develop

```bash
bumpversion patch # patch|minor|major
```

## Test

```bash
python -m unittest
# or
tox
```

## Build

```bash
python -m build --sdist --wheel --outdir dist/
twine upload --repository testpypi dist/*
twine upload dist/*
```

# README

## Develop

```bash
bumpversion patch # patch|minor|major
```

## Build

```bash
python -m build --sdist --wheel --outdir dist/
twine upload --repository testpypi dist/*
twine upload dist/*
```

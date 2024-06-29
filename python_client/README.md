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

## TODO

maybe use openapi-generator?

```bash
npx openapi-generator-cli generate -i ../app/main/static/api/schema.json -g python -o ./client
```

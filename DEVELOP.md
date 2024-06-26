# Commands

```bash
pre-commit install
pre-commit autoupdate
git add . && pre-commit run


bumpversion patch

# python -m unittest
tox

# python setup.py sdist
python -m build --sdist --wheel --outdir dist/
twine upload --repository testpypi dist/*
twine upload dist/*

python -m mkdocs build
```

## Pages

```
# Settings -> Actions -> General -> Workflow permissions: "Read and write permissions"
# Set github page
mkdocs gh-deploy # initially
```

## PYPI

# set PYPI_API_TOKEN

## Tasks

- register add https://readthedocs.org
- register add https://app.snyk.io

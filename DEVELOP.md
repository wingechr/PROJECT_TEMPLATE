# Commands

```bash
pre-commit install
pre-commit autoupdate
git add . && pre-commit run

sphinx-build docs docs/build

bumpversion --allow-dirty patch
python -m unittest

python setup.py sdist
twine upload --repository testpypi dist/*
twine upload dist/*
```

## Tasks

- register add https://readthedocs.org
- register add https://app.snyk.io

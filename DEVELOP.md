## tests

- tests
- unittest
- mocha

## documentation

- docs
- sphinx

## code linting

- flake8
- eslint
- black
- .pre-commit-config.yaml
- pylintrc [?]

```
pre-commit install
pre-commit autoupdate
git add . && pre-commit run # --all
eslint src --fix
black src

```

## build

- webpack
- babel
- scons
- site_scons
- babel.config.json

## software environment

- env
- node_modules
- package.json
- virtualenv
- pip
- npm
- package.json
- requirements.txt
- SConstruct
- webpack.config.js

```
npm prune
npm install
npm upgrade
npm audit --fix # --force
npm shrinkwrap

```

## versioning

- .bumpversion.cfg
- .gitignore

## metadata

- setup.cfg

## packaging

- setup.py

## IDE

- workspace.code-workspace
- .vsvode

env\Script\activate

npm audit --fix # --force
npm install
npm prune
npm update
npm shrinkwrap
sphinx-build docs build/docs
pre-commit autoupdate
bumpversion --allow-dirty patch
python -m unittest
mocha
python setup.py check
python setup.py sdist
twine upload dist/\*

#!/bin/bash
set -e  # stop le script en cas d'erreur

# Listes des versions à tester
PYTHON_VERSIONS=("3.13" "3.9" "2.7")
DJANGO_VERSIONS=("5.0" "4.2" "3.2")

for PYVER in "${PYTHON_VERSIONS[@]}"; do
  for DJVER in "${DJANGO_VERSIONS[@]}"; do
    echo "Testing with Python $PYVER and Django $DJVER"

    # Crée un nouveau Pipenv pour cette version
    PIPENV_PIPFILE=".Pipfile_$PYVER_$DJVER"
    export PIPENV_PIPFILE

    # Crée l'environnement virtuel avec la bonne version de Python
    pipenv --python $PYVER

    # Installe Django spécifique
    pipenv install "django==$DJVER"

    # Lance les tests
    pipenv run coverage run --source=tasks manage.py test tasks

    # Afficher la couverture des tests dans le terminal
    coverage report

    echo "Tests finished for Python $PYVER and Django $DJVER"
  done
done

#!/bin/bash

# Récupère la version passée en paramètre : ./build.sh version=1.0.1
for arg in "$@"; do
  case $arg in
    version=*)
      VERSION="${arg#version=}"
      shift
      ;;
  esac
done

# Vérifie que la version est fournie
if [ -z "$VERSION" ]; then
  exit 1
fi

# Met à jour la variable VERSION dans settings.py
sed -i "s/^VERSION = .*/VERSION = \"$VERSION\"/" todo/settings.py

# Commit + tag
git add .
git commit -m "Release $VERSION"
git tag "$VERSION"

# Génère l’archive zip
git archive --format=zip --output="to-do-list-$VERSION.zip" HEAD

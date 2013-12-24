#!/bin/bash

set -x

cd wibses/yo
grunt build

cd ..

rm -rf static/*
if [[ ! -d static/ ]]; then
    mkdir static
fi

cp -vr yo/dist/styles static/
cp -vr yo/dist/fonts static/
cp -vr yo/dist/scripts static/

cp -vr yo/dist/index.html static/index.html
cp -vr yo/dist/404.html static/404.html
cp -vr yo/dist/favicon.ico static/favicon.ico
cp -vr yo/dist/template static/template

set +x
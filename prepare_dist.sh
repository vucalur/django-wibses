#!/bin/bash

cd wibses/yo
grunt build

cd ..

rm -rf static/wibses/*
if [[ ! -d static/wibses ]]; then
    mkdir -p static/wibses
fi

# TODO vucalur: only a work-around to get lazily fetched bootstrap resources (problem lies in lame grunt build)
cp -vr yo/app/bower_components/bootstrap/dist/fonts static/wibses

cp -vr yo/dist/styles static/wibses
cp -vr yo/dist/scripts static/wibses

# TODO vucalur: serving as htmls as static not suitable for production
cp -vr yo/dist/index.html static/wibses/index.html
cp -vr yo/dist/404.html static/wibses/404.html
cp -vr yo/dist/favicon.ico static/wibses/favicon.ico
cp -vr yo/dist/views static/wibses/views
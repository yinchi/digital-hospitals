#!/usr/bin/env bash
cd digital-hospitals.common
pwd
poetry lock
poetry install
cd ..
echo -e '\n\n'

find . -maxdepth 1 -regex '\./digital-hospitals\..+' -not -name 'digital-hospitals.common' | \
xargs -I % bash -c 'cd %; pwd; poetry lock; poetry install; cd ..; echo -e "\n\n"'

cd digital-hospitals
pwd
poetry lock
poetry install
cd ..
echo -e '\n\n'

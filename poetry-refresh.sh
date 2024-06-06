#!/usr/bin/env bash
cd digital-hospitals.common
pwd
poetry lock
poetry install
cd ..
echo -e '\n\n'

# Any directory equal to or starting with "./digital-hospitals-docs"
find . -maxdepth 1 -regex '\./digital-hospitals-docs.*' | \
xargs -I % bash -c 'cd %; pwd; poetry lock; poetry install; cd ..; echo -e "\n\n"'

# Any directory starting with "./digital-hospitals." except "digital-hospitals.common"
find . -maxdepth 1 -regex '\./digital-hospitals\..+' -not -name 'digital-hospitals.common' | \
xargs -I % bash -c 'cd %; pwd; poetry lock; poetry install; cd ..; echo -e "\n\n"'

# Master "digital-hospitals" directory
cd digital-hospitals
pwd
poetry lock
poetry install
cd ..
echo -e '\n\n'

# Digital Hospitals

This repository is part of the [Digital Hospitals](https://www.ifm.eng.cam.ac.uk/research/dial/research-projects/current-projects/distributed-information-and-automation-laboratory/) project at the Institute for Manufacturing (IfM), University of Cambridge.

**Maintainers**
- Yin-Chi Chan (ycc39)

## Quickstart

`git clone` this repo and `cd` to its root directory. Obtain `secrets.zip` from a project maintainer and place the unzipped `secrets` folder at the project root.

`util.sh` contains a number of utility bash scripts. To access these scripts, run `source util.sh` from the project root directory.

To minimize diffs relating to Jupyter notebooks, [`nbstripout`](https://pypi.org/project/nbstripout/) is recommended:
```bash
pipx install nbstripout
nbstripout --install --attributes .gitattributes
```

### Poetry setup
```bash
pipx install poetry

# Install plugins (optional)
poetry self add poetry-dotenv-plugin

./poetry-refresh.sh
```

This will set up Poetry on your machine and create virtual environments for working on each subproject within this git repo. A master project is also provided within the `/digital-hospitals`
subfolder.

### Starting the services

```bash
source util.sh
build_sphinx  # build documentation pages
dcdev build
dcdev up -d
```

## Todo Tree VSCode plugin

A recommended Visual Studio Code plugin to install is [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree). The `.vscode/settings.json` file for this project contains some useful settings for this plugin.
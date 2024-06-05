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
# Installing the project locally

To work on this project, it is recommended to use either [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) on Windows or Linux directly.

:::{note}
Some of the `bash` commands below may be specific to Ubuntu (and possibly Debian).
:::

## Prerequisites

### Docker

To serve a local copy of the web services provided by this project, a set of Dockerfiles are included as well as a Docker Compose .yaml file. To install Docker locally, go to the [Docker Desktop](https://docs.docker.com/desktop/) website and follow the instructions for your host OS. For Windows, make sure that [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) is also installed.

Alternatively, if you are comfortable with the command line and Linux, you can install the [Docker snap package](https://snapcraft.io/docker).

### pipx and Poetry

If you try to install Python packages in Linux or WSL directly, you will likely encounter this error:

```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

The purpose of this block is to prevent the user from installing conflicting packages which may break the base Linux distribution. Instead, this project uses pipx and Poetry to manage the package dependencies of each subproject in its own virtual environment. To set up the virtual environments:

```bash
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

## Installation

Clone the repository from GitHub. The easiest way is to use the `Clone GitHub repository` link in a new Visual Studio Code window. Alternatively, enter the following in a terminal window:

```bash
git clone https://github.com/yinchi/digital-hospitals.git
```

or, if you have the [GitHub CLI tools](https://cli.github.com/) installed:

```bash
gh repo clone yinchi/digital-hospitals
```

### Secrets folder

The `secrets` folder contains passwords and other sensitive data that is not pushed to GitHub (see the `.gitignore` file). Obtain this folder from a project maintainer and place at the root of the project directory.

### Poetry setup

The following will set up Poetry environments for the main `digital-hospitals` project and each subproject:

```bash
# in project root:
chmod +x poetry-refresh.sh
./poetry-refresh.sh
```

:::{admonition} **Note:** Adding a new subpackage
:class: note

To add a new Python subpackage to the main Poetry project (`digital-hospitals`), add the following line to `digital-hospitals/pyproject.toml`:
```toml
digital-hospitals-zzzz = {path = "../digital-hospitals.zzzz", develop = true}
```
where `zzzz` represents the name of the new subpackage without the `digital-hospitals` prefix. However, do **not** add non-package subprojects (i.e. those configured with `package-mode = false`) to the master `pyproject.toml`. Instead, copy over their dependencies manually.

Finally, re-run `./poetry-refresh.sh`.
:::

### nbstripout

We can use `nbstripout` to reduce the size of commits involving Jupyter notebooks (i.e. notebooks will have to be re-run locally):

```bash
pipx install nbstripout
nbstripout --install --attributes .gitattributes
nbstripout --status  # check status
```
## Utility scripts

A set of utility scripts are included in this project. Load them using `source util.sh`.

The most important script in `util.sh` is `dev-refresh` which:

- Cleans and refreshes the Sphinx documentation in `digital-hospitals-docs`
- Rebuilds all docker containers associated with the Docker Compose file `dockercompose-dev.yaml`, and (re)launches them as necessary

## Deploying the services locally

Make sure Docker is running, then execute the following:

```bash
source util.sh
dev-refresh
```

### Exposing your local services to the web

[ngrok](https://ngrok.com/) is a easy way to launch publicly available web services from your local machine. First, sign up for a free ngrok account, then install ngrok using [these instructions](https://ngrok.com/docs/getting-started/?os=linux). Next, set up a free domain from the ngrok [Dashboard](https://dashboard.ngrok.com/cloud-edge/domains). Finally, ensure your local Docker containers are running and execute:

```bash
ngrok http 80 --domain=<your-free-domain>.ngrok-free.app
```

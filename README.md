# Development for aioSchwab

## Setup Python environment

### Install package manager

#### Install uv

`uv` is a fast Python package installer and virtual environment manager. You can install `uv` by running the following command:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Add the `uv` executable to your system's PATH

Source the appropriate environment file for your shell:

```sh
# On Bash, Zsh, or Sh:
source $HOME/.local/bin/env
# On Fish:
source $HOME/.local/bin/env.fish
```

You may need to restart your shell or open a new terminal session for the changes to take effect.

#### To the location of your Python interpreter:

```sh
# On Windows:
where uv
# On MacOS/Linux:
which uv
```

#### Check uv version

```sh
uv --version
```

### Manage packages

#### Create Virtual Environments and install packages

Sync the environment with the pyproject.toml:

```sh
uv sync
```

#### Check packages available for update

```sh
uv pip list --outdated
```

#### Upgrade packages

```sh
uv pip upgrade
```

### Manage virtual environment

#### Activate the virtual environment

```sh
# On Windows:
.venv\Scripts\activate
# On MacOS/Linux:
source .venv/bin/activate
```

#### To confirm the virtual environment is activated, check the location of your Python interpreter:

```sh
# On Windows:
where python
# On MacOS/Linux:
which python
```

#### Check python version

```sh
python --version
```

#### Deactivate a virtual environment

```sh
# On Windows:
.venv\Scripts\deactivate
# On MacOS/Linux:
deactivate
```

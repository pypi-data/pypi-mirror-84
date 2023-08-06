# StartIn'Blox Manager

## Quick start

### Installation

You will need both Python3 and Pip3 installed. You can follow [this article](https://realpython.com/installing-python/) if you don't konw where to start.

Before diving in Startin' Blox manager, just make sure you got the last version of `pip` by upgrading it:
```
sudo pip3 install --upgrade pip
```

Then install the `sib` command line:
```
$ pip3 install --user -U sib-manager
```

Note:

 * This install the `sib` program in the user context. `sib` doesn't need system priveleges
 * In some distribution the system can't find the user programs. In that case you have to add it manually, for example, by adding `export PATH=$HOME/.local/bin:$PATH` in your `~/.bashrc`.

### Start a LDP server

`sib` supports installation inside `venv`

Create a new project:
```
$ sib startproject myproject
$ cd myproject
```

Note:

 * The project name must be a valid python package name (no dashes).

Configure the modules you want to use in `packages.yml`:
```
ldppackages:
  djangoldp_project: djangoldp_project
  oidc_provider:     django-oidc-provider
```

Run the installation:
```
$ sib install myproject
```

And launch it locally !
```
$ python3 manage.py runserver
```

The administration interface is available at `http://localhost:8000/admin/` with default `admin` user and password.

### Start a client application

Create a new app: FIXME

Compile it:
```
$ sib startapp /tmp/sib_app
```

Run the client app locally:
```
$ cd /tmp/sib_app
$ npm run serve &
```

## Usage

To list all available commands, either read the [documentation](https://git.happy-dev.fr/startinblox/devops/sib/wikis/home) or use:
```
$ sib --help
Usage: sib [OPTIONS] COMMAND [ARGS]...

  Startin'Blox installer
```

## Contribute

Get the last unreleased version of the project:
```
$ pip3 install --user -U git+https://git.happy-dev.fr/startinblox/devops/sib
```


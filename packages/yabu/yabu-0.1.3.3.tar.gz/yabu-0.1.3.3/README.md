# YABU

**yet another backup utility**

[![GitHub](https://img.shields.io/github/license/robertobochet/yabu?color=blue)](https://github.com/RobertoBochet/yabu/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/yabu?color=yellow&label=pypi%20version)](https://pypi.org/project/yabu/)
[![AUR version](https://img.shields.io/aur/version/python-yabu)](https://aur.archlinux.org/packages/python-yabu/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/robertobochet/yabu/Package%20deploy?label=CD)](https://pypi.org/project/yabu/)

**YABU** is a utility that exploiting `rsync` allows to automatize backup tasks also for remote servers. 

## Install

**YABU** required to work the `rsync` tool, you can easily retrieves it from your package manager:

### From AUR (recommended if you using Arch Linux)

**YABU** is available also as **AUR** package. Yuo can find it as [`python-yabu`](https://aur.archlinux.org/packages/python-yabu/).

### From pypi (recommended)

You can install **YABU** from **pypi** using **pip**.

```shell script
pip install yabu
``` 

### From source code

An alternative way to install **YABU** is from the source code, exploiting the `setup.py` script.

```shell script
git clone https://github.com/RobertoBochet/yabu.git
cd yabu
python3 setup.py install --user 
```

## Usage

```shell script
yabu -h
```
```text
usage: yabu [-h] [-c CONFIG_PATH] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config CONFIG_PATH
                        configuration file path
  -v                    number of -v defines level of verbosity
  --version             show program's version number and exit
```

*Before start **YABU** you must create a custom configuration file (see configuration section).*

## Configuration

The whole **YABU** behaviour can be configured with its `config.yaml`.
You can provide to **YABU** a custom configuration file exploiting argument `-c`, if you will not do it, **YABU** will look for it in the default path `/etc/yabu/config.yaml`. 

### `config.yaml` structure

- `tasks` *[dict\<string,dict\>]* is a dict of the tasks that will be done, each task has a custom name as key and it has a specific struct

    - `remote_base_path` *[string]*
        the base path of the remote server
    
    - `targets` *[list\<string\>]*
        a list of the paths that have to be backuped

*A complete schema of config file can be found in `yabu/resources/config.schema.yaml`.*
# YABU

**yet another backup utility**

[![GitHub](https://img.shields.io/github/license/robertobochet/yabu?color=blue)](https://github.com/RobertoBochet/yabu/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/yabu?color=yellow&label=pypi%20version)](https://pypi.org/project/yabu/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/robertobochet/yabu/Upload%20Python%20Package?label=pypi%20build)](https://pypi.org/project/yabu/)

**YABU** is a utility that exploiting `rsync` allows to automatize backup tasks also for remote servers. 


## Install

**YABU** required to work the `rsync` tool, you can easily retrieves it from your package manager:

### From pypi

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
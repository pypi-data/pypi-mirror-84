# dogebuild-tex

[![Build Status](https://travis-ci.com/dogebuild/dogebuild-tex.svg?branch=master)](https://travis-ci.com/dogebuild/dogebuild-tex)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tex plugin for [dogebuild](https://github.com/dogebuild/dogebuild).

## Install

To install dogebuild-tex call

```shell script
pip install dogebuild-tex
```

## How to create project

Create `dogefile.py` and fill it with following code:

```python
from dogebuild_tex import Tex

Tex()
```

Create your latex document in `main.tex` file.
To build project run `doge build` or `doge pdf`.

## Use docker image to build project

Dogebuild-tex allow you to use docker image to keep your build reproducible.
To use docker set image as tex binary as follow:

```python
from dogebuild_tex import Tex, DockerTexBinary

Tex(
    tex_binary=DockerTexBinary("{docker-image-name}")
)
```

Dogebuild will call docker at the build process.

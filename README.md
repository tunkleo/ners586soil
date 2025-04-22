

## Package setup
This uses python 3.12. Necessary packages may be found in pyproject.toml. The easiest way to get things running is to install the [uv](https://astral.sh/uv/) package manager with:

```curl -LsSf https://astral.sh/uv/install.sh | sh```

After installation, you will need to restart your terminal.

If on a mac with homebrew, you can install uv with:

```brew install uv```

If you have trouble with installation, check their [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Usage
First clone this repository:
```git clone git@github.com:tunkleo/ners586soil.git```  

```cd ners586soil```

Currently, the jupyter notebook, testground.ipynb, is the best way to run this code. Otherwise, you can use the following commands to run the python scripts:

```uv run soilproject.py```

```uv run utils.py```

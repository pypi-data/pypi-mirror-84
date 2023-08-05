# sym-flow-cli

Sym Flow CLI

## Shell Completion

Bash:

    eval "$(env _SYM_COMPLETE=source_bash sym)"

Zsh:

    eval "$(env _SYM_COMPLETE=source_zsh sym)"

TODO: Build an [activation script](https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script) and ship with the code?

## Testing setuptools

This setup is based on [Click's docs](https://click.palletsprojects.com/en/7.x/setuptools/) for setuptools integration.

### pyenv-virtualenv setup

Install `pyenv-virtualenv` so you can create a virtualenv to install the CLI into:

    $ brew install pyenv-virtualenv

Add the following to your `.zshrc`:

    eval "$(pyenv init -)"
    if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi

### Install the CLI

Now install the CLI into a new virtualenv to make sure you've got everything working right:

    $ pyenv virtualenv symflow-cli
    $ pyenv activate symflow-cli
    $ pip install --editable .
    $ symflow --help

### Release

1. Set a PyPI API token in your local env
2. `./scripts/dist.sh`

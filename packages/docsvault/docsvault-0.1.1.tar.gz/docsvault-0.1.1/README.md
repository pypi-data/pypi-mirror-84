# DocsVault

> DocsVault is a python webapp that allow you to easily and reliably store importants documents in a ciphered vault.

For more informations, take a look at [full documentation](https://docsvault.sylvan.ovh)!

## Installation

DocsVault is available [on pypi](https://pypi.org/project/docsvault/).
You can install it using pip, or any pip-based tool like [pipenv](https://pipenv.pypa.io/en/latest/).

```bash
pip install docsvault
```

## Usage

Launch application server
```bash
docsvault server
```

Open web UI to interract with docsvault service.
```bash
docsvault webui
```

*Note: if server is not started, `docsvault webui` will run the server daemon automatically*

## Contribute

### Requirements

To contribute, you must have installed the following tools

- vue.js (version 2)
- python (version >= 3.6)
- pipenv (optional)


Then simply run 
```bash
make install
```

To automatically install python and npm dev. dependencies.

### Develop

You can start development server for backend by running
Idem for backend
```bash
pipenv run serve
```

Idem for frontend
```bash
npm run serve
```

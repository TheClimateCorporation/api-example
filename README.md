# API Example

Example app using Climate's API.

## Running the example

1. Follow steps in _Setup_
2. Set `client_id`, `client_secret`, and `api_key` values in main.py
3. Start the server:

```bash
python3 main.py
```

4. Open a browser to [localhost:8080/home](http://localhost:8080/home)

## Setup

Install python 3.6+.

```bash
# if you use Mac OS X and brew, this can be done with:
brew install python3
```

Make a virtual environment, activate it, and install dependencies.

```bash
python3 -m venv api-example
source api-example/bin/activate
pip install -r requirements.txt
```

When you're done testing the example, deactivate the virtual environment with:

```bash
deactivate
```

## License

Copyright © 2017 The Climate Corporation

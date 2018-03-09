# API Example

Example app using Climate's [FieldView API](https://dev.fieldview.com).

## Setup

1. Install python 3.6+.

```bash
# if you use Mac OS X and brew, this can be done with:
brew install python3
```

2. Make a virtual environment, activate it, and install dependencies.

```bash
python3 -m venv api-example
source api-example/bin/activate
pip install -r requirements.txt
```

3. Set the following environment variables (or hardcode them in `main.py`)
to the values provided to you by Climate:

```bash
export CLIMATE_API_ID="partner-fooco"
export CLIMATE_API_SECRET="azbq56fpadhnt8oukoeani2a4w"
export CLIMATE_API_KEY="partner-fooco-216b9875-0158-4142-1ab2-7c3bdbd6a2157"
export CLIMATE_API_SCOPES="openid fields:read imagery:write"
```

Regarding scopes - see the [FieldView API technical documentation](https://dev.fieldview.com/technical-documentation/) for more scopes and their
corresponding endpoints.

4. When you're done running the example, deactivate the virtual environment with:

```bash
deactivate
```

## Running the web example

1. Follow steps in _Setup_

2. Start the server:

```bash
python3 main.py
```

3. Open a browser to [localhost:8080/home](http://localhost:8080/home)

## License

Copyright © 2017 The Climate Corporation

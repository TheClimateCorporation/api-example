# API Example

Example app using Climate's API.

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

## Running the example

1. Follow steps in _Setup_

1. Set the following environment variables to the values provided by Climate:

    ```
    export CLIMATE_API_ID="partner-fooco"
    export CLIMATE_API_SECRET="azbq56fpadhnt8oukoeani2a4w"
    export CLIMATE_API_KEY="partner-fooco-216b9875-0158-4142-1ab2-7c3bdbd6a2157"
    ```
    
3. Start the server:

    ```bash
    python3 main.py
    ```

4. Open a browser to [localhost:8080/home](http://localhost:8080/home)

## License

Copyright © 2017 The Climate Corporation

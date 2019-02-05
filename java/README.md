# API Example

Example app exercising some of Climate's [FieldView API](https://dev.fieldview.com).

## Setup

1. Install [Java 8+](https://www.java.com/en/download/)
2. Install [Gradle](https://gradle.org/install/)
3. Set the following environment variables

```bash
export CLIMATE_APP_ID="my-api-id"
export CLIMATE_APP_SECRET="azbq56fpadhnt8oukoeani2a4w"
export CLIMATE_API_KEY="my-api-id-216b9875-0158-4142-1ab2-7c3bdbd6a2157"
export CLIMATE_API_SCOPES=" fields:read asPlanted:read"
```
Regarding scopes - see the [FieldView API technical documentation](https://dev.fieldview.com/technical-documentation/) for more scopes and their
corresponding endpoints (click the `Authorize` button in the swagger docs).

## Running the web example

1. Start the server:

```bash
./gradlew run
```

2. Open a browser to [localhost:8080](http://localhost:8080)

## License

Copyright © 2019 The Climate Corporation
# FMCV Debug Proxy

A FastAPI-based debug proxy for intercepting and logging API requests and responses.

## Features

- Intercepts and logs all incoming API requests
- Forwards requests to a target API
- Logs responses from the target API
- Measures and logs request duration
- Configurable via a JSON file
- Error logging for debugging

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install fastapi uvicorn requests pyfiglet
```

## Configuration

Edit the `config.txt` file to set your configuration:

```json
{
  "TARGET_URL": "http://Target:1234",
  "REQEST_CONNECTION_TIMEOUT": 2,
  "REQEST_READ_TIMEOUT": 5,
  "host": "0.0.0.0",
  "port": 8888
}
```

## Usage

Run the proxy server:

```bash
python main.py
```

The server will start on the host and port specified in the configuration file.

## Logs

Logs are stored in the `logs` directory:

- `YYYYMMDD_logs.txt`: Contains detailed logs of requests and responses
- `YYYYMMDD_error.txt`: Contains error logs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[GPLv3 License](LICENSE)

## Author

Created by chong@fmcv.my

For more information, visit [www.fmcv.my](http://www.fmcv.my)

## Version

20240813
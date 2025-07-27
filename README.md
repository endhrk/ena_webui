# ENA webui

This project provides a small Flask-based web UI that connects to a KoboldCpp API endpoint to generate novel text.

## Features

- Prompt entry and generation of text via KoboldCpp
- Simple log and chapter saving to JSON files
- Command line options for host, port and KoboldCpp API URL

## Requirements

- Python 3.11+
- `Flask` and `requests` (see `requirements.txt`)

## Usage

Install the dependencies and start the server:

```bash
pip install -r requirements.txt
python app.py --host 0.0.0.0 --port 5000 --kobold-url http://localhost:5001/api/v1/generate
```

### Using a virtual environment

Creating a Python virtual environment is recommended so that the
dependencies for this project do not interfere with other Python
packages on your system. You can set one up with the built in
`venv` module:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py --host 0.0.0.0 --port 5000 --kobold-url http://localhost:5001/api/v1/generate
```

Open the displayed URL in your browser. Enter a prompt on the left, then press **Generate** to call the KoboldCpp API. Generated text appears on the right. The log area can be used to save the result as a chapter in the `chapters/` directory.

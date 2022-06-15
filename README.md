# Coincounter

## Preparation

1. create a virtual python environment and install the dependencies

Windows
```PowerShell
Set-ExecutionPolicy RemoteSigned-Scope CurrentUser
python -m venv ./venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

Linux
```bash
python -m venv ./venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Programm

```bash
./src/coincounter.py
```
# SpeakEasy

The backing API to support the speak easy app.

# Installing

Install prerequisites with:

```console
python3.6 -m pip install -r requirements.txt
```

# Config File

```ini
[Files]
tempdir=/home/chris/Git/SpeakEasy/temp
```

# Running server

```console
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/file.json" export FLASK_DEBUG=1; export FLASK_APP=main; flask run -h 0.0.0.0 -p 80
```
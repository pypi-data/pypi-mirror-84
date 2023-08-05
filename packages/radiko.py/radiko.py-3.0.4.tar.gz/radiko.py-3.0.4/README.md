# radiko.py

"radiko.py" is a python library to use radiko API.

# DEMO

```python
client = Client()

for station in client.stations:
    print(station.id, station.name, station.get_on_air().title)
    print(client.get_stream(station))
```

# Requirement

* Python 3.8

# Installation

```bash
pip install radiko.py
```

# Author

akatobo1011

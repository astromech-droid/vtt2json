``vtt2json`` converts .vtt file to json string.

Installation
------------
    $ pip install vtt2json

Usage
------------
```python
from vtt2json import vtt2json

json_str = vtt2json.to_json("captions.vtt")
print(json_str)
```

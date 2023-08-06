# Astro Bot List Python Wrapper

This is a wrapper for astro bot list made for python

# Get Bot Stats

```python
from main import Botlists
abl = Botlists('api key')
x=abl.get()
print(x)
```

# Post Server Count
```python
from main import Botlists
abl = Botlists('api key')

x=abl.count(12)
print(x)
```
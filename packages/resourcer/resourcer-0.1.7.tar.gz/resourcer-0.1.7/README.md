## Resourcer

A simple wrapper around [requests](https://github.com/psf/requests).  

```
pip install resourcer
```

Example usage

```Python
from resourcer import Resource

resource = Resource('https://{domain}/{path1}/{path2}')

resource.domain = "github.com"
resource.path1 = "fiazsami"
resource.path2 = "resourcer"

response = resource.get()
print(response.text)
```
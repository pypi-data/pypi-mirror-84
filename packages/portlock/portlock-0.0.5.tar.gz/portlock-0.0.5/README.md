# portlock

A simple library you can use to ensure that only one copy of your script is running at once

Works on *NIX systems, not sure about Windows.

```
from portlock import ensure_singleton

def main():
    ensure_singleton(6000)
    # If you reach here, you can ensure that no other proccess
    # is running on port 6000
    ...
```

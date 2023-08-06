# Mythic Scripting Interface

The `mythic` package creats a way to programatically interact and control a Mythic instance. Mythic is a Command and Control (C2) framework for Red Teaming. The code is on GitHub (https://github.com/its-a-feature/Mythic) and the Mythic project's documentation is on GitBooks (https://docs.mythic-c2.net).

## Installation

You can install the mythic scripting interface from PyPI:

```
pip install mythic
```

## How to use

Version 0.0.3 of the `mythic` package supports version 2.1.* of the Mythic project.

```
from mythic import mythic_rest
mythic = mythic_rest.Mythic(
    username="mythic_admin",
    password="mythic_password",
    server_ip="192.168.205.151",
    server_port="7443",
    ssl=True,
    global_timeout=-1,
)
await mythic.login()
```

The Mythic documentation has a whole section on scripting examples (https://docs.mythic-c2.net/scripting) that are useful for how to leverage this package. 

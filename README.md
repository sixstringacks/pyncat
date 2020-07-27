pyncat is a simple implementation of netcat. This is based on the version found in Black Hat Python.

```
python .\pyncat.py -h
                                      __
        ____  __  ______  _________ _/ /_
       / __ \/ / / / __ \/ ___/ __ `/ __/
      / /_/ / /_/ / / / / /__/ /_/ / /_
     / .___/\__, /_/ /_/\___/\__,_/\__/
    /_/    /____/

pyncat | A simple python implementation of netcat
          written by @autocorekt


usage: pyncat.py [-h] [-l] -p PORT -t HOST [-v]

A python implementation of netcat.

optional arguments:
  -h, --help            show this help message and exit
  -l, --listen          listen for incoming connections (listen mode)
  -p PORT, --port PORT  source port
  -t HOST, --host HOST  target host / IP to listen on if in listen mode
  -v, --verbose         increase verbosity
```

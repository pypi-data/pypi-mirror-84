# pyizone

This python module aims to implement query and control of WiFi-enabled iZone 310 and compatible family of climate control devices.

## Installing pre-requisites

Clone the repository, change into the directory and run `pip install -r requirements.txt`.

It will require python3, and has been tested with version 3.5 and later.

## Using as a command line tool

You can import this module to use it as a command line tool.

You could also set an alias, for example:

```bash
alias izone='python3 -m pyizone'
```

### View help

```
$ python3 -m pyizone
usage: izone [-h] [--verbose] {discover,get,set} ...

Control a control-bridge equipped iZone airconditioning system

optional arguments:
  -h, --help          show this help message and exit
  --verbose, -v

Available subcommands:
  {discover,get,set}
```

### Discover devices

```
$ python3 -m pyizone discover
Found 1 iZone Controls-Bridge:
  Device ID: 000000XXX (at: xxx.xxx.xxx.xxx:xxxxx)
Run 'export IZONE_DEVICE=xxx.xxx.xxx.xxx' to automatically target this controls-bridge for all future izone commands.
```

```
$ export IZONE_DEVICE=xxx.xxx.xxx.xxx
```

### Querying settings

```
$ python3 -m pyizone get fan
xxx.xxx.xxx.xxx: System fan is: low
```

```
$ python3 -m pyizone get mode
xxx.xxx.xxx.xxx: System mode is: vent
```

### Setting settings

```
$ python3 -m pyizone set power on
xxx.xxx.xxx.xxx: System power is: on
```

```
$ python3 -m pyizone set mode vent
xxx.xxx.xxx.xxx: System mode is: vent
```

```
$ python3 -m pyizone set fan low
xxx.xxx.xxx.xxx: System fan is: low
```

## Using as a Python Module

```python
>>> import pyizone
>>> pyizone.discover()
[{'port': 'xxxx', 'id': '000000XXX', 'ipaddr': 'xxx.xxx.xxx.xxx'}]
>>> pyizone.get_system_settings("xxx.xxx.xxx.xxx")
{'Temp': '0.0', 'Setpoint': '22.0', 'NoOfConst': 1, 'UnitType': 'Unknown', 'CtrlZone': 13, 'ACError': '', 'EcoMax': '26.0', 'SysOn': 'on', 'Tag2': '', 'AirStreamDeviceUId': '000000XXX', 'Id': 0, 'Supply': '0.0', 'Warnings': 'filter', 'Tag1': 'iZone 310', 'SleepTimer': 0, 'UnitLocked': 'false', 'AirflowLock': 'off', 'EcoMin': '22.0', 'SysType': '310', 'NoOfZones': 7, 'SysFan': 'low', 'DeviceType': 'ASH', 'RAS': 'master', 'SysMode': 'vent', 'EcoLock': 'true'}
```

## Getting Help

### Docstrings

Each function has docstrings, so you can get help using python's `help()` function, for example:

```python
>>> help(pyizone.discover)
```

Returns:

```
Help on function discover in module pyizone.__pyizone__:

discover(discovery_timeout_seconds:float=5.0, socket_timeout_seconds:float=1.0, izone_cb_id=None) -> list
    Attempts discovery of iZone 1.x Controls Bridges (CB)

    Args:
        discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
        socket_timeout_seconds: (float) Socket timeout in number of seconds
        izone_cb_id: (str) Look for a specific id only, and return as soon as it is found

    Returns:
        A list of dict objects containing the id (str), ipaddr (str) and port (str) of each CB discovered, eg:
        [{'ipaddr': '192.168.0.9', 'id': '000002323', 'port': '12107'}]
```

### Open an issue

Please feel free to [open an issue on the project's GitHub](https://github.com/mikenye/pyizone/issues), and I'll do my best to help you.

I also have a [Discord channel](https://discord.gg/sTf9uYF), feel free to [join](https://discord.gg/sTf9uYF) and converse.

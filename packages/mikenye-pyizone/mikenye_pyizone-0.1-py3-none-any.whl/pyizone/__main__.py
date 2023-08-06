#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import pyizone

# Import "Literal". This is only available in Python 3.8+.
# It has been backported to the 3rd party module "typing_extensions" for previous versions of Python.
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


def error_on_non_empty_response(
    izone_device: str,
    response: dict,
    verb: str,
    setting_name: str,
):
    if response != {}:
        print(
            "{izone_device}: ERROR: Could not {verb} {setting_name}!".format(
                izone_device=izone_device,
                verb=verb,
                setting_name=setting_name,
            ),
            file=sys.stderr
        )


def discovery(
    print_output: bool = True,
    discovery_timeout_seconds: float = pyizone.__pyizone__.DISCOVERY_TIMEOUT_SECONDS,
):

    response = pyizone.discover()

    txt = "  Device ID: {id} (at: {ipaddr}:{port})"

    device_ids = list()

    if len(response) > 0:
        if len(response) == 1:
            if print_output:
                print("Found {num} iZone Controls-Bridge:".format(num=len(response)))
        elif len(response) > 1:
            if print_output:
                print("Found {num} iZone Controls-Bridges:".format(num=len(response)))
        for cb in response:
            device_ids.append(cb['id'])
            if print_output:
                print(txt.format(
                    id=cb['id'],
                    ipaddr=cb['ipaddr'],
                    port=cb['port'],
                    ))
        if len(response) == 1:
            txt = "Run 'export IZONE_DEVICE={ipaddr}' to automatically target this"
            txt += " controls-bridge for all future izone commands."
            print(txt.format(
                ipaddr=response[0]['ipaddr'],
            ))

    return device_ids


def add_izone_device_argument(parser):
    parser.add_argument(
        '-d', '--izone-device',
        type=str,
        default=os.getenv("IZONE_DEVICE", default=None),
        help="The IPv4 address or numeric ID of the iZone CB, can also be set with environment variable 'IZONE_DEVICE'",
    )


def sanitise_izone_device(
    izone_device
):
    # If izone_device is not given, then do discovery, if only one iZone then use it
    if izone_device is None:
        device_ids = discovery(
            print_output=False,
            discovery_timeout_seconds=1,
            )
        if len(device_ids) > 1:
            print("ERROR: specify a device ID!", file=sys.stderr)
            sys.exit(1)
        elif len(device_ids) == 0:
            print("ERROR: no iZone devices found!", file=sys.stderr)
            sys.exit(1)
        else:
            izone_device = pyizone.get_ipaddr(device_ids[0])
    return izone_device


def get_system_setting(
    izone_device: str,
    setting_name: str,
    json_key: str,
    suffix: str = "",
    system_settings_dict=None,
):

    if system_settings_dict is None:
        system_settings_dict = pyizone.get_system_settings(izone_device)

    if suffix != "":
        suffix = " {suffix}".format(suffix=suffix)

    if json_key in system_settings_dict:
        print(
            "{izone_device}: System {setting_name} is: {setting_value}{suffix}".format(
                izone_device=izone_device,
                setting_name=setting_name,
                setting_value=system_settings_dict[json_key],
                suffix=suffix,
            )
        )
    else:
        print(
            "{izone_device}: ERROR: Could not determine system {setting_name}!".format(
                izone_device=izone_device,
                setting_name=setting_name,
            ),
            file=sys.stderr
        )


def get_zone(
    izone_device: str,
    zone_to_get: Literal[
        'all',
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    ],
    include_default_named_zones: bool = False,
):

    response = pyizone.get_zones(izone_device)

    # get maximum length zone name (for formatting)
    max_zone_name_length = 0
    for zone in response.keys():
        if len(response[zone]['Name']) > max_zone_name_length:
            max_zone_name_length = len(response[zone]['Name'])

    num_active_zones = 0
    num_closed_zones = 0
    num_open_zones = 0
    # get number of active zones (for formatting)
    if zone_to_get == 'all':
        for zone in response.keys():
            if response[zone]['Name'] == "Zone {zone_number}".format(zone_number=zone) and not include_default_named_zones:
                continue
            num_active_zones += 1
            if response[zone]['Mode'] == 'close':
                num_closed_zones += 1
            if response[zone]['Mode'] == 'open':
                num_open_zones += 1

    # output zone info
    if zone_to_get == 'all':
        print("{izone_device}: Total zones: {num_active_zones}, {num_closed_zones} closed, {num_open_zones} open:".format(
            izone_device=izone_device,
            num_active_zones=num_active_zones,
            num_closed_zones=num_closed_zones,
            num_open_zones=num_open_zones,
        ))
    for zone in response.keys():

        if zone_to_get != 'all' and zone_to_get != zone:
            continue

        is_zone_default_name = response[zone]['Name'] == "Zone {zone_number}".format(zone_number=zone)
        if is_zone_default_name and not include_default_named_zones and zone_to_get == 'all':
            continue

        if response[zone]['Mode'] == 'close':
            response[zone]['Mode'] = 'closed'

        txt = "Zone {zone_number}  |  {zone_name}  |  zone is {zone_mode}  |".format(
            zone_number=str(zone).rjust(len(str(num_active_zones))),
            zone_name=response[zone]['Name'].ljust(max_zone_name_length),
            zone_mode=response[zone]['Mode'].ljust(6),  # length of "closed"
        )
        txt += "  closed (min) airflow: {zone_airmin}  |  open (max) airflow: {zone_airmax}".format(
            zone_airmin=str(response[zone]['MinAir']).rjust(3),
            zone_airmax=str(response[zone]['MaxAir']).rjust(3),
        )
        print(txt)


def main():

    description = "Control a control-bridge equipped iZone airconditioning system"

    # Prepare command line

    parser = argparse.ArgumentParser(
        prog='izone',
        description=description,
        epilog="See github repo for documentation",
    )

    parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers_root = parser.add_subparsers(
        title="Available subcommands"
    )

    # "discover"
    parser_discover = subparsers_root.add_parser("discover")
    parser_discover.set_defaults(root_cmd_discover=True)

    # "get"
    parser_get = subparsers_root.add_parser("get")
    parser_get.set_defaults(root_cmd_get=True)
    add_izone_device_argument(parser_get)
    subparsers_get = parser_get.add_subparsers(
        title="Available 'get' subcommands"
    )

    # "get all"
    parser_get_all = subparsers_get.add_parser("all")
    parser_get_all.set_defaults(get_all=True)

    # "get fan"
    parser_get_fan = subparsers_get.add_parser("fan")
    parser_get_fan.set_defaults(get_fan=True)

    # "get mode"
    parser_get_mode = subparsers_get.add_parser("mode")
    parser_get_mode.set_defaults(get_mode=True)

    # "get power"
    parser_get_power = subparsers_get.add_parser("power")
    parser_get_power.set_defaults(get_power=True)

    # "get setpoint"
    parser_get_setpoint = subparsers_get.add_parser("setpoint")
    parser_get_setpoint.set_defaults(get_setpoint=True)

    # "get sleeptimer"
    parser_get_sleep = subparsers_get.add_parser("sleeptimer")
    parser_get_sleep.set_defaults(get_sleeptimer=True)

    # "get zones"
    parser_get_zones = subparsers_get.add_parser("zones")
    parser_get_zones.set_defaults(get_zones=True)
    parser_get_zones.add_argument(
        '-a',
        '--include-all-zones',
        action='store_true',
        default=False,
        help="This open shows default named zones (which are otherwise assumed to be unused)",
    )

    # "get zone"
    parser_get_zone = subparsers_get.add_parser("zone")
    parser_get_zone.set_defaults(get_zone=True)
    parser_get_zone.add_argument(
        'zone_number',
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        help="Show information about this zone",
    )

    # "set"
    parser_set = subparsers_root.add_parser("set")
    parser_set.set_defaults(root_cmd_set=True)
    add_izone_device_argument(parser_set)
    subparsers_set = parser_set.add_subparsers(
        title="Available 'set' subcommands"
    )

    # "set fan"
    parser_set_fan = subparsers_set.add_parser("fan")
    parser_set_fan.set_defaults(set_fan=True)
    parser_set_fan.add_argument(
        'fan_speed',
        type=str,
        choices=[
            pyizone.FAN.AUTO,
            pyizone.FAN.LOW,
            pyizone.FAN.MEDIUM,
            pyizone.FAN.HIGH,
        ],
        help="Set the fan speed",
    )

    # "set mode"
    parser_set_mode = subparsers_set.add_parser("mode")
    parser_set_mode.set_defaults(set_mode=True)
    parser_set_mode.add_argument(
        'mode',
        type=str,
        choices=[
            pyizone.MODE.AUTO,
            pyizone.MODE.COOL,
            pyizone.MODE.HEAT,
            pyizone.MODE.VENT,
            pyizone.MODE.DRY,
        ],
        help="Set the mode of operation",
    )

    # "set power"
    parser_set_power = subparsers_set.add_parser("power")
    parser_set_power.set_defaults(set_power=True)
    parser_set_power.add_argument(
        'power_state',
        type=str,
        choices=['on', 'off'],
        help="Turn the system on or off",
    )

    # "set setpoint"
    parser_set_setpoint = subparsers_set.add_parser("setpoint")
    parser_set_setpoint.set_defaults(set_setpoint=True)
    parser_set_setpoint.add_argument(
        'temperature',
        type=float,
        help="The setpoint temperature in degrees celcius",
    )

    # "set sleeptimer"
    parser_set_sleep = subparsers_set.add_parser("sleeptimer")
    parser_set_sleep.set_defaults(set_sleeptimer=True)
    parser_set_sleep.add_argument(
        'minutes',
        type=int,
        choices=[
            pyizone.SLEEPTIMER.OFF,
            pyizone.SLEEPTIMER.MINS_30,
            pyizone.SLEEPTIMER.MINS_60,
            pyizone.SLEEPTIMER.MINS_90,
            pyizone.SLEEPTIMER.MINS_120,
        ],
        help="Set sleep timer minutes",
    )

    # "set zone"
    parser_set_zone = subparsers_set.add_parser("zone")
    parser_set_zone.set_defaults(set_zone=True)
    parser_set_zone.add_argument(
        'zone_number',
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        help="Perform set operation on this zone",
    )
    subparsers_set_zone = parser_set_zone.add_subparsers(
        title="Available 'zone' subcommands"
    )

    # "set zone mode"
    parser_set_zone_mode = subparsers_set_zone.add_parser("mode")
    parser_set_zone_mode.set_defaults(set_zone_mode=True)
    parser_set_zone_mode.add_argument(
        'zone_mode',
        type=str,
        choices=('open', 'close', 'closed'),
        help="Set the zone mode to open or closed",
    )

    # "set zone airflow"
    parser_set_zone_airflow = subparsers_set_zone.add_parser("airflow")
    parser_set_zone_airflow.set_defaults(set_zone_airflow=True)
    parser_set_zone_airflow.add_argument(
        'min_max',
        type=str,
        choices=('min', 'max'),
        help="Set the minimum or maximum airflow",
    )
    parser_set_zone_airflow.add_argument(
        'airflow_percent',
        type=int,
        help="Set the airflow percentage",
    )

    # Parse args
    args = parser.parse_args()

    # Set up logging
    if args.verbose > 0:

        logger = logging.getLogger()
        FORMAT = "[%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s()] %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logging.debug('Verbose logging enabled')

    # Handle command line

    # Handle "discover"
    if getattr(args, 'root_cmd_discover', False):
        discovery()

    # Handle "get all"
    elif getattr(args, 'get_all', False):
        izone_device = sanitise_izone_device(args.izone_device)
        system_settings_dict = pyizone.get_system_settings(izone_device)
        settings = [
            {
                'setting_name': 'CB ID',
                'json_key': 'AirStreamDeviceUId',
                'suffix': '',
            },
            {
                'setting_name': 'power',
                'json_key': 'SysOn',
                'suffix': '',
            },
            {
                'setting_name': 'mode',
                'json_key': 'SysMode',
                'suffix': '',
            },
            {
                'setting_name': 'fan',
                'json_key': 'SysFan',
                'suffix': '',
            },
            {
                'setting_name': 'sleep timer',
                'json_key': 'SleepTimer',
                'suffix': 'minutes',
            },
            {
                'setting_name': 'unit type',
                'json_key': 'UnitType',
                'suffix': '',
            },
            {
                'setting_name': 'supply (in-duct) air temperature',
                'json_key': 'Supply',
                'suffix': '°C',
            },
            {
                'setting_name': 'setpoint',
                'json_key': 'Setpoint',
                'suffix': '°C',
            },
            {
                'setting_name': 'return air temperature',
                'json_key': 'Temp',
                'suffix': '°C',
            },
            {
                'setting_name': 'return air temperature sensor',
                'json_key': 'RAS',
                'suffix': '',
            },
            {
                'setting_name': 'controlling zone',
                'json_key': 'CtrlZone',
                'suffix': '',
            },
            {
                'setting_name': 'tag 1',
                'json_key': 'Tag1',
                'suffix': '',
            },
            {
                'setting_name': 'tag 2',
                'json_key': 'Tag2',
                'suffix': '',
            },
            {
                'setting_name': 'warnings',
                'json_key': 'Warnings',
                'suffix': '',
            },
            {
                'setting_name': 'errors',
                'json_key': 'ACError',
                'suffix': '',
            },
            {
                'setting_name': 'eco lock',
                'json_key': 'EcoLock',
                'suffix': '',
            },
            {
                'setting_name': 'eco max',
                'json_key': 'EcoMax',
                'suffix': '',
            },
            {
                'setting_name': 'eco min',
                'json_key': 'EcoMin',
                'suffix': '',
            },
            {
                'setting_name': 'number of constant zones',
                'json_key': 'NoOfConst',
                'suffix': '',
            },
            {
                'setting_name': 'number of zones',
                'json_key': 'NoOfZones',
                'suffix': '',
            },
            {
                'setting_name': 'iZone system type',
                'json_key': 'SysType',
                'suffix': '',
            },
            {
                'setting_name': 'airflow adjustment allowed',
                'json_key': 'AirflowLock',
                'suffix': '',
            },
            {
                'setting_name': 'system locked',
                'json_key': 'UnitLocked',
                'suffix': '',
            },
        ]
        for setting in settings:
            get_system_setting(
                izone_device=izone_device,
                setting_name=setting['setting_name'],
                json_key=setting['json_key'],
                suffix=setting['suffix'],
                system_settings_dict=system_settings_dict,
            )
        get_zone(
            izone_device=izone_device,
            zone_to_get='all',
            include_default_named_zones=True,
        )

    # Handle "get fan"
    elif getattr(args, 'get_fan', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_system_setting(izone_device, 'fan', 'SysFan')

    # Handle "get mode"
    elif getattr(args, 'get_mode', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_system_setting(izone_device, 'mode', 'SysMode')

    # Handle "get power"
    elif getattr(args, 'get_power', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_system_setting(izone_device, 'power', 'SysOn')

    # Handle "get setpoint"
    elif getattr(args, 'get_setpoint', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_system_setting(
            izone_device=izone_device,
            setting_name='setpoint',
            json_key='Setpoint',
            suffix="°C")

    # Handle "get sleep"
    elif getattr(args, 'get_sleeptimer', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_system_setting(
            izone_device=izone_device,
            setting_name='sleep timer',
            json_key='SleepTimer',
            suffix="minutes")
        get_system_setting(izone_device, 'power', 'SysOn')

    # Handle "get zones"
    elif getattr(args, 'get_zones', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_zone(
            izone_device=izone_device,
            zone_to_get='all',
            include_default_named_zones=args.include_all_zones,
        )

    # Handle "get zone"
    # TODO: handle zones by name.
    # eg: if type(args.zone_number) = str, then do a lookup to return a zone number...
    elif getattr(args, 'get_zone', False):
        izone_device = sanitise_izone_device(args.izone_device)
        get_zone(
            izone_device=izone_device,
            zone_to_get=args.zone_number,
            include_default_named_zones=False,
        )

    # Handle "set fan ..."
    elif getattr(args, 'set_fan', False):
        izone_device = sanitise_izone_device(args.izone_device)
        try:
            error_on_non_empty_response(
                izone_device=izone_device,
                response=pyizone.set_system_fan(
                    izone_device,
                    args.fan_speed,
                ),
                verb='set',
                setting_name='fan',
            )
        except TimeoutError:
            if args.fan_speed == pyizone.FAN.MEDIUM:
                print(
                    "{izone_device}: WARNING: This device may not support '{fan_speed}' fan speed.".format(
                        izone_device=izone_device,
                        fan_speed=pyizone.FAN.MEDIUM,
                    ),
                    file=sys.stderr
                )
        get_system_setting(izone_device, 'fan', 'SysFan')

    # Handle "set mode ..."
    elif getattr(args, 'set_mode', False):
        izone_device = sanitise_izone_device(args.izone_device)
        error_on_non_empty_response(
                izone_device=izone_device,
                response=pyizone.set_system_mode(
                    izone_device,
                    args.mode,
                ),
                verb='set',
                setting_name='mode',
            )
        get_system_setting(izone_device, 'mode', 'SysMode')

    # Handle "set power ..."
    elif getattr(args, 'set_power', False):
        if args.power_state == "on":
            power_state = True
        else:
            power_state = False
        izone_device = sanitise_izone_device(args.izone_device)
        error_on_non_empty_response(
            izone_device=izone_device,
            response=pyizone.set_system_power(
                izone_device,
                power_state,
            ),
            verb='set',
            setting_name='power',
        )
        get_system_setting(izone_device, 'power', 'SysOn')

    # Handle "set setpoint ..."
    elif getattr(args, 'set_setpoint', False):
        izone_device = sanitise_izone_device(args.izone_device)
        error_on_non_empty_response(
            izone_device=izone_device,
            response=pyizone.set_system_setpoint(
                izone_device,
                args.temperature,
            ),
            verb='set',
            setting_name='setpoint',
        )
        get_system_setting(
            izone_device=izone_device,
            setting_name='setpoint',
            json_key='Setpoint',
            suffix="°C",
        )

    # Handle "set sleeptimer ..."
    elif getattr(args, 'set_sleeptimer', False):
        izone_device = sanitise_izone_device(args.izone_device)
        error_on_non_empty_response(
            izone_device=izone_device,
            response=pyizone.set_sleep(
                izone_device,
                args.minutes,
            ),
            verb='set',
            setting_name='sleep timer',
        )

    # Handle "set zone N mode ..."
    elif getattr(args, 'set_zone_mode', False):
        izone_device = sanitise_izone_device(args.izone_device)
        zone_mode = args.zone_mode
        if zone_mode == 'closed':
            zone_mode = 'close'
        pyizone.set_zone_mode(
            izone_device,
            args.zone_number,
            zone_mode,
        )
        get_zone(
            izone_device=izone_device,
            zone_to_get=args.zone_number,
            include_default_named_zones=False,
        )

    # Handle "set zone N airflow ..."
    elif getattr(args, 'set_zone_airflow', False):
        izone_device = sanitise_izone_device(args.izone_device)
        if args.min_max == 'min':
            pyizone.set_zone_min_airflow(
                izone_device,
                args.zone_number,
                args.airflow_percent,
            )
        if args.min_max == 'max':
            pyizone.set_zone_max_airflow(
                izone_device,
                args.zone_number,
                args.airflow_percent,
            )
        get_zone(
            izone_device=izone_device,
            zone_to_get=args.zone_number,
            include_default_named_zones=False,
        )

    # Second level parsers, must be handled after specific parsers and before root level parsers

    # Handle "set zone"
    elif getattr(args, 'set_zone', False):
        parser_set_zone.print_help()

    # Root level parsers, must be handled last

    # Handle "get"
    elif getattr(args, 'root_cmd_get', False):
        parser_get.print_help()

    # Handle "set"
    elif getattr(args, 'root_cmd_set', False):
        parser_set.print_help()

    else:
        parser.print_help()


# CLI utility
if __name__ == "__main__":
    main()

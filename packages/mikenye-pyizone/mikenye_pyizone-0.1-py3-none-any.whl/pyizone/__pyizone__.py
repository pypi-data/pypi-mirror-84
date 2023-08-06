#!/usr/bin/env python3

import socket
import time
import re
import logging
import json
import http.client
import ipaddress
import pycurl

# Import "Literal". This is only available in Python 3.8+.
# It has been backported to the 3rd party module "typing_extensions" for previous versions of Python.
try:
    from typing import Literal
except ImportError:
    logging.debug("Importing 'Literal' from 'typing_extensions'")
    from typing_extensions import Literal


# Globals
DISCOVERY_TIMEOUT_SECONDS = 5.0   # 5 seconds on local LAN should be more than sufficient
SOCKET_TIMEOUT_SECONDS = 1.0      # 1s to wait for a UDP response should be more than sufficient
GET_COMMAND_TIMEOUT = 5.0         # 5 second on local LAN should be more than sufficient
SET_COMMAND_TIMEOUT = 5.0         # 5 seconds on local LAN should be more than sufficient


# "Enum" classes
class MODE(object):
    """Valid settings for 'SystemMODE'"""
    COOL = "cool"
    HEAT = "heat"
    VENT = "vent"
    DRY = "dry"
    AUTO = "auto"


class FAN(object):
    """Valid settings for 'SystemFAN'"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"


class ZONECOMMAND(object):
    """Valid settings for 'ZoneCommand'"""
    OPEN = "open"
    CLOSE = "close"


class SLEEPTIMER(object):
    """Valid settings for 'SleepTimer'"""
    OFF = 0
    MINS_30 = 30
    MINS_60 = 60
    MINS_90 = 90
    MINS_120 = 120


class FREEAIR(object):
    """Valid settings for 'FreeAir'"""
    ON = "on"
    OFF = "off"


def discover(
        discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
        socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
        izone_cb_id=None,
) -> list:
    """
        Attempts discovery of iZone 1.x Controls Bridges (CB)

        Args:
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds
            izone_cb_id: (str) Look for a specific id only, and return as soon as it is found

        Returns:
            A list of dict objects containing the id (str), ipaddr (str) and port (str) of each CB discovered, eg:
            [{'ipaddr': '192.168.0.9', 'id': '000002323', 'port': '12107'}]
    """

    # Set up socket
    udp_sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP
        )

    # Set socket timeout
    udp_sock.settimeout(socket_timeout_seconds)

    # Configure socket for sending/receiving broadcast datagrams
    udp_sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BROADCAST, 1
        )

    # Send discovery datagram
    logging.debug("Sending IASD broadcast discovery datagram")
    udp_sock.sendto(
        b"IASD",
        ('<broadcast>', 12107)
    )

    # prepare compiled regex to break captured output into a dict for easy python processing
    regex_rawstring = r'^ASPort_(?P<port>\d{1,5}),\w*?_{0,1}(?P<id>\d+),IP_(?P<ipaddr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'
    regex_cb_response = re.compile(regex_rawstring)

    # Receive messages for up discovery_timeout_seconds
    logging.debug("Listening for discovery responses for %s seconds", discovery_timeout_seconds)
    responses = list()
    timeout = time.time() + discovery_timeout_seconds
    while True:
        response_datagram = None

        # Listen for replies from CBs up to socket_timeout_seconds...
        try:
            response_datagram = udp_sock.recvmsg(1024)
        except socket.timeout:
            # Don't throw an error on timeout as this is expected
            pass

        # If we get a response, let the user know & add to list of responses
        if response_datagram:

            # firstly, convert the response to a normal string
            response_str = str(response_datagram[0], 'utf-8')

            # Make sure we understand the result
            result = regex_cb_response.match(response_str)
            if result:

                # convert the result to a dict object
                response_dict = result.groupdict()
                logging.debug(
                    "Found iZone CB %s at %s:%s",
                    response_dict['id'],
                    response_dict['ipaddr'],
                    response_dict['port'],
                    )

                if izone_cb_id:
                    if response_dict['id'] == izone_cb_id:
                        # if a specific ID has been specified, return result immediately
                        responses.append(response_dict)
                        break
                    else:
                        # If looking for a specific ID, but this isn't it,
                        # don't add the discovered device to list of responses
                        continue
                else:
                    # If a specific ID hasn't been specified, add discovered device to list of responses
                    responses.append(response_dict)

            else:
                # Log a warning if the regex doesn't match.
                # Perhaps there are different versions that don't behave
                # exactly to spec that we may need to deal with in future...
                logging.warning(
                    "Could not interpret respose: '%s' from '%s:%s'",
                    response_str,
                    response_datagram[3][0],
                    response_datagram[3][1],
                    )

        # Break out of while loop on once discovery_timeout_seconds has passed
        if time.time() > timeout:
            break

    # Close our socket
    udp_sock.close()

    # Sanity check
    if len(responses) < 1:
        raise TimeoutError("No response from iZone CB")

    # TODO report on the capabilities of the unit, ie:
    #   - does it support FreeAir?

    # Return responses
    logging.debug("Discovery complete, found %s CB(s)", len(responses))
    return(responses)


def get_ipaddr(
        izone_cb: str,
        discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
        socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
        ) -> str:
    """
        Returns the IP address of an iZone 1.x Controls Bridge (CB) with a known ID

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds


        Returns:
            ipaddr (str) of the iZone 1.x CB

        Raises:
            TimeoutError: if id is not found within discovery_timeout_seconds
            IndexError: if more than one IP is returned (should never really happen)
    """

    # is izone_cb already have an IP address? if so, return it
    try:
        ipaddr = ipaddress.IPv4Address(izone_cb)
    except ValueError:
        pass
    else:
        return str(ipaddr)

    # if izone_cb is not an IP address, perform discovery
    results = discover(
        izone_cb_id=izone_cb,
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds,
        )

    if len(results) == 1:
        # We expect a single result to be returned from discover()
        # Return the IP address
        ipaddr = ipaddress.IPv4Address(results[0]['ipaddr'])
        logging.debug("iZone CB ID {izone_cb} has IPv4 address {ipaddr}".format(
            izone_cb=izone_cb,
            ipaddr=ipaddr,
        ))
        return str(ipaddr)

    # Deal with any wierd error scenarios
    elif len(results) > 1:
        # iZone protocol spec says every CB has a unique ID, so this should never happen
        raise IndexError("Expecting one IP address, got %s" % (len(results)))
    elif len(results) == 0:
        # TimeoutError should be raied by discover(), so this should never happen
        raise TimeoutError("No response from iZone CB %s" % (izone_cb))
    else:
        # Number of results should never be less than zero, so this should never happen
        raise Exception("Unknown error")


def _izone_api_get(
    izone_cb: str,
    api_endpoint: str,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Performs iZone CB API get operation

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            api_endpoint: (str) API Endpoint
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    # Get CB ipaddr
    ipaddr = get_ipaddr(
        izone_cb=izone_cb,
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds,
        )

    conn = http.client.HTTPConnection(
        ipaddr, 80,
        timeout=get_command_timeout
        )
    request = "/%s" % (api_endpoint)
    logging.debug("Performing GET to {ipaddr}:80{request}".format(
        ipaddr=ipaddr,
        request=request,
    ))
    conn.request("GET", request)
    response = conn.getresponse()

    logging.debug("Response code: {response_status}, type: {response_type}".format(
        response_status=response.status,
        response_type=response.getheader("Content-Type")
    ))

    if response.status == 200:
        if response.getheader("Content-Type") == "application/json":
            response_bytes = response.read()
            logging.debug("Response length: {response_bytes}".format(
                response_bytes=len(response_bytes),
            ))
            response_str = str(response_bytes, 'utf-8')
            response_dict = json.loads(response_str)
        else:
            raise Exception("Unexpected Content-Type: " % (response.getheader("Content-Type")))
    else:
        raise Exception("Unexpected status: " % (response.status))

    return(response_dict)


def _izone_api_set(
    izone_cb: str,
    api_endpoint: str,
    command_dict: dict,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Performs iZone CB API set operation

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            api_endpoint: (str) API Endpoint
            command_dict: (dict) A dict representing the JSON for the API request
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    # Prepare JSON body
    json_body = json.dumps(command_dict)

    # Get CB ipaddr
    ipaddr = get_ipaddr(
        izone_cb=izone_cb,
        discovery_timeout_seconds=DISCOVERY_TIMEOUT_SECONDS,
        socket_timeout_seconds=SOCKET_TIMEOUT_SECONDS,
        )

    # Use cURL to perform POST
    # iZone doesn't like http.client or requests :(
    raw_response_body = list()
    raw_response_headers = list()
    c = pycurl.Curl()
    url = "http://%s/%s" % (ipaddr, api_endpoint)
    logging.debug("Performing curl POST to {url}".format(
        url=url,
    ))
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, json_body)
    c.setopt(pycurl.WRITEFUNCTION, raw_response_body.append)
    c.setopt(pycurl.HEADERFUNCTION, raw_response_headers.append)
    c.perform()
    response_status = c.getinfo(pycurl.RESPONSE_CODE)
    c.close()

    # Split headers out into dictionary
    response_headers = dict()
    for raw_header in raw_response_headers:
        if raw_header.count(b':'):
            raw_header_split = raw_header.split(b":")
            key = str(raw_header_split[0].strip(), 'utf-8')
            val = str(raw_header_split[1].strip(), 'utf-8')
            response_headers[key] = val

    logging.debug("Response code: {response_status}, type: {response_type}".format(
        response_status=response_status,
        response_type=response_headers["Content-Type"],
    ))

    # Split body out into a BytesIO
    response_bytes = b''
    for line in raw_response_body:
        response_bytes += line

    logging.debug("Response length: {response_bytes}".format(
        response_bytes=len(response_bytes),
    ))

    # Check response code
    if response_status == 200:
        if "Content-Type" in response_headers.keys():
            if response_headers["Content-Type"] == "application/json":
                response_str = str(response_bytes, 'utf-8')

                # For many (all?) set requests, the unit just returns an empty body, this prevents json decoder errors
                if response_str != '':
                    response_dict = json.loads(response_str)
                else:
                    response_dict = {}
            else:
                raise Exception("Unexpected Content-Type: %s" % (response_headers["Content-Type"]))
        else:
            raise Exception("Unexpected Headers: %s" % (repr(response_headers)))
    else:
        raise Exception("Unexpected status: %s" % (repr(response_status)))

    return(response_dict)


def get_system_settings(
    izone_cb: str,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Returns iZone CB API system settings

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_izone_api_get(
        izone_cb=izone_cb,
        api_endpoint="SystemSettings",
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds,
        ))


def get_zones(
    izone_cb: str,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Returns iZone CB API zone settings

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            get_command_timeout: (str) API Endpoint
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    zone_endpoints = (
        'Zones1_4',
        'Zones5_8',
        'Zones9_12',
    )

    output = dict()

    for zone_endpoint in zone_endpoints:
        for zone in _izone_api_get(
            izone_cb=izone_cb,
            api_endpoint=zone_endpoint,
        ):
            output[zone['Index']+1] = zone

    return(output)


def get_schedules(
    izone_cb: str,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> list:

    """
        Returns iZone CB API schedule settings

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    sched_endpoints = (
        'Schedules1_5',
        'Schedules6_9',
    )

    output = list()

    for sched_endpoint in sched_endpoints:
        for sched in _izone_api_get(
            izone_cb=izone_cb,
            api_endpoint=sched_endpoint,
        ):
            output.append(sched)

    return(output)


def _set_system_setting(
    izone_cb: str,
    api_endpoint: str,
    system_setting_key: str,
    system_setting_check_key: str,
    system_setting_desired_value: str,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB API system setting

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            api_endpoint: (str) API Endpoint
            system_setting_key: (str) The key of the system setting to change
            system_setting_check_key: (str) the key from get_zones() to query to ensure system_setting_desired_value is set
            system_setting_desired_value: (str) The desired value we want to set the key to
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    response = {}

    # check to see if the system is already in the desired state
    current_system_settings = get_system_settings(izone_cb=izone_cb)
    if current_system_settings[system_setting_check_key] == system_setting_desired_value:
        logging.debug("iZone CB %s is already %s", izone_cb, system_setting_desired_value)

    else:

        # Power the system to desired_state
        response = _izone_api_set(
            izone_cb=izone_cb,
            api_endpoint=api_endpoint,
            command_dict={system_setting_key: system_setting_desired_value},
        )

        # Wait for the system to report it is on
        timeout = time.time() + set_command_timeout
        while True:

            # Wait for the system to respond
            time.sleep(0.25)

            # Check current status
            current_system_settings = get_system_settings(izone_cb=izone_cb)
            if current_system_settings[system_setting_check_key] == system_setting_desired_value:
                break

            # Raise a TimeoutError when set_command_timeout has passed
            if time.time() > timeout:
                # TimeoutError should be raied by discover(), so this should never happen
                raise TimeoutError("Timeout waiting for new settings to be reflected from iZone CB %s" % (izone_cb))

    return(response)


def set_system_power(
    izone_cb: str,
    system_power: bool,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB API system power setting (turning the unit on/off)

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            system_power: (bool) True to power on the unit, False to power off the unit
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    if system_power:
        desired_state = "on"
    else:
        desired_state = "off"

    return(_set_system_setting(
        izone_cb=izone_cb,
        api_endpoint="SystemON",
        system_setting_key="SystemON",
        system_setting_check_key="SysOn",
        system_setting_desired_value=desired_state,
        ))


def set_system_mode(
    izone_cb: str,
    system_mode: Literal[
        MODE.COOL,
        MODE.HEAT,
        MODE.VENT,
        MODE.DRY,
        MODE.AUTO,
    ],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB API system operating mode (heating/cooling/vent/dry/auto)

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            system_mode: (pyizone.MODE) pyizone.MODE.COOL / pyizone.MODE.HEAT / pyizone.MODE.VENT /
                                        pyizone.MODE.DRY / pyizone.MODE.AUTO
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_set_system_setting(
        izone_cb=izone_cb,
        api_endpoint="SystemMODE",
        system_setting_key="SystemMODE",
        system_setting_check_key="SysMode",
        system_setting_desired_value=system_mode,
        ))


def set_system_fan(
    izone_cb: str,
    system_fan: Literal[
        FAN.LOW,
        FAN.MEDIUM,
        FAN.HIGH,
        FAN.AUTO,
        ],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB API system fan speed (low, medium (if supported), high, auto)

        Not all systems support "medium" fan mode. If "medium" is set on these systems, the iZone CB may change to "high".

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            system_fan: (pyizone.FAN) pyizone.FAN.COOL / pyizone.FAN.HEAT / pyizone.FAN.VENT /
                                      pyizone.FAN.DRY / pyizone.FAN.AUTO
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_set_system_setting(
        izone_cb=izone_cb,
        api_endpoint="SystemFAN",
        system_setting_key="SystemFAN",
        system_setting_check_key="SysFan",
        system_setting_desired_value=system_fan,
        ))


def set_system_setpoint(
    izone_cb: str,
    system_setpoint: float,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB API system temperature setpoint

        Setpoint will be rounded to nearest half degree.
        Not all systems support this resolution, and the iZone CB may round the temperature down to the nearest degree.

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            system_setpoint: (float) system temperature setpoint in degrees celcius
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON

        Raises:
            ValueError: in the event that EcoMode is enabled, and the requested system_setpoint is outside EcoMin/EcoMax
    """

    system_setpoint_rounded = round(0.5 * round(float(system_setpoint)/0.5), 1)
    if system_setpoint_rounded != system_setpoint:
        logging.debug("Setpoint rounded to: {setpoint}".format(
            setpoint=system_setpoint_rounded,
        ))

    # Get current system settings
    settings = _izone_api_get(
        izone_cb=izone_cb,
        api_endpoint="SystemSettings",
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds,
        )

    if settings['EcoLock'] == 'true':
        logging.debug("EcoLock is enabled, min: {min}, max: {max}".format(
            min=settings['EcoMin'],
            max=settings['EcoMax'],
        ))
        if (system_setpoint < float(settings['EcoMin'])) or (system_setpoint > float(settings['EcoMax'])):
            raise ValueError(
                "EcoLock enabled, requested setpoint of '%s' outside of EcoMax/EcoMin (%s/%s)" % (
                    system_setpoint,
                    settings['EcoMin'],
                    settings['EcoMax'],
                    ))

    return(_set_system_setting(
        izone_cb=izone_cb,
        api_endpoint="UnitSetpoint",
        system_setting_key="UnitSetpoint",
        system_setting_check_key="Setpoint",
        system_setting_desired_value=str(system_setpoint_rounded),
        ))


def _zone_command(
    izone_cb: str,
    api_endpoint: Literal["ZoneCommand", "AirMinCommand", "AirMaxCommand"],
    zone_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    zone_setting_key: Literal["ZoneCommand", "AirMinCommand", "AirMaxCommand"],
    zone_setting_check_key: str,
    zone_setting_desired_value: str,
    set_command_timeout=SET_COMMAND_TIMEOUT,
    get_command_timeout=GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds=DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds=SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB zone settings

          - api_endpoint/zone_setting_key of "ZoneCommand" for open/close
          - api_endpoint/zone_setting_key of "AirMinCommand" to set minimum zone airflow
          - api_endpoint/zone_setting_key of "AirMaxCommand" to set maximum zone airflow

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            api_endpoint: (str) see above: "ZoneCommand", "AirMinCommand", "AirMaxCommand"
            zone_number: (int) The zone number. Valid zones are 1-12.
            zone_setting_key: (str) see above: "ZoneCommand", "AirMinCommand", "AirMaxCommand"
            zone_setting_check_key: (str) the key from get_zones() to query to ensure zone_setting_desired_value is set
            zone_setting_desired_value: (str) the desired value of zone_setting_key / zone_setting_check_key
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON

        Raises:
            TimeoutError: in the event that set_command_timeout is exceeded waiting for new settings to be reflected
    """

    response = {}

    zones = get_zones(
        izone_cb=izone_cb,
    )

    # check to see if the system is already in the desired state
    if zones[zone_number][zone_setting_check_key] == zone_setting_desired_value:
        logging.debug("iZone CB %s zone %s is already %s", izone_cb, zone_number, zone_setting_desired_value)

    else:

        response = _izone_api_set(
            izone_cb=izone_cb,
            api_endpoint=api_endpoint,
            command_dict={
                zone_setting_key: {
                    "ZoneNo": str(zone_number),
                    "Command": str(zone_setting_desired_value),
                }},
            )

        # Wait for the system to report it is on
        timeout = time.time() + set_command_timeout
        while True:

            # Wait for the system to respond
            time.sleep(0.25)

            zones = get_zones(
                izone_cb=izone_cb,
                )

            # check to see if the system is already in the desired state
            if zones[zone_number][zone_setting_check_key] == zone_setting_desired_value:
                break

            # Raise a TimeoutError when set_command_timeout has passed
                if time.time() > timeout:
                    # TimeoutError should be raied by discover(), so this should never happen
                    raise TimeoutError("Timeout waiting for new settings to be reflected from iZone CB %s" % (izone_cb))

    return(response)


def set_zone_mode(
    izone_cb: str,
    zone_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    zone_mode: Literal[
        ZONECOMMAND.OPEN,
        ZONECOMMAND.CLOSE,
    ],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB zone mode (open/close)

        Args:
            izone_cb: (str) ID of an iZone 1.x CB
            zone_number: (int) The zone number. Valid zones are 1-12.
            zone_mode: (pyizone.ZONECOMMAND) pyizone.ZONECOMMAND.OPEN / pyizone.ZONECOMMAND.CLOSE
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON

        Raises:
            TimeoutError: in the event that set_command_timeout is exceeded waiting for new settings to be reflected
    """

    return(_zone_command(
        izone_cb=izone_cb,
        api_endpoint="ZoneCommand",
        zone_number=zone_number,
        zone_setting_key="ZoneCommand",
        zone_setting_check_key="Mode",
        zone_setting_desired_value=zone_mode,
    ))


def set_zone_min_airflow(
    izone_cb: str,
    zone_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    zone_airflow: int,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB zone minimum airflow

        zone_airflow will be rounded to nearest 5(%).

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            zone_number: (int) The zone number. Valid zones are 1-12.
            zone_airflow: (int) 0-100(%) in increments of 5.
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    zone_airflow_rounded = round(5 * round(float(zone_airflow)/5), 5)
    if zone_airflow_rounded > 100:
        zone_airflow_rounded = 100
    if zone_airflow_rounded < 0:
        zone_airflow_rounded = 0
    if zone_airflow != zone_airflow_rounded:
        logging.debug("Airflow rounded to: {airflow}".format(
            airflow=zone_airflow_rounded,
        ))

    zones = get_zones(izone_cb)
    if zone_airflow_rounded >= zones[zone_number]['MaxAir']:
        raise ValueError(
            "Zone MinAir must be less than zone MaxAir"
        )

    return(_zone_command(
        izone_cb=izone_cb,
        api_endpoint="AirMinCommand",
        zone_number=zone_number,
        zone_setting_key="AirMinCommand",
        zone_setting_check_key="MinAir",
        zone_setting_desired_value=zone_airflow_rounded,
    ))


def set_zone_max_airflow(
    izone_cb: str,
    zone_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    zone_airflow: int,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Changes iZone CB zone maximum airflow

        zone_airflow will be rounded to nearest 5(%).

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            zone_number: (int) The zone number. Valid zones are 1-12.
            zone_airflow: (int) 0-100(%) in increments of 5.
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    zone_airflow_rounded = round(5 * round(float(zone_airflow)/5), 5)
    if zone_airflow_rounded > 100:
        zone_airflow_rounded = 100
    if zone_airflow_rounded < 0:
        zone_airflow_rounded = 0
    if zone_airflow != zone_airflow_rounded:
        logging.debug("Airflow rounded to: {airflow}".format(
            airflow=zone_airflow_rounded,
        ))

    zones = get_zones(izone_cb)
    if zone_airflow_rounded <= zones[zone_number]['MinAir']:
        raise ValueError(
            "Zone MaxAir must be greater than zone MinAir"
        )

    return(_zone_command(
        izone_cb=izone_cb,
        api_endpoint="AirMaxCommand",
        zone_number=zone_number,
        zone_setting_key="AirMaxCommand",
        zone_setting_check_key="MaxAir",
        zone_setting_desired_value=zone_airflow_rounded,
    ))


def set_favourite(
    izone_cb: str,
    favourite_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Applys settings defined by a favourite

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            favourite_number: (int) The favourite number. Valid favourites are 1-9.
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_izone_api_set(
        izone_cb=izone_cb,
        api_endpoint="FavouriteSet",
        command_dict={"FavouriteSet": "%s" % (favourite_number)},
        set_command_timeout=set_command_timeout,
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds
    ))


def set_schedule(
    izone_cb: str,
    schedule_number: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9],
    schedule_enabled: bool,
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Enables/Disables a schedule

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            schedule_number: (int) The schedule number. Valid schedules are 1-9.
            schedule_enabled: (bool) True to enable the schedule, False to disable the schedule
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON

        Raises:
            TimeoutError: in the event that set_command_timeout is exceeded waiting for new settings to be reflected
    """

    schedules = get_schedules(
        izone_cb=izone_cb,
        )

    command_dict = {"ScheduleCommand": {
        "SchedNo": "%s" % (schedule_number),
        }}

    if schedule_enabled:
        command_dict["ScheduleCommand"]["Command"] = "on"
        desired_state = "true"
    else:
        command_dict["ScheduleCommand"]["Command"] = "off"
        desired_state = "false"

    for schedule in schedules:
        if schedule['Index'] == (schedule_number - 1):
            if schedule['Active'] == desired_state:
                logging.debug(
                    "iZone CB %s schedule %s is already %s",
                    izone_cb,
                    schedule_number,
                    command_dict["ScheduleCommand"]["Command"]
                )
            else:
                response = _izone_api_set(
                    izone_cb=izone_cb,
                    api_endpoint="ScheduleCommand",
                    command_dict=command_dict,
                    set_command_timeout=set_command_timeout,
                    discovery_timeout_seconds=discovery_timeout_seconds,
                    socket_timeout_seconds=socket_timeout_seconds
                )

                # Wait for the system to report success
                timeout = time.time() + set_command_timeout

                setting_applied = False
                while not setting_applied:

                    # Wait for the system to respond
                    time.sleep(0.25)

                    schedules = get_schedules(
                        izone_cb=izone_cb,
                    )

                    for schedule in schedules:
                        if schedule['Index'] == (schedule_number - 1):
                            if schedule['Active'] == desired_state:
                                setting_applied = True

                    # Raise a TimeoutError when set_command_timeout has passed
                    if time.time() > timeout:
                        # TimeoutError should be raied by discover(), so this should never happen
                        raise TimeoutError("Timeout waiting for new settings to be reflected from iZone CB %s" % (izone_cb))

    return(response)


def set_sleep(
    izone_cb: str,
    sleep_timer: Literal[
        SLEEPTIMER.OFF,
        SLEEPTIMER.MINS_30,
        SLEEPTIMER.MINS_60,
        SLEEPTIMER.MINS_90,
        SLEEPTIMER.MINS_120,
    ],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    get_command_timeout: float = GET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Sets the sleep timer

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            sleep_timer: (pyizone.SLEEPTIMER) pyizone.SLEEPTIMER.OFF / pyizone.SLEEPTIMER.MINS_30 / pyizone.SLEEPTIMER.MINS_60
                                              / pyizone.SLEEPTIMER.MINS_90 / pyizone.SLEEPTIMER.MINS_120
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_set_system_setting(
        izone_cb=izone_cb,
        api_endpoint="SleepTimer",
        system_setting_key="SleepTimer",
        system_setting_check_key="SleepTimer",
        system_setting_desired_value=int(sleep_timer),
        set_command_timeout=set_command_timeout,
        get_command_timeout=get_command_timeout,
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds,
    ))


def set_freeair(
    izone_cb: str,
    freeair_mode: Literal[
        FREEAIR.OFF,
        FREEAIR.ON,
    ],
    set_command_timeout: float = SET_COMMAND_TIMEOUT,
    discovery_timeout_seconds: float = DISCOVERY_TIMEOUT_SECONDS,
    socket_timeout_seconds: float = SOCKET_TIMEOUT_SECONDS,
) -> dict:

    """
        Sets the free air mode

        Args:
            izone_cb: (str) IPv4 address or numeric ID of an iZone 1.x CB
            freeair_mode: (pyizone.FREEAIR) pyizone.FREEAIR.OFF / pyizone.FREEAIR.ON
            set_command_timeout: (float) Number of seconds to wait for CBs to respond for API set requests
            get_command_timeout: (float) Number of seconds to wait for CBs to respond for API get requests
            discovery_timeout_seconds: (float) Number of seconds to wait for CBs to respond after sending discovery datagram
            socket_timeout_seconds: (float) Socket timeout in number of seconds

        Returns:
            response (dict): dict from response JSON
    """

    return(_izone_api_set(
        izone_cb=izone_cb,
        api_endpoint="FreeAir",
        command_dict={"FreeAir": "%s" % (freeair_mode)},
        set_command_timeout=set_command_timeout,
        discovery_timeout_seconds=discovery_timeout_seconds,
        socket_timeout_seconds=socket_timeout_seconds
    ))

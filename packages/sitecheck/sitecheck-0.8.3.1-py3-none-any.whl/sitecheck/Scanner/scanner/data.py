"""
    Geo-Instruments
    Sitecheck Scanner
    Data handler Package for Scanner

"""
import json
import os
from pathlib import Path

import paho.mqtt.client as paho

from . import utlis
from . import logger
from . import options

client = paho.Client("qv", clean_session=True)
client.connect("3.134.3.199", 1884)


def check_mode(sensor: object) -> object:
    """
    Pauses run to give observer the chance to look at the information before proceeding.

    :return: Wait for input
    :rtype: object
    """
    return
    if os.environ['Repl']:
        logger.log(f'{sensor} is missing data')
        return input(
            "Pausing run for eval.\nPress Enter to continue...")


async def watchdog_handler(diff, project_name, sensor, last_updated):
    """
    Handles sorting sensor watchdog status.

    Timeesamps from last update are sorted into three categories:
    Up-to-date, Behind, Old

    :param diff: Time since last reading
    :type diff: int

    :param project_name: Name of Project
    :type project_name: str

    :param sensor: Sensor ID
    :type sensor: str

    :param last_updated: Formatted Date string
    :type last_updated: str
    """
    # Sensor is Up-to-date.
    if diff <= options.Watchdog:
        data_list = [sensor, 'good', 'Up-to-date', last_updated]
        if options.PrintNew:
            logger.info(data_list)
            store(project_name, data_list)
        else:
            logger.debug(data_list)
            
    # Sensor is Behind.
    elif options.Watchdog <= diff <= options.Oldperiod:
        data_list = [
            sensor,
            'warning',
            'Older than %s hours' % options.args.time,
            last_updated
            ]
        store(project_name, data_list)
        logger.info(data_list)
        check_mode(sensor)
    # Sensor is Old. Assumes after a week that this is a known issue.
    else:
        data_list = [sensor, 'attention', 'Older than a week', last_updated]
        if options.PrintOld:
            logger.info(data_list)
            store(project_name, data_list)
            check_mode(sensor)
        else:
            logger.debug(data_list)


def post(topic, payload):
    """
    Post results to MQTT broker for processing
    :param topic: Project name
    :param payload: Sensor Data
    """
    topic = str(f'Scanner/lists/{topic}.txt')
    payload = str(payload)
    try:
        client.publish(topic, payload)
        logger.debug(f"pub: {topic}=:={payload}")
    except ValueError:
        logger.info(f"pub Failed because of wildcard: {str(topic)}=:={str(payload)}")
        logger.info(f"Attempting fix...")
        try:
            tame_t = topic.replace("+", "_")
            tame_topic = tame_t.replace("#", "_")
            tame_p = payload.replace("+", "_")
            tame_payload = tame_p.replace("#", "_")
            client.publish(str(tame_topic), str(tame_payload))
            logger.info(f"Fix successful, Sending data...")
            logger.debug(f"pub: {topic}=:={payload}")
        except Exception as error:
            logger.info(f"Fix Failed. Bug report sent.")
            client.publish("error", str(error))


def store(project, data_list):
    """
    Sensor Data storage function

    :param project:	Project name
    :type project: str

    :param data_list: Sensor data in list format
                Examples: ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']
    :type data_list: list

    :rtype: None
    """
    
    store_path = Path(f"{os.environ['Output']}"
                      f"//data"
                      f"//{os.environ['filedate']}"
                      f"//{project}.txt")
    utlis.ensure_exists(store_path)
    with open(store_path, 'a') as file:
        if not file.tell():
            file.write('[')
        else:
            file.write(',')
        file.write(json.dumps(data_list))
        post(project, data_list)

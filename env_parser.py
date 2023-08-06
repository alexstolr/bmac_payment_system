from os.path import dirname, join

from dotenv import load_dotenv
import os
import sys

import constants

configured = False


def load_env():
    global configured
    if configured is True:
        return
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    set_constants()
    configured = True


def get_env_var(env_var: str) -> str:
    if configured is False:
        load_env()
    return os.getenv(env_var)


def set_constants():
    constants.BMAC_LINK = os.environ.get('BMAC_LINK')

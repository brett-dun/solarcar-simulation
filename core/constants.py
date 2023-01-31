"""
Module for representing universal constants.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


import datetime


unix_epoch: datetime.datetime = datetime.datetime.utcfromtimestamp(0)


gps_epoch: datetime.datetime = datetime.datetime(1980, 1, 6)


GAS_CONSTANT = 8.314462175  # <joule/(kelvin * mol)>

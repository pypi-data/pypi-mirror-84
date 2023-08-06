# -*- coding: utf-8 -*-
from pylicensemanager.internal import HelperMethods


class ActivatedMachine:
    def __init__(self, IP, Mid, Time, FriendlyName=""):
        self.IP = IP
        self.Mid = Mid

        # TODO: check if time is int, and convert to datetime in this case.
        self.Time = Time
        self.FriendlyName = FriendlyName

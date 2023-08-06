# -*- coding: utf-8 -*-
import platform
import random
import uuid
import sys
from pylicensemanager.internal import HelperMethods
from pylicensemanager.models import *
import json
from urllib.error import URLError, HTTPError


class Key:
    """
    generates and returns a 25 char key like: 2ILH-QWN7-2G2O-L1K2-2MNO
    courtesy of https://www.youtube.com/watch?v=IArt2Fgv644
    """

    def __init__(self, key=''):
        if key == '':
            self.key = self.generate()
        else:
            self.key = key.lower()

    def verify(self):
        score = 0
        check_digit = self.key[0]
        check_digit_count = 0
        chunks = self.key.split('-')
        for chunk in chunks:
            if len(chunk) != 4:
                return False
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        if score == 1772 and check_digit_count == 5:
            return True
        return False

    def generate(self):
        key = ''
        chunk = ''
        check_digit_count = 0
        alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
        while True:
            while len(key) < 25:
                char = random.choice(alphabet)
                key += char
                chunk += char
                if len(chunk) == 4:
                    key += '-'
                    chunk = ''
            key = key[:-1]
            if Key(key).verify():
                return key
            else:
                key = ''

    def __str__(self):
        valid = 'Invalid'
        if self.verify():
            valid = 'Valid'
        return self.key.upper()


class Helpers:

    @staticmethod
    def GetMachineCode(v=1):

        """
        Get a unique identifier for this device. If you want the machine code to be the same in .NET on Windows, you
        can set v=2. More information is available here: https://help.cryptolens.io/faq/index#machine-code-generation
        """

        if "windows" in platform.platform().lower():
            return HelperMethods.get_SHA256(
                HelperMethods.start_process(["cmd.exe", "/C", "wmic", "csproduct", "get", "uuid"], v))
        elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():
            res = HelperMethods.start_process(["system_profiler", "SPHardwareDataType"])
            return HelperMethods.get_SHA256(res[res.index("UUID"):].strip())
        elif "linux" in platform.platform().lower():
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
        else:
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())

    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license=False, allow_overdraft=False, v=1):

        """
        Check if the device is registered with the license key.
        The version parameter is related to the one in GetMachineCode method.
        """

        current_mid = Helpers.GetMachineCode(v)

        if license_key.activated_machines is None:
            return False

        if is_floating_license:
            if len(license_key.activated_machines) == 1 and \
                    (license_key.activated_machines[0].Mid[9:] == current_mid or allow_overdraft and license_key.activated_machines[0].Mid[19:] == current_mid):
                return True
        else:
            for act_machine in license_key.activated_machines:
                if current_mid == act_machine.Mid:
                    return True

        return False

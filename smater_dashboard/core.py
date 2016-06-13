"""
This is the core module of smarterdashboard
If any of the base of comms changes it should be
implemented here and not hard coded anywhere else!!!

We really shouldn't be using network tables from now on...

Team 5431 - Titan Robotics
"""
from networktables import NetworkTable


class Core:
    """
    Super class was acting up so we assigned NetworkTables as an object
    No clue what provider meant so this was easier
    """
    def __init__(self, table_key="5431"):
        self.table_key = table_key
        self.table = NetworkTable.getTable(self.table_key)

    def get_num(self, key, types=float, default=-1.12):
        return types(self.table.getNumber(key, default))

    def get_str(self, key, default=""):
        return str(self.table.getString(key, default))

    def get_bool(self, key, default=False):
        return bool(self.table.getBoolean(key, default))

    def set_num(self, key, num):
        self.table.putNumber(key, num)

    def set_str(self, key, string):
        self.table.putString(key, str(string))

    def set_bool(self, key, boolean):
        self.table.putBoolean(key, bool(boolean))

    def check_key(self, key):
        return self.table.containsKey(key)

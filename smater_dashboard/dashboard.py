"""
This is for the dashboard instan
"""
from .core import Core


class DashBoard(Core):
    def __init__(self):
        super().__init__()
        self.update_verbose = 1

    def drive_base(self, left, right):
        if self.update_verbose > 0:
            self.set_num("left-drive", left)
            self.set_num("right-drive", right)

    def shoot_rpms(self, left, right):
        if self.update_verbose > 0:
            self.set_num("left-fly", left)
            self.set_num("right-fly", right)

    def chopper_state(self, state):
        if self.update_verbose > 0:
            self.set_bool("chopper", state)

    def drive_distance(self, left, right):
        if self.update_verbose > 1:
            self.set_num("left-drive-distance", left)
            self.set_num("right-drive-distance", right)

    def manual_mode(self, state):
        if self.update_verbose > 1:
            self.set_bool("manual-mode", state)

    def intake_state(self, state):
        if self.update_verbose > 0:
            self.set_num("intake", state)
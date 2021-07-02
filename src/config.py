#!/usr/bin/env python3

import os


class Config:

    def __init__(self):
        self.config_dir = os.path.expanduser("~/.dedup")
        os.makedirs(self.config_dir, exist_ok=True)

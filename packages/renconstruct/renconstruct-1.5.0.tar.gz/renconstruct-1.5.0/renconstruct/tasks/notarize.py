### System ###
import os
from glob import glob
from subprocess import Popen, PIPE, STDOUT

### Logging ###
from renconstruct import logger

### Parsing ###
import yaml


class NotarizeTask:

    # The higher priority, the earlier the task runs
    # This is relative to all other enabled tasks
    PRIORITY = 0

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.active = config["build"]["mac"]

    def post_build(self):
        if not self.active:
            return

        with open("renotize.yml", "w") as f:
            f.write(yaml.dump(self.config["renotize"]))

        mac_zip = glob(os.path.join(self.config["output"], "*-mac.zip"))[0]

        cmd = "renotize -c renotize.yml {} full-run".format(mac_zip)
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in proc.stdout:
            line = str(line.strip(), "utf-8")
            if line:
                logger.debug(line)

        os.remove("renotize.yml")

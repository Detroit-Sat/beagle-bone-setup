#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, subprocess
from getpass import getuser
from shutil import copyfile

def systemd_setup():
    try:
        with open("/dev/null","w") as out:
            subprocess.call(['systemctl'],stdout=out)
    except OSError:
        return False

    cwd = os.getcwd()
    enable_pin_bash_dest = cwd+"/enable-i2c-pins.sh"
    copyfile(cwd+"/support_files/enable-i2c-pins.service", "/lib/systemd/system/enable-i2c-pins.service")
    copyfile(cwd+"/support_files/enable-i2c-pins.sh", enable_pin_bash_dest)
    os.chmod(enable_pin_bash_dest, 0755)
    with open("/dev/null","w") as out:
        subprocess.call(['systemctl','daemon-reload'],stdout=out)
        subprocess.call(['systemctl','enable','enable-i2c-pins.service'],stdout=out)
    return True

if __name__ == "__main__":
    if getuser() != 'root':
        print("Must be run as root...")
        exit(1)

    if systemd_setup():
        print("Finished systemd setup")
        run = input("All set, run now and test? [y/n]:")
        if run.lower() in ["y", "yes"]:
            subprocess.call(['systemctl','start','enable-i2c-pins.service'])
            subprocess.call(['config-pin','-q','p9.17'])
            subprocess.call(['config-pin','-q','p9.18'])
    else:
        print("Installation on non-systemd linux is not supported...Exiting")
exit(1)
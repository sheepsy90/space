#!/usr/bin/env python
import os
import sys


def perform_basic_setup():
    from lib.setup.Setup import Setup
    Setup()

def main():
    # Import the django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webtool.settings")

    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        perform_basic_setup()
    elif len(sys.argv) == 4 and sys.argv[2] == "-C":
        os.environ["LOOTGAME_CONF_PATH"] = sys.argv[3]
        sys.argv = sys.argv[0:2]
    else:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()

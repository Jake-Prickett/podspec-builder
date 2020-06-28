#!/usr/bin/env python
"""
 build_podspec.py

 Intent:
      - Simplify the process of generating .podspec files
      - Easily generate and push to Private Pod Repo
      - No longer required to keep as part of Repo

 usage: build_podspec.py [-h] [-u] [-l] version

 positional arguments:
   version

 optional arguments:
   -h, --help    show this help message and exit
   -u, --upload  Determines if the newly built Podspec files should be pushed.
   -l, --local   Generate the podspec files and store them in the project
                 directory. NOTE: You are unable to push if this option is set.

 Simply run the script and provide a version, the rest will be done for you by
      scanning the project.yml to detect internal dependencies and add 3rd party
      libraries into the Podspec automatically

 If you would like to generate Pods for local development (from a consuming Application),
      leverage the --local option, and it will place the .podspec files right in the
      main directory

 Jake Prickett - May 2020
"""

import os
import random
import string
import argparse
from podmanager import PodManager

def main():
    """
    Responsible for parsing command line arguments and
    configuring the PodManager properly.
    """
    # Setup
    parser = argparse.ArgumentParser(description='Build Podspec Files.')

    parser.add_argument(
        '-u',
        '--upload',
        action='store_true',
        help='Determines if the newly built Podspec files should be pushed.'
        )

    parser.add_argument(
        '-l',
        '--local',
        action='store_true',
        help='Generate the podspec files and store them in the project directory.\nNOTE: You are unable to push if this option is set.'
        )

    parser.add_argument('version')

    args = parser.parse_args()

    should_publish = args.upload and not args.local
    version = args.version

    if args.local:
        # Store generated .podspec files in the current directory
        path = os.getcwd()
    else:
        # Creates temp folder /tmp/.podspecsXXXXXX for storage
        #    XXXXXX is a random alpha numeric string to ensure we don't have duplicates
        path = "/tmp/.podspecs" + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        os.mkdir(path)

    pod_manager = PodManager(path, version, should_publish)

    # Execute

    print("Building podspecs in %s\n" % path)

    pod_manager.detect_pods()
    pod_manager.go()

if __name__ == "__main__":
    main()
    
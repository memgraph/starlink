"""
simulator

Usage:
    main.py start
    main.py -h | --help

Arguments:
    -h --help   Shows this screen.
    NAME    Any random string
"""

import re
import sys
import logging
from typing import Dict, Any

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('simulator')
logger.setLevel(logging.INFO)

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


def _start() -> None:
    from simulator import starlink
    starlink.run()

def main(args: Dict[str, Any]) -> None:
    if args['start']:
        return _start()

 
if __name__ == '__main__':
    sys.excepthook = my_handler
    from docopt import docopt
    args = docopt(__doc__)
    main(args)

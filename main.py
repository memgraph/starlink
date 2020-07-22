"""
starlink_simulator

Usage:
    main.py start NAME
    main.py -h | --help

Arguments:
    -h --help   Shows this screen.
    NAME    Set name to print out
"""

import re
import logging
from typing import Dict, Any

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('starlink_simulator')
logger.setLevel(logging.INFO)


def _start(name: str) -> None:
    from starlink_simulator import start
    start(name)

def main(args: Dict[str, Any]) -> None:
    if args['start']:
        return _start(args['NAME'])


if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    main(args)

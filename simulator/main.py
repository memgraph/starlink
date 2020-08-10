"""
simulator

Usage:
    main.py start NAME
    main.py -h | --help

Arguments:
    -h --help   Shows this screen.
    NAME    Any random string
"""

import re
import logging
from typing import Dict, Any

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('simulator')
logger.setLevel(logging.INFO)


def _start(name: str) -> None:
    from src.start import start
    start(name)

def main(args: Dict[str, Any]) -> None:
    if args['start']:
        return _start(args['NAME'])

 
if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    main(args)

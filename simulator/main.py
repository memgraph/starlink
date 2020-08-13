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
import logging
from typing import Dict, Any

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('simulator')
logger.setLevel(logging.INFO)


def _start() -> None:
    from simulator import starlink
    starlink.run()

def main(args: Dict[str, Any]) -> None:
    if args['start']:
        return _start()

 
if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    main(args)

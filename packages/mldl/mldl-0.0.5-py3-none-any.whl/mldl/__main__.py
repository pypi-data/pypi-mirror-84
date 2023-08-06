"""
MLDL module entry point
"""
import sys
from .cli.cli_main import main

if __name__ == '__main__':
    main(sys.argv[1:])

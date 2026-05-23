import argparse
import asyncio
from pathlib import Path
from py_server.main import main

parser = argparse.ArgumentParser()
parser.add_argument("mode", nargs="?", default="stdio", choices=["stdio", "http"])
parser.add_argument("--env-file", type=str, default=None)
args = parser.parse_args()

asyncio.run(main(env_file=args.env_file, mode=args.mode))
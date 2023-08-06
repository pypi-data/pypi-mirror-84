import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="subcommand help")

# init
init = subparsers.add_parser("init")
init.add_argument("--pdf", help="init a beamer presentation")

# run??

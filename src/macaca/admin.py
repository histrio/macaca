"""
File: admin.py
Author: Rinat F Sabitov
Description:
"""
import logging

from database import Base, db


def init_db():
    Base.metadata.create_all(db)


def main(args=None, test=False):
    logging.basicConfig(level=logging.INFO,
        format='%(levelname)-8s %(message)s')

    import argparse
    parser = argparse.ArgumentParser(description='Macaca administration')
    parser.add_argument("command",
        choices=['init_db', ],
        help="administration command")

    args = parser.parse_args()
    if args.command == 'init_db':
        init_db()


if __name__ == "__main__":
    main()

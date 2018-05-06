#!/usr/bin/python

import argparse
import sys
import json
import re
import os
import subprocess

def start():
   print("test") 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='t3client', description='Tic Tac Toe Client')
    subparsers = parser.add_subparsers(help='sub-command help')

    start_parser = subparsers.add_parser('start', help='start help')
    start_parser.set_defaults(func=start)

    args = parser.parse_args()

    args.func()

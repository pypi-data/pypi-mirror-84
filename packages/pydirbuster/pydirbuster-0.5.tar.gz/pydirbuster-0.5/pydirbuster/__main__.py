#!/usr/bin/python3
from pydirbuster.main import Pybuster
import argparse
from pydirbuster import utils

parser = argparse.ArgumentParser(description="Python Web Directory and File Brute Forcer")
parser.add_argument('-u', "--url",required=True, help="The url to start brute foroce from.")
parser.add_argument('-w', "--wordlist", dest="wordfile", required=True, help="The wordlist to use for brute force.")
parser.add_argument('--user', help="HTTP Username")
parser.add_argument('--pass', dest="password", help="HTTP Password")
parser.add_argument('-x', dest="exts", type=utils.lister, default=[''], help="File Extensions - must be commad delimited list")
parser.add_argument('-t', "--threads", type=int, default=15, help="The amount of threads to use.")
parser.add_argument('-o', "--output", dest="logfile", help="File to log results.")
parser.add_argument('-s', dest="codes", type=utils.lister, default=[200,204,301,302,307,401,403],
                    help="HTTP Status Codes to accept in a comma delimited list. Default - 200,204,301,302,307,401,403")
parser.add_argument('-f', dest="force", action="store_true", default=False, help="Force wildcard proccessing.")
agent_help = "Custom or random user agent. -z 'User-agent' for custom. -z for random"
parser.add_argument('-z', "--user-agent", dest="user_agent", default=utils.default_user_agent(), nargs='?',
                    action=utils.UserAgentAction, help=agent_help)

args = parser.parse_args()
scanner = Pybuster(**vars(args))
scanner.Run()

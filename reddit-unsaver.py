import argparse
import os
import time

import praw

def main():
    arg_parser = argparse.ArgumentParser(description="Unsaver for Reddit")
    arg_parser.add_argument("--include", nargs="*", default=[], help="Only unsave from these subreddits")
    arg_parser.add_argument("--exclude", nargs="*", default=[], help="Do not unsave from these subreddits")
    arg_parser.add_argument("--apply", action="store_true", help="Actually unsave (default is dry run)")
    arg_parser.add_argument("delay", type=float, default=0.5, help="Time in seconds between unsaves")
    args = arg_parser.parse_args()

    

import os
import re
import asyncio
import logging
import argparse
# modules
from .classes.Story import Story as lit_story
from .classes.Author import Author as lit_author

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{name}:{filename}] {levelname} - {message}"
    )
)

log = logging.getLogger("literotica_dl")
log.setLevel(logging.INFO)
log.addHandler(handler)

def returnStoryStub(stub):
    # if literotica.com in arg, trim down to the url stub
    if "literotica.com" in stub:
        pattern = "/s/"
        x = stub.find(pattern)
        return stub[x+len(pattern):]
    else:
        return stub

def returnAuthorUID(stub):
    pattern = r'.*uid=(.*)&'
    # if literotica.com in arg, trim down to the url stub
    if "literotica.com/stories/memberpage" in stub:
        match = re.search(pattern, stub)
        return match.group(1)
    else:
        assert str.isdigit(stub)
        return stub

def main():
    # Handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='v0.0.1')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-s', '--story', default=None, help="The story to download. pass in the part after the /s/*")
    parser.add_argument('-a', '--author', default=None, help="The author to mirror.")
    parser.add_argument('-o', '--output', default="output", help="The directory to write files. default: %(default)s")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output)
    except FileExistsError:
        pass

    # argument checking
    if args.author is None and args.story is None:
        msg="One of (-a / -s) flags must be specified"
        log.error(msg)
        raise RuntimeError(msg)

    # Store current directory and return on end
    cwd = os.getcwd()
    # change into output directory
    os.chdir(args.output)

    try:
        if args.story:
            stub = args.story
            stub = returnStoryStub(stub)

            s = lit_story(id=stub)
            s.writeToDisk()

        if args.author:
            stub = args.author
            stub = returnAuthorUID(stub)
            a = lit_author(uid=stub)
            a.download_stories()

    except:
        raise
    finally:
        os.chdir(cwd)
        return

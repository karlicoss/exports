#!/usr/bin/env python3
import json
from subprocess import check_call, check_output
import sys

from feedbin_secrets import email, password

def main():
    # TODO use requests or something
    # right; it's not paginated..
    ress = check_output([
        'http', 
        # https://httpie.org/doc#scripting
        '--check-status', '--ignore-stdin',
        'GET', 'https://api.feedbin.com/v2/subscriptions.json?mode=extended',
        '--auth', email + ':' + password,
    ]).decode('utf8')
    items = json.loads(ress)
    json.dump(items, sys.stdout, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()


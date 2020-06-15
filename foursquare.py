#!/usr/bin/env python3
'''
TODO: use proper data access layer architecture..
'''
import sys
import requests
import json

LIMIT = 250 # according to https://developer.foursquare.com/docs/users/checkins
URL = 'https://api.foursquare.com/v2/users/self/checkins?limit={}&oauth_token={}&v=20161020&offset={}'

def run(limit=LIMIT):
    # Visit https://developer.foursquare.com/docs/explore to generate an OAuth token. Paste that token below.
    from foursquare_secrets import token

    
    offset = 0
    data = []
    while True:
        jj = requests.get(URL.format(limit, token, offset)).json()
        resp = jj['response']
        if 'checkins' not in resp:
            json.dump(jj, sys.stderr, indent=1, ensure_ascii=False)
            sys.exit(1)

        items = len(resp['checkins']['items'])
        if items == 0:
            break
        data.append(jj)
        offset += items

    json.dump(data, sys.stdout, indent=1, ensure_ascii=False, sort_keys=True)


def main():
    run()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
'''
TODO: use proper data access layer architecture..
'''
import json
import sys
import requests


LIMIT = 250 # according to https://developer.foursquare.com/docs/users/checkins
URL = 'https://api.foursquare.com/v2/users/self/checkins?limit={}&oauth_token={}&v=20161020&offset={}'


class RetryMe(Exception):
    pass

# todo make imports defensive?
from tenacity import retry, retry_if_exception_type, wait_exponential

@retry(retry=retry_if_exception_type(RetryMe), wait=wait_exponential())
def get_json(limit=LIMIT):
    # Visit https://developer.foursquare.com/docs/explore to generate an OAuth token
    from foursquare_secrets import token

    offset = 0
    data = []
    while True:
        jj = requests.get(URL.format(limit, token, offset)).json()
        resp = jj['response']
        if 'checkins' not in resp:
            json.dump(jj, sys.stderr, indent=1, ensure_ascii=False)
            if jj.get('meta', {}).get('errorType') == 'server_error':
                # started happening around june 2020 for no reason.. seems transient
                raise RetryMe
            sys.exit(1)

        items = len(resp['checkins']['items'])
        if items == 0:
            break
        data.append(jj)
        offset += items
    return data


def main():
    data = get_json()
    json.dump(data, sys.stdout, indent=1, ensure_ascii=False, sort_keys=True)


if __name__ == '__main__':
    main()

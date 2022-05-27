#!/usr/bin/env python3
from sys import stdout
import requests


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--secrets', required=True, help='secrets file')
    args = p.parse_args()
    from pathlib import Path
    secrets_file = Path(args.secrets)
    obj = {}
    exec(secrets_file.read_text(), {}, obj)
    ical_url = obj['rtm_ical_url'] 
    req = requests.get(ical_url)
    stdout.buffer.write(req.content)


if __name__ == '__main__':
    main()

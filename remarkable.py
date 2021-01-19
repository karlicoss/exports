#!/usr/bin/env python3
'''
Local (SSH) remarkable 2 export

NOTE:
- on Remarkable  : use https://github.com/Evidlo/remarkable_entware to setup rsync, then run: ln -s /opt/bin/rsync /usr/bin/rsync on Remarkable
- on the computer: setup SSH alias and passwordless login as described here (https://remarkablewiki.com/tech/ssh#host_alias_in_sshconfig)
'''

from pathlib import Path
import logging
import subprocess
import sys


def run(*, device: str, to: Path) -> None:
    logger = logging.getLogger()
    cmd = [
        'rsync',
        '--timeout', '5',
        '-av',
        '--delete',
        '--exclude', '.entware', '--delete-excluded',
        '--stats',
        f'{device}:/home/root/',
        str(to),
    ]
    logger.info('Running: %s', cmd)
    res = subprocess.run(cmd, stderr=subprocess.PIPE)
    err = res.stderr.decode('utf8')
    sys.stderr.write(err)
    if 'No route to host' in err:
        # device must be offline, ignore
        return
    res.check_returncode()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    from argparse import ArgumentParser as P
    p = P()
    p.add_argument('--device', type=str, required=True)
    p.add_argument('--to', type=Path, required=True)
    args = p.parse_args()
    run(device=args.device, to=args.to)


if __name__ == '__main__':
    main()

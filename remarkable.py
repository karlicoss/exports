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


def run(*, device: str, to: Path) -> None:
    logger = logging.getLogger()
    cmd = [
        'rsync',
        '-av',
        '--delete',
        '--exclude', '.entware', '--delete-excluded',
        '--stats',
        f'{device}:/home/root/',
        str(to),
    ]
    logger.info('Running: %s', cmd)
    subprocess.run(cmd) # NOTE: deliberately not using check_call, because remarkable might go to sleep while rsync is running?


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

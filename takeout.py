#!/usr/bin/env python3
'''
Uses [[https://rclone.org/drive][rclone]] to mount Google Drive and grab the takeout files.

The most automatic way to set it up I'm aware of is to use [[https://support.google.com/accounts/answer/3024190?hl=en#scheduled-export][scheduled exports]] (one export every two months).
Make sure to use "Add to Drive" as the delivery method!
'''

from contextlib import contextmanager
import logging
from pathlib import Path
from shutil import move
from subprocess import check_call
import sys


def get_logger() -> logging.Logger:
    return logging.getLogger('takeout-grabber')


@contextmanager
def rclone_mount(remote: str):
    logger = get_logger()
    from tempfile import mkdtemp
    from subprocess import Popen, check_call
    import time
    # todo kinda annoying that it creates a dir visible from the outside of the process..
    td = Path(mkdtemp(prefix='takeout_'))
    try:
        cmd = ['rclone', 'mount', '--drive-use-trash=false', f'{remote}:/', str(td)]
        logger.info('%s', cmd)
        with Popen(cmd) as p:
            # need to give it a bit of time to mount
            for _ in range(10):
                time.sleep(0.5)
                if len(list(td.iterdir())) > 0:
                    break
                # rclone shouldn't terminate by that point
                assert p.poll() is None, 'Seems that rclone failed'
                logger.info('waiting for directory to mount...')
            else:
                raise RuntimeError('No files')
            try:
                yield td
            finally:
                check_call(['fusermount', '-u', str(td)])
                while p.poll() is None:
                    p.kill()
                    time.sleep(0.5)
    finally:
        td.rmdir()


def run(*, rclone_remote: str, to: Path) -> None:
    logger = get_logger()
    with rclone_mount(remote=rclone_remote) as mount:
        # sometimes takeout end up in weird paths... e.g.  'Takeout (7971cc47)'
        # in addition, sometimes in google drive it ends up with two Takeout directories (since google drive allows dupe names)
        # but seems like a random one may be mounted since obviously unix wouldn't allow identical names
        # so I guess the idea is at least the script will grab it on the second run or something
        takeout_dirs = list(mount.glob('Takeout*/'))
        for takeout_dir in takeout_dirs:
            logger.info(f'processing {takeout_dir}')
            takeouts = list(takeout_dir.glob('takeout-*.zip'))
            if len(takeouts) == 0:
                logger.info('no new takeouts!')
            for t in takeouts:
                # TODO check for free space?
                logger.info('grabbing %r', t)
                move(t, to / t.name)

            # this should error if the dir isn't empty for some reason
            takeout_dir.rmdir()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
   
    from argparse import ArgumentParser as P
    p = P()
    p.add_argument('--remote', required=True, type=str , help='Rclone remote name (check "rclone listremotes")')
    p.add_argument('--to'    , required=True, type=Path, help='Target directory to move takeout archives to')
    args = p.parse_args()
    run(rclone_remote=args.remote, to=args.to)


if __name__ == '__main__':
    main()

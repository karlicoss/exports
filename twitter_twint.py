#!/usr/bin/env python3
"""
Exports Twitter data using [[https://github.com/twintproject/twint][Twint]]
"""

import twint # type: ignore


# TODO FIXME error handling??
def export_all(*, cfg: twint.Config) -> None:
    # TODO what happens when followers/following change??
    twint.run.Followers(cfg)
    twint.run.Following(cfg)
    twint.run.Favorites(cfg)
    twint.run.Search(cfg)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--username', type=str, required=True)
    p.add_argument('--database', type=str, required=True)
    p.add_argument('--limit', type=int, help='Pass the limit during the subsequent runs of the tool for faster exports')
    # TODO user id?
    args = p.parse_args()


    cfg = twint.Config()
    cfg.Limit = args.limit
    cfg.Username = args.username
    cfg.Database = args.database

    export_all(cfg=cfg)


if __name__ == '__main__':
    main()


# TODO database is locked during the update... not sure if should do atomic writes
# TODO CRITICAL:root:twint.feed:Follow:IndexError ??

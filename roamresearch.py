#!/usr/bin/env python3
'''
Script to 

Usage:

1. Install https://github.com/MatthieuBizien/roam-to-git (pip3 install --user .)
2. Create a wrapper script (e.g. export-roam):

    export ROAMRESEARCH_USER='<username>'
    export ROAMRESEARCH_PASSWORD='<password>'
    ./roamresearch.py

3. Run `export-roam > /path/to/roam/export.json` !

   Note: you might benefit from [arctee](https://github.com/karlicoss/arctee) here.

'''

import asyncio
from pathlib import Path
import sys
import json
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from roam_to_git.scrapping import Config, download_rr_archive, patch_pyppeteer # type: ignore[import]


def main():
    import argparse
    p = argparse.ArgumentParser()
    # todo not sure if need any args??
    args = p.parse_args()

    # TODO remove if it's moved inside download_rr_archive
    patch_pyppeteer()
    with TemporaryDirectory() as td:
        tdir = Path(td)
        atask = download_rr_archive(
            output_type='json',
            output_directory=tdir,
            config=Config(database=None, debug=False),
        )

        # TODO remove this if stderr is used in the library...
        from contextlib import redirect_stdout
        with redirect_stdout(sys.stderr):
            asyncio.get_event_loop().run_until_complete(atask)

        [export_zip] = tdir.glob('*.zip')
        z = ZipFile(export_zip)
        [export_json] = z.namelist()
        json_data = z.read(export_json)

    # sys.stdout.buffer.write(json_data) # this ends up pretty ugly..
    json.dump(json.loads(json_data, encoding='utf8'), sys.stdout, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()

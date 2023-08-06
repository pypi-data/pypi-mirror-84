"""
Copyright (C) 2019-2020 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
from pathlib import Path
import re
import requests
import sys
from urllib.parse import urljoin

from . import fedora, qubes


RE_TORRENT = re.compile(r'<a(.*?)href="(.*?)\.torrent"')
GROUPS = {
    'debian': {
        'index': 'https://cdimage.debian.org/debian-cd/current/amd64/bt-cd/',
    },
    'fedora': {
        'index': 'https://torrents.fedoraproject.org/',
        'filter': fedora.filter_fedora
    },
    'qubes': {
        'index': 'https://ftp.qubes-os.org/iso/',
        'filter': qubes.filter_qubes
    },
    'raspberrypi': {
        'index': 'https://www.raspberrypi.org/downloads/raspberry-pi-os/',
    },
    'slackware': {
        'index': 'http://www.slackware.com/torrents/',
    },
    'tails': {
        'index': 'https://tails.boum.org/torrents/files/'
    },
    'ubuntu': {
        'index': 'https://ubuntu.com/download/alternative-downloads',
    },
}


class FreeTorrents:
    def __init__(self, config: dict, watch: Path):
        self.session = requests.Session()
        self.config = config
        self.watch = watch

    def index_scraper(self, url: str, filter_=None):
        r = self.session.get(url)
        r.raise_for_status()
        matches = set(RE_TORRENT.findall(r.text))
        torrents = set()
        for _,  match in matches:
            torrents.add(urljoin(url, f'{match}.torrent'))

        if filter_:
            torrents = filter_(torrents)

        yield from torrents

    def download(self, url: str):
        if url.endswith('_latest.torrent'):
            req = self.session.head(url)
            req.raise_for_status()
            if req.status_code == 302:
                url = req.headers['location']
        fname = url.rsplit('/')[-1]
        path = self.watch / fname
        if path.is_file():
            print(f'Skipping {fname}...')
            return
        with self.session.get(url, stream=True) as r:
            r.raise_for_status()
            with path.open('wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f'Downloaded {fname}!')

    def run(self, enabled):
        for group, conf in self.config.items():
            if group not in enabled:
                continue
            torrents = self.index_scraper(
                conf['index'], conf.get('filter')
            )
            print(f'-- {group} --')
            for torrent in sorted(torrents):
                # print(torrent)
                self.download(torrent)


def parse_args(groups: list, real_args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('watch', help='Watch folder to download torrents to')
    for group in groups:
        parser.add_argument(f'--no-{group}',
                            help=f'Skip {group} torrents',
                            action='store_true')
    args = parser.parse_args(real_args)
    enabled = []
    for group in groups:
        if not args.__getattribute__(f'no_{group}'):
            enabled.append(group)
    path = Path(args.watch)
    assert path.is_dir()
    return [path, enabled]


def main():
    path, enabled = parse_args(list(GROUPS))
    ft = FreeTorrents(GROUPS, path)
    ft.run(enabled)


if __name__ == '__main__':
    main()

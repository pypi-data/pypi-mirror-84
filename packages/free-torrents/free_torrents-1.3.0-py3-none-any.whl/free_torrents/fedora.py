"""
Copyright (C) 2020 Kunal Mehta <legoktm@member.fsf.org>

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
import re
import requests


def filter_fedora(torrents):
    latest = latest_fedora()
    for torrent in torrents:
        if torrent.endswith(f'-{latest}.torrent'):
            yield torrent


def latest_fedora() -> str:
    r = requests.get(
        'https://bodhi.fedoraproject.org/releases/?rows_per_page=50',
        headers={
            'Accept': 'application/json'
        }
    )
    r.raise_for_status()
    data = r.json()
    versions = set()
    for release in data['releases']:
        # e.g. F30
        if release['state'] == 'current' \
                and re.match(r'^F(\d*?)$', release['name']):
            # Strip F prefix
            versions.add(release['name'][1:])
    if not versions:
        raise RuntimeError('Unable to determine latest Fedora release')

    return max(versions)

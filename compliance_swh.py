#!/usr/bin/env python3
# osscompliance
# Copyright (C) 2020 Sebastien Campion
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import json
import urllib.request
from hashlib import sha1
from functools import lru_cache
from pathlib import Path

def get(r):
    return json.loads(urllib.request.urlopen(r).read())


def swhids():
    for root, dirs, files in os.walk(".", topdown=False):
        if not root.startswith("./."):  # Ignore .dirs and .files
            for name in files:
                filepath = os.path.join(root, name)
                with open(filepath, 'rb') as f:
                    s = sha1()
                    s.update(("blob %u\0" % os.stat(filepath).st_size).encode('utf-8'))
                    s.update(f.read())
                    yield "swh:1:cnt:" + s.hexdigest(), filepath


@lru_cache(maxsize=128)
def license(url):
    for facts in get(url)['facts']:
        yield facts["license"]


def get_license(swhid):
    try:
        url = "https://archive.softwareheritage.org/api/1/content/" + swhid.replace("swh:1:cnt", "sha1_git")
        return list(license(get(url)['license_url']))
    except:
        return


def post_swh():
    ids = {swhid: fp for swhid, fp in swhids()}
    url = 'https://archive.softwareheritage.org/api/1/known/'
    params = json.dumps(list(ids.keys())).encode("utf-8")
    req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})
    for swhid, v in get(req).items():
        if v['known']:
            yield ids[swhid], get_license(swhid)

def md_report():
    if os.environ.get("OSSCOMPLIANCE_NO_MDREPORT"):
        return
    with open("OSS_compliance_report.md", "w") as f:
        for report in os.listdir(".osscompliance"):
            with open(os.path.join(".osscompliance", report), 'r') as fr:
                    f.writelines("# %s report\n" % report.replace(".json", "").capitalize())
                    f.writelines("| Artefact   | License(s)     |\n")
                    f.writelines("| ---------- | -------------- |\n")
                    for k, v in json.load(fr).items():
                        v = str(v)
                        f.writelines(f"| {k: <{40}} | {v: <{40}} |\n")


if __name__ == '__main__':
    Path(".osscompliance").mkdir(exist_ok=True)
    with open(os.path.join(".osscompliance", "Software Heritage.json"), "w") as f:
        results = {pkg: str(lic) for pkg, lic in post_swh()}
        json.dump(results, f, indent=2, sort_keys=True)
    md_report()

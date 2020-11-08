#!/usr/bin/env python3
import os
import json
import urllib.request
from hashlib import sha1
from functools import lru_cache


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


if __name__ == '__main__':
    with open("Software_Heritage_Compliance_Report.md", "w") as f:
        f.writelines("# Software Heritage Compliance Report\n")
        f.writelines("## Files already indexed :\n")
        no_results = True
        for fp, lic in post_swh():
            if no_results:
                f.writelines("| File       | License(s)     |\n")
                f.writelines("| ---------- | -------------- |\n")
            lic = str(lic)
            f.writelines(f"| {fp: <{40}} | {lic: <{40}} |\n")
            no_results = False
        if no_results:
            f.writelines("No files identified\n")

#!/usr/bin/env python3
import os
import json
import urllib.request


def requirements_licenses_inventory():
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r') as f:
            for line in f:
                pkg = line.rstrip().replace('==', '/')
                url = f"https://pypi.org/pypi/{pkg}/json"
                try:
                    metadata = json.loads(urllib.request.urlopen(url).read())
                    yield pkg, metadata['info']['license'].lower()
                except Exception as e:
                    print(str(e))

if __name__ == '__main__':
    print(set([l for _, l  in requirements_licenses_inventory()]))
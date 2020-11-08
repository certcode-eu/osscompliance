#!/usr/bin/env python3
import os
import json
import urllib.request
from pathlib import Path

def requirements_licenses_inventory():
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r') as f:
            for line in f:
                pkg = line.rstrip().replace('==', '/')
                if pkg.startswith("git+https"):
                    yield pkg, "???"
                    continue
                url = f"https://pypi.org/pypi/{pkg}/json"
                try:
                    metadata = json.loads(urllib.request.urlopen(url).read())
                    yield pkg, metadata['info']['license'].lower()
                except Exception as e:
                    print(f"{pkg} pypi metadata extration failed : "+ str(e))


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
    with open(os.path.join(".osscompliance", "python.json"), "w") as f:
        results = {pkg: lic  for pkg, lic in requirements_licenses_inventory()}
        json.dump(results, f, indent=2, sort_keys=True)
    md_report()

    # with open("Python_Compliance_Report.md", "w") as f:
    #     f.writelines("# Python Packages Compliance Report\n")
    #     f.writelines("| Packages   | License(s)     |\n")
    #     f.writelines("| ---------- | -------------- |\n")
    #     for pkg, lic  in requirements_licenses_inventory():
    #         lic = str(lic)
    #         f.writelines(f"| {pkg: <{40}} | {lic: <{40}} |\n")
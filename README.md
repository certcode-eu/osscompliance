# Open Source Sofware Compliance Hooks

## Goal
As OSS components are used more and more in our development, it is important to
monitor the compliance of their licenses to avoid errors by mixing incompatible 
pieces of code as defined by their licenses

Obiously, it's important to discover that issue earlier
in the developpement process, in others well knowned terms ...
[Fail Fast](https://www.martinfowler.com/ieeeSoftware/failFast.pdf)


## Approach
The first approach is to build a single and simple compliance report. 
These hooks will build it. It will list licenses and/or open sources files used in and by your code repository.

When `python` and `Software Heritage` hooks are combined, you will discover an new markdown file `OSS_compliance_report.md`

```
# Software heritage report
| Artefact                                 | License(s)                               |
| ---------------------------------------- | ---------------------------------------- |
| ./.gitignore                             | ['No_license_found']                     |
| ./agpl-3.0.txt                           | ['AGPL-3.0']                             |

# Python report
| Artefact                                 | License(s)                               |
| ---------------------------------------- | ---------------------------------------- |
| Flask/1.1.1                              | bsd-3-clause                             |
| aiohttp-jinja2                           | apache 2                                 |
| docker                                   | apache license 2.0                       |
| flask-ldap3-login                        |                                          |
| flask-simpleldap                         | mit                                      |
| git+https://github.com/dataiku/dataiku-api-client-python#egg=dataiku-api-client | ???                                      |
| gunicorn                                 | mit                                      |
| kafka-python                             | apache license 2.0                       |
| psycopg2-binary                          | lgpl with exceptions                     |
| pymongo/3.10.1                           | apache license, version 2.0              |
| python-ldap                              | python style                             |
| requests/2.21                            | apache 2.0                               |
| websockets                               | bsd                                      |

```


## How to
This repo contains several git hooks, move one them into your git project`.git/hooks/pre-commit` to use it
If you plan to use severals hooks, take a look at the [`pre-commit` project](https://github.com/pre-commit/pre-commit) 

You only need a python3 interpreter.


### Modules

#### Software Heritage
This module will scan your repository files to find out if any of them was already indexed 
by [Software Heritage](https://www.softwareheritage.org/)

In our example, two files was already known : 

    | ./.gitignore                             | ['No_license_found']                     |
    | ./agpl-3.0.txt                           | ['AGPL-3.0']                             |


#### Python
This module will scan the pipy cheese shop based on the `requirements.txt` file and display licenses associated.


## TODO
- Notification when report diff detected
- Use previous results as cache
- Create other language modules

## License 
AGPL 

## Author(s)
- Sebastien Campion 




# ec2-compare
[![PyPI - ec2-compare](https://img.shields.io/pypi/v/ec2-compare.svg?color=blue&label=ec2-compare)](https://pypi.org/project/ec2-compare)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ec2-compare.svg?color=blue)](https://pypi.org/project/ec2-compare)
[![Coverage](https://img.shields.io/codecov/c/github/weldpua2008/ec2-compare)](https://codecov.io/gh/weldpua2008/ec2-compare)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/ec2-compare?color=blue)](https://pypistats.org/packages/ec2-compare)

Compare EC2 instances families without querying AWS API

## Versioning

`ec2_compare` follows
[PEP 440](https://www.python.org/dev/peps/pep-0440/).


## How to build

```bash
python -m pip install -e ./[devel]
# or pip install -e ./[devel]

# Running tests
scripts/tests.sh
```

## Update data Locally
1. Downland the latest info
````bash
aws ec2 describe-instance-types | jq '.InstanceTypes' > aws_ec2.json
````
2. repack
```bash
python3 repack.py
```

## Thank you
- https://github.com/actions/ for an awesome github actions
- [mypy](https://github.com/python/mypy) for doing all dirty work for us

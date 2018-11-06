#!/usr/bin/env bash

set -eo pipefail

virtualenv venv
source ./venv/bin/activate

pip install --editable .

mergeyaml --input ./test.yaml --set web.image.tag=1.0.4

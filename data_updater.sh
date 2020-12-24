#!/bin/bash
# see: https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

SCRIPT_DIR=`dirname $0`
DATA_DIR=$SCRIPT_DIR/app/data

cd $SCRIPT_DIR

# activate virtual environment
source .venv/bin/activate

# download sources, backup current data and update processed CSVs
python refreshdata.py

# pull in case there were commits
git pull

# add updated files to index
TODAY=`date +%Y.%m.%d`
YESTERDAY=`date +%Y-%m-%d -d "1 day ago"`

git add $DATA_DIR/processed/*.csv
git add $DATA_DIR/processed_backups/*.csv
git add $DATA_DIR/sources/$YESTERDAY*

# commit, tag and push
git commit -m "Automatic update: Data update for $YESTERDAY"
git push

git tag v$TODAY.0
git push --tags

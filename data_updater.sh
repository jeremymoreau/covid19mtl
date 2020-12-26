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

# create version tag, increment if it already exists
TODAY=`date +%Y.%m.%d`
YESTERDAY=`date -v-1d +"%Y-%m-%d"`
VERSION_TAG="v$TODAY.0"
REMOTE_TAGS=`git ls-remote --tags origin`

while [[ $REMOTE_TAGS == *$VERSION_TAG* ]]; do
  i="$((${VERSION_TAG: -1}+1))"
  VERSION_TAG="v$TODAY.$i"
done

# add updated files to index
git add $DATA_DIR/processed/*.csv
git add $DATA_DIR/processed_backups/*.csv
git add $DATA_DIR/sources/$YESTERDAY*

# commit, tag and push
git commit -m "Automatic update: Data update for $YESTERDAY"
git push

git tag $VERSION_TAG
git push --tags

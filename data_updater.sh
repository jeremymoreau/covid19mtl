#!/bin/bash
# see: https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

SCRIPT_DIR=$(dirname $0)
DATA_DIR=$SCRIPT_DIR/app/data

cd $SCRIPT_DIR

# activate virtual environment
source .venv/bin/activate

# pull in case there were commits
echo "pulling latest state of repo..."
git pull

# download sources, backup current data and update processed CSVs
echo "downloading data, processing files..."
python refreshdata.py

# create version tag, increment if it already exists
echo "determining version tag..."
TODAY=$(date +%Y.%m.%d)
VERSION_TAG="v$TODAY.0"
REMOTE_TAGS=$(git ls-remote --tags origin)

while [[ $REMOTE_TAGS == *$VERSION_TAG* ]]; do
  i="$((${VERSION_TAG: -1}+1))"
  VERSION_TAG="v$TODAY.$i"
done

echo "committing and pushing changes..."

# support Mac/BSD date and Linux/GNU date
if [ "$(uname)" == "Darwin" ]; then
    YESTERDAY=$(date -v-1d +"%Y-%m-%d")
else
    YESTERDAY=$(date +%Y-%m-%d -d "1 day ago")
fi

# add updated files to index
git add $DATA_DIR/processed/*.csv
git add $DATA_DIR/processed_backups/*.csv
git add $DATA_DIR/sources/$YESTERDAY*

# commit, tag and push
git commit -m "Automatic update: Data update for $YESTERDAY"
git push

git tag $VERSION_TAG
git push --tags

#!/bin/bash
# see: https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

SCRIPT_DIR=$(dirname $0)
DATA_DIR=$SCRIPT_DIR/app/data

cd $SCRIPT_DIR

# activate virtual environment
source .venv/bin/activate

# pull in case there were commits
# echo "pulling latest state of repo..."
git pull > /dev/null

# download sources, backup current data and update processed CSVs
# echo "downloading data, processing files..."
OUTPUT=$(python refreshdata.py)

# check if there are local changes to the processed files
# see: https://stackoverflow.com/q/5143795
# since untracked files are not reported, this will prevent only the backup to be committed
if ! git diff-index --quiet HEAD -- $DATA_DIR/processed/; then
  echo "detected local changes:"
  echo "$OUTPUT"

  # create version tag, increment if it already exists
  echo "determining version tag..."
  TODAY=$(date +%Y.%m.%d)
  VERSION_TAG="v$TODAY.0"
  REMOTE_TAGS=$(git ls-remote --tags origin)

  while [[ $REMOTE_TAGS == *$VERSION_TAG* ]]; do
    i="$((${VERSION_TAG: -1}+1))"
    VERSION_TAG="v$TODAY.$i"
  done

  echo "version tag: $VERSION_TAG"

  echo "committing and pushing changes..."

  # support Mac/BSD date and Linux/GNU date
  if [ "$(uname)" == "Darwin" ]; then
      YESTERDAY=$(date -v-1d +"%Y-%m-%d")
  else
      YESTERDAY=$(date +%Y-%m-%d -d "1 day ago")
  fi

  # add updated files to index
  git add $DATA_DIR/processed/*.csv > /dev/null
  git add $DATA_DIR/processed_backups/$(date +%Y-%m-%d)/*.csv > /dev/null
  git add $DATA_DIR/sources/$YESTERDAY/* > /dev/null

  # check if there are now changes on the index (staged for commit)
  if ! git diff-index --cached --quiet HEAD --; then
    # commit, tag and push
    git commit -m "Automatic update: Data update for $YESTERDAY" -m "$OUTPUT"
    git push

    git tag $VERSION_TAG
    git push --tags
  fi
fi

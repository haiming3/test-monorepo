#!/bin/bash
#
# This script automates the creation and updating of a subtree split
# in a second repository.asdasd
#
set -eu
#IFS=$'\n\t'

command -v splitsh-lite >/dev/null 2>&1 || { echo "$0 requires splitsh-lite but it's not installed.  Aborting." >&2; exit 1; }

source_list_file=$1

# Adjust for your repositories.
source_repository=https://github.com/haiming3/test-monorepo.git
source_branch=main


cat $source_list_file | while read line
do
    echo ""
    source_dir=${line%:*}
    branch_name=${line#*:}
    echo "***** source_dir:${source_dir} -> ${branch_name} branch *****"
    destination_branch=${branch_name}

    # The rest shouldn't need changing.
    temp_repo=$(mktemp -d)
    temp_branch=$RANDOM

    # Checkout the old repository, make it safe and checkout a temp branch
    git clone ${source_repository} ${temp_repo}
    cd ${temp_repo}
    git checkout ${source_branch}
    git remote remove origin
    git checkout -b ${temp_branch}

    # Create the split, check it out and then push the temp branch up
    sha1=$(splitsh-lite --prefix=${source_dir} --quiet)
    git reset --hard ${sha1}
    git remote add remote ${source_repository}

    echo "***** push new code to ${destination_branch} branch *****"
    # To repair split, 'push -f' is required for the first time
    # After the service branch is forced to update, it will cancel '-f'
    git push -u remote ${temp_branch}:${destination_branch}

    # Cleanup
    #rm -rf ${temp_repo}
done


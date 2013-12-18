#!/bin/bash
# compass/install.sh - install Compass under the "./Gem" directory

if ! which gem >/dev/null ;then
    echo 'Error: no "gem" command available!'
    echo 'Please install Ruby!'
    exit 1
fi

BASE=$(dirname $(readlink -f $(which "$0")))
cd $BASE  # the directory where this script lives

gem install -i Gem compass
gem install -i Gem compass-susy-plugin
gem install -i Gem zen-grids
gem install -i Gem sassy-buttons
#!/bin/bash
# compass/compass.sh - properly invoke the "Compass" program
# # Provided by http://rhodesmill.org/brandon/2011/adding-compass/ to help set up compass

BASE=$(dirname $(readlink -f $(which "$0")))
export GEM_HOME=$BASE/Gem
export RUBYLIB=$BASE/Gem/lib
$BASE/Gem/bin/compass "$@"

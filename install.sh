#!/usr/bin/env bash

if [ ! -d venv ]; then
  echo "Creating venv"
  python3.10 -m venv venv
fi

source venv/bin/activate

if [[ ! $PYTHONPATH =~ $PWD ]]; then
  echo "Exporting PYTHONPATH"
  export PYTHONPATH=$PWD:$PWD/src:$PYTHONPATH
fi

pip install --upgrade pip
pip install -r requirements.txt

#extra packages to install
pip install -r requirements-local.txt
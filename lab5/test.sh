#!/bin/bash
TEST='examples/example1.m'

if [[ -d ".venv" ]]
then
	rm -rf .venv
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py --filename ${TEST} --disable_ast
deactivate
rm -rf .venv # cleanup

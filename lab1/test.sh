TEST='example.txt'

if [[ -d ".venv" ]]
then
	rm -rf .venv
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py ${TEST}
deactivate
rm -rf .venv # cleanup

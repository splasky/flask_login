export FLASK_APP=src/app.py

install_requirements:
	pip install -r requirements.txt
init:
	flask initdb
run:
	flask run

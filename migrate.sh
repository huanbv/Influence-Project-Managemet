# step 1: drop all tables in the db -- using sqlite studio
# step 2: remove the migrations folder
# step 3: re-run the following scripts
# sh ./migrate.sh


export FLASK_APP=main.py

flask db init
flask db migrate -m "create tables"
flask db upgrade

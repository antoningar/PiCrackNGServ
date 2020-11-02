export FLASK_APP=/home/pi/dev/api/__init__.py

rm -f ./output/*
python -m flask run --host=192.168.43.177

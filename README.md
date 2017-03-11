# facebook_update
Use for testing facebook app 
create a virtaul Environment:-
virtualenv env

activate virtual environment:-
source env/bin/activate

install dependencies:-
pip install -r requirement.txt

run django migrations
python manage.py makemigrations
python manage.py migrate

do collectstatic
python manage.py collectstatic

run server
python manage.py runserver 80

use following link(since this is registered in my facebook app)
http://localhost:8000

Project reqiures such variables in files .env: 
FLASK_DEBUG
DATABASE_URL
SQL_HOST
SQL_PORT
DATABASE
DEVELOPER_KEY for YouTube 
API_TOKEN for Lichess

Variables for .env.prod.db:
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

To make a container use this comands
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

This program gives the timestamps of the all lost games during the stream.
To do this you need to write username of streamer on lichess in the first field. Then you have to write youtube video id. For desktop version the id is after "=". As for mobile version id is after the last "\"
Example:
user = Zhigalko_Sergei

id = dec17AekrSs

     (xG2YjKtLGWA)

or

user = nemtsevguru

id = clhANCZvtig

Then copy and paste result  in youtube video's comments. Enjoy highlited momments. 

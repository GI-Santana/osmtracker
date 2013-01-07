#OSMTracker

##Overview

OSM Tracker is an django based web-application for tracking the activities
of OpenStreetMap mappers.  You add a list of mappers to OSM Tracker and
it will monitor their activities (by querying the HTTP interface on
OpenStreetMap) so you can track there activities.

You can also use OSM Tracker to send mappers messages through the OSM
messaging system.  OSM Tracker will keep track of which mappers you have
contacted with each email template.

## Requirments

* python 2.6 (should work with 2.7 as well)
* django 1.4 (tested with 1.4.2)
* distribute (tested with 0.6.24)
* dj-database-url (tested with 0.2.1)
* psycopg2 (tested with 2.4.5)
* feedparser (tested with 5.1.2
* pytz (tested with 2012h)
* wsgiref (tested iwth 0.1.2)

## Installation via Heroku

* Create a heroku application  (ie heroku apps:create myappname)
* Push the repository to heroku (git push heroku) 
* create the database (heroku run python manage.py syncdb)

## Local installation

* Setup a Postgresql database (ie osmtracker)
* edit DATABASE_URL to point at your database.  ie (export DATABASE_URL=postgres://mydbuser@localhost:5432/osmtracker)
* python manage.py syncdb
* python manage.py runserver



## License 

OSM tracker is licensed under the BSD license. See COPYING

## Contact

Steve Singer
steve@ssinger.info
http://scanningpages.wordpress.com



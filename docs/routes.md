# Routes

## General Routes

* `/`: `GET` that does a API and database check, returns database status
* `/login`: `POST` to login into the system, returns the access token
* `/sitemap`: `GET` that prints out all routes available, returns list of routes
* `/refresh`: `GET` that refreshes access token from refresh token, returns new
access token
* `/adduser`: Adding new user to user DB, 

## Individual Runs

Please note: All of these can be accessed under `/run` and `/runs`. 

* `/run/insert`: Not implemented. Add a new run doc

* Using the run number as an integer:
    * `/run/runnumber/<int:run_number>/`:
        * `GET`: Returns the whole run document
        * `DELETE`: 
    * `/run/number/<int:run_number>/`: Same as 
    `/run/runnumber/<int:run_number>/`
    * `/run/runnumber/<int:run_number>/gains/`:
        * `GET`: Retrieve the gains for given run
        * `PUT`: Add/update the gains for given run
    * `/run/number/<int:run_number>/gains`: Same as 
    `/run/number/<int:run_number>/gains`
    * `/run/number/<int:run_number>/data/`:
        * `GET`: Retrieve the `data` field for given run
        * `POST`: Add to the `data` list for given run
        * `DELETE`: Delete the entry in the `data` list for a given run
    * `/run/number/<int:run_number>/data/<string:data_type>/`: Limits `GET` 
    from `/run/number/<int:run_number>/data/` to a selected data type

    * `/run/runnumber/<int:run_number>/filter/<string:top_level>/<string:second_level>/<string:third_level>`: `GET` returns the partial run document that can be filtered up to three levels deep
    * `/run/number/<int:run_number>/filter/<string:top_level>/<string:second_level>/<string:third_level>`: Same as `/run/runnumber/<int:run_number>/filter/<string:top_level>/<string:second_level>/<string:third_level>`

* Using the run name (YYMMDD_HHMM format):
    * `/run/timestamp/<string:timestamp>/`: `GET` return the whole document 
    * `/run/name/<string:timestamp>/`: Same as 
    `/run/timestamp/<string:timestamp>/`
    * `/run/timestamp/<string:timestamp>/gains/`:
        * `GET`: Retrieve the gains for given run
        * `PUT`: Add/update the gains for given run
    * `/run/timestamp/<string:timestamp>/data/`:
        * `GET`: Retrieve the `data` field for given run
        * `POST`: Add/update the `data` list for given run
        * `DELETE`: Delete the entry in the `data` list for a given run
    * `/run/timestamp/<string:timestamp>/data/<string:data_type>/`: Limits `GET`
     from `/run/timestamp/<string:timestamp>/data/` to a selected data type
    * `/run/timestamp/<string:timestamp>/filter/<string:top_level>/<string:second_level>/<string:third_level>`: `GET` returns the partial run document that can be filtered up to three levels deep
    * `/run/name/<string:timestamp>/filter/<string:top_level>/<string:second_level>/<string:third_level>`: Same as `/run/timestamp/<string:timestamp>/filter/<string:top_level>/<string:second_level>/<string:third_level>`

* Using the object ID (MongoDB specific) in UUID format. 
    * `/run/objectid/<ObjectId:object_id>/`: `GET` return the whole document
    * `/run/objectid/<ObjectId:object_id>/gains/`:
        * `GET`: Retrieve the gains for given run
        * `PUT`: Add/update the gains for given run
    * `/run/objectid/<ObjectId:object_id>/data/`:
        * `GET`: Retrieve the `data` field for given run
        * `POST`: Add/update the `data` list for given run
        * `DELETE`: Delete the entry in the `data` list for a given run
    * `/run/objectid/<ObjectId:object_id>/data/<string:data_type>/`: Limits `GET`
     from `/run/objectid/<ObjectId:object_id>/data/` to a selected data type
    * `/run/objectid/<ObjectId:object_id>/filter/<string:top_level>/<string:second_level>/<string:third_level>`: `GET` returns the partial run document that can be filtered up to three levels deep


## Sets of Runs

Note these will by default return a list of run identifiers

* `/runs/`: `GET` of all runs
* `/runs/<string:data_field>`: `GET` of all runs with an additional top-level 
field

* `/runs/status/<string:status>`: `GET` all runs with certain pseudo status
* `/runs/status/<string:status>/<string:data_field>`: `GET` all runs with 
certain pseudo status with an additional top-level field

* `/runs/location/<string:location>`: `GET` all runs at a certain RSE
* `/runs/location/<string:location>/<string:data_field>`: `GET` all runs at a 
certain RSE with an additional top-level field

* `/runs/detector/<string:detector>/`: `GET` all runs for a certain detector 
type
* `/runs/detector/<string:detector>/<string:data_field>`: all runs for a 
certain detector type with an additional top-level field

* `/runs/source/<string:source>/`: `GET` all runs with a certain source. There 
is a special source called "calibration", which is all runs that are not 
background
* `/runs/source/<string:source>/<string:data_field>/`: `GET` all runs with a 
certain source with an additional top-level field. There is a special source 
called "calibration", which is all runs that are not background.

* `/runs/tag/<string:tag>/`: `GET` all runs with a certain tag.
* `/runs/tag/<string:tag>//<string:data_field>"`: `GET` all runs with a certain 
tag with an additional top-level field.

## None functioning

* `/runs/query`: `GET` open-ended query.


# XENON runsDB REST API

The XENON runsDB REST API is the new interface for users to interact with the 
runsDB without the shortcomings of interacting with the DB through CAX or 
through MongoDB bindings for the respective language. Moving to a REST
interface was necessary because we needed a language agnostic (at least
Python2 vs. 3 agnostic) way to access the DB and to allow a more flexible
interaction with the runsDB for the production services and general
user. The MongoDB developers also recommend using a REST interface
rather than the language-specific bindings directly

## Overview

The main objective of this REST API is support the data processing and 
management for the XENONnT experiment. Both of these tasks need to access the 
so-called `runsDB`. The `runsDB` stores tbe relevant information about a given
detector run. This includes the status of a run, the data location, detector 
configuration, DAQ settings, etc.. The data processing and management software
will have to retrieve, update, and add information to the database. 

The choice to create a REST API for the `runsDB` was made because:

* Language-agnostic and user-friendly interface
* Industry-standard form of access to DBs and services over the WAN
* No more direct DB calls
* IP whitelist no longer necessary
* Readily scalable
* Easy caching of data through HTTP proxy

### Data Management

The main tasks in data management is to initiate and monitor file transfers 
between storage locations across USA, EU, and Israel. The detailed steps 
that the data management system are as follows:

1. Check runsDB for runs that have been recently completed and have not had 
data added to the rucio catalog
2. Add data to rucio catalog and create dataset
3. Add rules for dataset transfers to destinations
4. Check rucio catalog for changes and update runsDB accordingly

To be able to facilitate this workflow the REST API will have to be able to:

1. Access the status of the run
2. Update the location of data in the runsDB
3. Add information about new data types, etc. to runsDB

### Data Processing

The main tasks in data processing is to perform first level of data reduction 
and produce higher-level quantities require for physics analysis. As part of 
this, the data processing follows these steps:

1. Check `runsDB` for runs that have transferred and not yet processed
2. If new data is present, submit jobs to calculate the PMT gains
3. Once PMT gains have been put into the runsDB, create a DAGMan job that will 
process the data one file per job.
4. Once data is processed, add per-run output file to rucio catalog
5. Add information about processed data to the runsDB

To facilitate the data processing the REST API will need to:

1. Check runsDB for runs that have been recently transferred and have not been 
processed
2. Submit jobs to calculate PMT gains
3. Create jobs for processing data - One file per job
4. Adding per-run output file to rucio catalog
5. Add rules to transfers for processed data to destination
6. Update runsDB with information on processed data, e.g. location

## Implementation

The implementation primarily focuses on the `runsDB` interface for the 
production data management and processing services. In this case we have 
made following choices:

* Make frequently used queries directly accessible, e.g. entire 
document for a given run, all runs with a certain tag, runs with a certain 
source, query individual run documents up to three-levels deep, etc.
* "Pseudo" status - MongoDB queries of "data" field have been translated into a 
status for the run
* Additions/updates only for necessary fields, e.g. gains
* Read-only queries return list of run identifiers
* Updates and additions can only access a single run document at a time. NOTE:
This may change

### Frequent Queries

There are certain quantities and documents that users want to access frequently. 
The main information that users want to be accessed are the complete database 
document for an individual run or a sub-section of said document and list
the runs associated with a certain set of criteria, e.g. sources, tags, location
detector type, etc.

#### Single Runs

The API provides several ways to access the run documents. The documents can be 
accessed either through their `name` (timestamp of run start), `number` 
(number of the run), and the MongoDB `objectid`. The routes are

* `name`:
  * `/runs/name/<run name>`
  * `/run/name/<run name>`
  * `/runs/timestamp/<run name>`
  * `/run/timestamp/<run name>`
* `number`
  * `/runs/runnumber/<run number>`
  * `/run/runnumber/<run number>`
  * `/runs/number/<run number>`
  * `/run/number/<run number>`
* `objectid`
  * `/runs/objectid/<object id>`
  * `/run/objectid/<object id>`

One can also access the only the sub-sections of a single document through their
keys. For example, to access the `data` document of a given run one simply has 
to add `data` to the URL: `/runs/number/<run number>/data`. One can access 
up to three levels deep, e.g. 
`/runs/number/<run number>/filter/<top level>/<second level>/<third level>`

There are two special fields: `data`, and `gains` (`processor.DEFAULT.gains`). 
These can be accessed directly without `filter` in the route. This is to 
accommodate the fact that these have `PUT`/`POST`as well as `GET` methods.

#### Set of Runs

Listing a set of runs can currently be done through the following criteria:

* Detector: Detector type of the run
* Location: All runs at a certain RSE
* Source: Calibration source being used for this run, background runs don't 
have a source
* Status: "Pseudo" status of run, see below
* Tags: All runs with a certain tag

The API returns a list of `JSON` objects that contain the run identifiers. The
entire run document for each run will not be returned. This was necessary to 
reduce the query execution time and keep the amount of data returned reasonable.
One can add specific top level data fields to the returned object, by adding
the name of the top level field to the query, e.g. `/runs/source/none/data`

### "Pseudo" Status

The status of run is not defined as singular field in the runsDB. 
It is rather defined as linear combination of status of the data type, e.g. 
"raw" data is in the "transferred" state or "processed" data does not exist yet
means that the data is ready for processing. To allow for an easier access to 
the various states, the REST API support creates "pseudo" states for the runs. 
At the moment, the pseudo states are:

* `not_processed`: Raw data has been transferred and not yet processed
* `transferring`: Data is being transferred and not yet processed
* `processing`: Data is processing
* `processed`: Data has completed processing
* `new_run`: Data taking is complete and run hasn't been added to rucio catalog

### Adding/Updating Fields

At the moment, there are only two top level fields that can be updated: `data`
and `gains`. These two fields are altered during processing. Mainly by adding
PMT gains and then by adding the location of the processed data to the runsDB. 

These changes can only be done on a per-run basis rather than as a batch update. 
The instances in which a batch update of the database are needed are fairly
uncommon. Similarly, in day-to-day operation only single or a handful of runs
is handled at any given time. 

The updates are handled through a `JSON` document that has to be attached to 
`PUT`/`POST` request. The document is then minimally sanitized and vetted. The
`data` field allows for following keys in the `JSON` document:

* `checksum`: String that contains the checksum of the files. Required
* `creation_time`: Datetime in iso string format that indicates when the data 
was created. Require
* `creation_place`: String where data was created. Required
* `host`: String on what host the data is stored. Required
* `location`: String where the data is stored on the `host`. Required
* `type`: String what type of data (raw, processed, etc.). Required
* `rse`: List of strings that indicate the RSE where the data is stored
* `rule_info`: List of strings that show the status of the rucio rules
* `strax_hash`: String used by strax to define it's version
* `pax_version`: String that indicates which pax version has been used for 
processing

The `gains` field only allows:

* `gains`: List of floats that are greater than or equal to 0.

These fields can only be updated on a per-run basis. This is a safety 
mechanism, an outgrow of how systems and people interact with the system, and 
a choice to simplify the codebase. The safety mechanism is that large changes to 
the database require thought and some effort. Instead of simply pushing a 
`JSON`, one has to loop through the individual runs. This can tedious but 
allows for better error checking.

The data management and processing scheme operates mostly on individual runs. 
There are a few instances where multiple runs are being processed, e.g. 
re-processing campaign, or moved by the data management system. These instances 
only happen O(1) per year versus the dealing with individual runs happens on a 
hourly basis.

The per-run change simplifies the codebase mostly from the aspect of sanitizing 
the inputs to change the database. Sanitizing a list or dictionary of changes
is significantly harder than santizing individual runs. 

## Authorization and Authentication

The authorization and authentication is done through the flask-praetorian 
flask extension. It provides a fairly simply way to implement authentication 
and authorization.

In this case we will have four users:

* `admin`: User for administration
* `xenon-admin`: XENON member with administration rights
* `xenon-production`: XENON member with production rights
* `xenon-user`: XENON user with user rights

The authorization levels are:

* Administration: Can add/remove users, has access to all routes, incl. 
`PUT`/`POST`
* Production: Has access to all routes, incl. `PUT`/`POST/DELETE`
* User: Has access to all `GET` routes
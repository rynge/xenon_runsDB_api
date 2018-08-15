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

### Data Processing

The main tasks in data processing is to perform first level of analysis and 
produce higher-level quantities require for physics analysis. As part of this,
the data processing follows these steps:

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
primary user, which is the production data management and processing services. 
In this case we have made following choices:

* Focus on frequently used queries are directly accessible, e.g. entire 
document for a given run, all runs with a certain tag, runs with a certain 
source, query individual run documents up to three-levels deep, etc.
* "Pseudo" status - MongoDB queries to get status of a run through "data" 
field have been translated into a status for the run
* Additions/updates only for necessary fields, e.g. gains
* Read-only queries return anywhere one to many run documents
* Updates and additions can only access a single run document at a time. NOTE:
This may change

### Frequent Queries

There are certain quantities and documents that users want to access frequently. 
The main information that users want to be accessed are the complete database 
document for an individual run or a sub-section of said document. To access the
the documents, the API provides several ways to access the run documents. The
documents can be accessed either through their `name` (timestamp of run start), 
`number` (number of the run), and the MongoDB `objectid`. These are accessed 
through

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
`/runs/number/<run number>/<top level>/<second level>/<third level>`

To list 



### "Pseudo" Status

The status of run is not defined as singular field in the runsDB. 
It is rather defined as status of the data type, e.g. "raw" data is in the
"transferring" state or "processed" data is in the "processing" state. To allow
for an easier access to the various states, the REST API support creates 
"pseudo" states for the runs. At the moment, the pseudo states are:

* `not_processed`: Data has been transferred and  not yet processed
* `transferring`: Data is being transferred and not yet processed
* `processing`: Data is processing
* `processed`: Data has completed processing
* `new_run`: Data taking is complete and run hasn't been added to rucio catalog

Once a request is made against the API for a certain status, the API will 
return a `JSON`-object. This will typically be a list of documents.

## Current Status




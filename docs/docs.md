# XENON runsDB REST API

The XENON runsDB REST API is the new interface for users to interact with the 
runsDB without the shortcomings of interacting with the DB through CAX or 
through MongoDB bindings for the respective language. Moving to a REST
interface was necessary because we needed a language agnostic (at least
Python2 vs. 3 agnostic) way to access the DB and to allow a more flexible
interaction with the runsDB for the production services and general
user. The MongoDB developers also recommend using a REST interface
rather than the language-specific bindings directly

## Overall Design


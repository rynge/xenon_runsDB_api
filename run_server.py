from xenon_runsDB_api.app import app, config
if config["server"]["url"]:
    app.run(host=config["server"]["url"], 
            debug=config["server"]["debug"])
elif config["server"]["url"] and config["server"]["port"]:
    app.run(host=config["server"]["url"],
            post=config["server"]["port"],
            debug=config["server"]["debug"])
else:
    app.run(debug=config["server"]["debug"])
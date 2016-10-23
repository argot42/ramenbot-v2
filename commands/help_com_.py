def help(info):
    
    if not info["arguments"]:
        response = ("{} :List of Commands:".format(info["receiver"]),\
            "{} :|help|tell|src".format(info["receiver"]))

    elif info["arguments"][0] == "help":
        response = ("{} :help <command>".format(info["receiver"]),)

    elif info["arguments"][0] == "tell":
        response = ("{} :tell <user> <msg>".format(info["receiver"]),)

    elif info["arguments"][0] == "src":
        response = ("{} :src".format(info["receiver"]),)

    return response

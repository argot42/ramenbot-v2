def help(info):
    if info["receiver"][0] != "#": receiver = info["sender"]
    else: receiver = info["receiver"]
    
    if not info["arguments"]:
        response = ("{} :\x1FList of Commands:".format(receiver),\
            "{} :help | tell | info".format(receiver))

    elif info["arguments"][0] == "help":
        response = ("{} :help <command>".format(receiver),)

    elif info["arguments"][0] == "tell":
        response = ("{} :tell <user> <msg>".format(receiver),)

    elif info["arguments"][0] == "info":
        response = ("{} :Shows ramenbot's repo".format(receiver),)

    return response

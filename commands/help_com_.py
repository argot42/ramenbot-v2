def help(info):
    if info["receiver"][0] != "#": receiver = info["sender"]
    else: receiver = info["receiver"]
    
    if not info["arguments"]:
        response = ("{} :\x1FList of Commands:".format(receiver),\
            "{} :help | tell | src".format(receiver))

    elif info["arguments"][0] == "help":
        response = ("{} :help <command>".format(receiver),)

    elif info["arguments"][0] == "tell":
        response = ("{} :tell <user> <msg>".format(receiver),)

    elif info["arguments"][0] == "src":
        response = ("{} :src".format(receiver),)

    return response

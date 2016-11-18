def help(info):
    if info["receiver"][0] != "#": receiver = info["sender"]
    else: receiver = info["receiver"]
    
    if not info["arguments"]:
        response = ({"msg": "{} :\x1FList of Commands:".format(receiver)},\
            {"msg": "{} :help | tell | info".format(receiver)})

    elif info["arguments"][0] == "help":
        response = ({"msg": "{} :help <command>".format(receiver)},)

    elif info["arguments"][0] == "tell":
        response = ({"msg": "{} :tell <user> <msg>".format(receiver)},)

    elif info["arguments"][0] == "info":
        response = ({"msg": "{} :Shows ramenbot's repo".format(receiver)},)

    return response

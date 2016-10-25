def src(info):
    if info["receiver"][0] != "#": receiver = info["sender"]
    else: receiver = info["receiver"]

    return ("{} :https://github.com/argot42/ramenbot-v2".format(receiver),)

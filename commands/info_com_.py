def info(info):
    if info["receiver"][0] != "#": receiver = info["sender"]
    else: receiver = info["receiver"]

    return ({"msg": "{} :ramenbot 2.0 -> [https://github.com/argot42/ramenbot-v2]".format(receiver)},)

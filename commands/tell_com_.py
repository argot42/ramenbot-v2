def tell(info):
    # check if msg was sent as a private or chan msg
    if info["receiver"][0] != "#": 
        receiver = info["sender"]
        priv = 1
    else: 
        receiver = info["receiver"]
        priv = 0

    try:
        # raise exception if no usr provided as argument
        if not info["arguments"]: raise RuntimeError("No username provided to deliver msg")

        # insert msg into db
        info["database"].query("INSERT INTO msg(sender, receiver, body, priv) VALUES(?, ?, ?, ?)",\
                (info["sender"],\
                info["arguments"][0],\
                " ".join(info["arguments"][1:]),\
                priv))

        return ({"msg": "{} :The msg will be delivered :3".format(receiver)},)


    except IndexError:
        return ({"msg": "{} :Baka, that's not the command's syntax".format(receiver)},)

    except RuntimeError:
        return ({"msg": "{} :Baka, that's not the command's syntax".format(receiver)},)


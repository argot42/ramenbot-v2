def tell(info):
    try:
        # check if msg was sent as a private or chan msg
        priv = 0
        receiver = info["receiver"]
        if info["arguments"][0][0] != '#':
            priv = 1
            receiver = info["arguments"][0]

        # insert msg into db
        res = info["database"].query("INSERT INTO msg(body, sender_id, receiver_id, priv) VALUES(?, ?, ?, ?)",\
                (" ".join(info["arguments"][1:]),\
                info["sender"],\
                receiver,\
                priv)) 

    except IndexError:
        return ("{} :Baka, that's not the command's syntax".format(info["receiver"]),)

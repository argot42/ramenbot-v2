def checkon(info):
    msg = info["database"].query("SELECT * FROM msg WHERE receiver = ?",\
            (info["sender"],))

    # make irc msgs
    irc_msg = []
    for m in msg:
        if not m[4]: receiver = info["receiver"]
        else: receiver = m[3]

        irc_msg.append({"msg": "{} :{} left this msg for {}: {}".format(receiver, m[2], m[3], m[1])})

        info["database"].query("DELETE FROM msg WHERE msg_id = ?", (m[0],))


    return irc_msg

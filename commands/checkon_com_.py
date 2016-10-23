def checkon(info):
    msg = info["database"].query("SELECT user.nickname, msg.receiver_id, msg.body, msg.priv FROM msg JOIN user ON msg.sender_id = user.nickname WHERE msg.receiver_id = (?)", (info['sender'],)) 


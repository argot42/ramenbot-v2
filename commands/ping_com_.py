def ping(args):
    #return ({"event": "event test"},"test")
    #return ({"event": ["ping", [True, 0.0, args["arguments"][0], "test"]]},)
    return ({"event": ["reset", "ping"]},)

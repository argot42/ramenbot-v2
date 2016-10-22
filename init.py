import sys
import json
import os.path

from irc import IRC

# config path
cfg_path = "~/.ramenbot/ramenrc.json"

if len(sys.argv) >= 2:
    cfg_path = sys.argv[1]

# get config from json file
try:
    fd = open(os.path.expanduser(cfg_path), 'r')
    config = json.load(fd)

except FileNotFoundError as err:
    print("Configuration file not found [{0}]".format(cfg_path), file=sys.stderr)
    sys.exit(2)

except json.decoder.JSONDecodeError:
    print("Provide a valid json file as configuration", file=sys.stderr)
    sys.exit(1)


# try to connect to server
try:
    irc = IRC(host=config['host'], port=config['port'], nick=config['nick'], channels=config['channels'], database=os.path.expanduser(config['db']), 
            ssl=config['ssl'], prefix=config['prefix'], password=config['password'])
    irc.connect()

except KeyError:
    print("The configuration provided is not valid")
    sys.exit(1)

except KeyboardInterrupt:
    pass

finally:
    print("goodbye ❤")

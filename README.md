# ramenbot-v2
ramenbot - Love-filled, handcrafted, bad-coded, python irc bot ❤

###TODO
1. ~~Retry when connection fails~~

2. Trigger commands by a msg or time

3. Check if server is reachable (if not try to reconnect)

4. Another way to load commands that allow different langs

5. ???

###config.json
{

	"host" : "chat.freenode.net",

	"port" : 6697,

	"nick" : "ramenbot",

	"channels" : ["#sushigirl"],

	"prefix" : ".",

	"password" : false,

	"ssl" : true,

	"db" : "~/.ramenbot/ramen.db"

}

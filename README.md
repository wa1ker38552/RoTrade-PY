# RoTrade-PY

RoTrade is an API wrapper around trading, economy, and inventory related endpoints for Roblox used to create a Roblox client that can handle incoming and completed trades.

Written in a very shitty format as of now, (tried to replicate discord py but failing), feel free to create pull requests.

**Documentation**

Getting Started:

Examples are in RoTrade/examples/ directory and they include a basic client as well as a basic trade bot with accept and decline + bad countering algorithm
To create a client, use:
```py
client = roblox.Client('TOKEN or PATH to TOKEN')
```
For parameters, you can use the Settings subclass:
```py
params = roblox.Settings()
params.xcsrf_refresh = 120
params.roblox_refresh = 5

client = roblox.Client('TOKEN or PATH to TOKEN', settings=params)
```

There are 3 events you can listen to, the `on_trade_recieved` listener and the `on_trade_completed` listener. You can call them by creating a function with the listeners as the name and the client after being ran will automatically run them if a trade is completed or recieved. Both listeners return a Trade object.

The third event is the `on_ready` event which is ran after the client is set up on a class level.
```py
client = ...

def on_ready():
  print(client.user)
```

```py
clinet = ...

def on_trade_recieved(trade):
  print(trade.total_values())
  
def on_trade_completed(trade):
  print(trade.total_values())

client.run()
```

Client Object

A client object is the base client for RoTrade and handles all requests to Roblox and Rolimons as well as listener loops and refresh loops.

A Client object has the following attributes:
- request.Session `Client.client`
- int `Client.last_scanned_inbound`
- int `Client.last_scanned_outbound`
- int `Client.id`
- str `Client.xcsrf`
- str `Client.user`

Methods defined in Client are:
- `Client.run()`
- `Client.refresh_xcsrf()` (to force a manual refresh)

Manual x-csrf-token refresh:
```py
client.xcsrf = client.refresh_xcsrf()
```

Trade Object

A Trade object has the following attributes:
- int `Trade.id `
- int `Trade.user_id`
- int `Trade.offer_robux`
- int `Trade.request_robux`
- str `Trade.user_name`
- str `Trade.time`
- str `Trade.expiration`
- list `Trade.offer`
- list `Trade.request`

Inside `Trade.offer` and `Trade.request` are a list of Item objects. Additionally, a Trade object has a method defined called `Trade.total_values()` which calculates the total values for the trade. The method takes in `rap_only` or `value_only` as additional parameters. It is highly recommended that you calculate your own trades.
```py
def on_trade_received(trade):
  print(trade.total_values(value_only=True))
```

Item Object

A Item object has the following attributes:
- int `Item.id`
- int `Item.serial`
- int `Item.rap`
- int `Item.value`

The Item object is only created so that it is easier for users to fetch information rather than use a dictionary.

Inventory Object

To create an Inventory object, use:
```py
roblox.Inventory(id).items
```
> `[<Item Object>, ...]`

A Inventory object has the following attributes:
- list `Inventory.items`

Methods defined in Inventory are:
- `Inventory.total_values()`

```py
roblox.Inventory(id).total_values()['rap']
```
> `1000`


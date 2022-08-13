from roblox import roblox

params = roblox.Settings()
params.xcsrf_refresh = 120

client = roblox.Client('./token.txt', parameters=params)

def on_ready():
  print(client.user)

def on_trade_recieved(trade):
  total_values = trade.total_values()
  
  # your offer is less than their offer
  if total_values['offering']['offer_value'] > total_values['requesting']['request_value']:
    client.accept_trade(trade)
  else:
    # calculate loss threshold
    if total_values['offering']['offer_values']-total_values['requesting']['request_value'] in range(100, 500):
      # get self inventory
      my_inventory = roblox.Inventory(client.id)
      
      # counter trade
      inventory = roblox.Inventory(trade.user_id)
      request_items = []
      for item in inventory:
        total = sum([x.value for x in request_items])
        if total+item.value < my_inventory[0].value:
          request_items += item
        
      client.send_trade(trade.user_id,
                        [my_inventory[0].id],
                        [x.id for x in request_items[:4]])
    else:
      client.decline_trade(trade)

def on_trade_completed(trade):
  total_values = trade.total_values()
  rap_win = total_values['offering']['offer_rap']-total_values['requesting']['request_rap']
  value_win = total_values['offering']['offer_value']-total_values['requesting']['request_value']
  print('Trade completed! Yay!')
  print(f'RAP win: {rap_win}\nValue win: {value_win}')

if __name__ == '__main__':
  client.run()

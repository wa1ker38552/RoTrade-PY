from roblox import roblox

'''
Class used for creating a Trade object
A Trade object attributes are:
- id
- user_id
- user_name
- time
- expiration
- offer
- request
- offer_robux
- request_robux
Methods defined in Trade are:
- __init__()
- total_values()
'''

class Trade:
  # creates a trade object
  def __init__(self, client, trade):
    # create a temporary client for acccesing trades
    self.client = client
    
    # basic metadata
    self.id = int(trade['id'])
    self.user_id = int(trade['user']['id'])
    self.user_name = trade['user']['name']
    self.time = trade['created'].replace('T', ' ')[:trade['created'].index('.')]
    self.expiration = trade['expiration'].replace('T', ' ')[:trade['expiration'].index('.')]

    # trade values
    try:
      self.offer = []
      self.request = []
      request = self.client.get(f'https://trades.roblox.com/v1/trades/{self.id}').json()

      for item in request['offers'][0]['userAssets']:
        self.offer.append(roblox.Item(
          int(item['assetId']),
          int(item['serialNumber']) if not item['serialNumber'] is None else None,
          int(item['recentAveragePrice']),
          int(client.value_data[str(item['assetId'])][4]) if not client.value_data[str(item['assetId'])][4] == '-1' else int(item['recentAveragePrice'])
        ))
      for item in request['offers'][1]['userAssets']:
        self.request.append(roblox.Item(
          int(item['assetId']),
          int(item['serialNumber']) if not item['serialNumber'] is None else None,
          int(item['recentAveragePrice']),
          int(client.value_data[str(item['assetId'])][4]) if not client.value_data[str(item['assetId'])][4] == '-1' else int(item['recentAveragePrice'])
        ))
      self.offer_robux = request['offers'][0]['robux']
      self.request_robux = request['offers'][1]['robux']
        
    except KeyError:
      raise roblox.robloxError(request['errors'][0]['message'])

  # doesn't take into account robux !!
  def total_values(self, rap_only=False, value_only=False):
    if rap_only is True and value_only is True:
      raise roblox.tradeError('Both arguments cannot be True')
    elif rap_only is False and value_only is False:
      # loop through offers
      offer_rap = 0 
      offer_value = 0
      request_rap = 0
      request_value = 0
      for item in self.offer:
        offer_rap += item.rap
        offer_value += item.value
      for item in self.request:
        request_rap += item.rap
        request_value += item.value
      return {'offering': 
                {'offer_rap': offer_rap, 'offer_value': offer_value},
              'requesting':
                {'request_rap': request_rap, 'request_value': request_value}
             }
    elif rap_only is True:
      offer_rap = 0
      request_rap = 0
      for item in self.offer:
        offer_rap += item.rap
      for item in self.request:
        request_rap += item.rap
      return {'offering': 
                {'offer_rap': offer_rap},
              'requesting':
                {'request_rap': request_rap}
             }
    elif value_only is True:
      offer_value = 0
      request_value = 0
      for item in self.offer:
        offer_value += item.value
      for item in self.request:
        request_value += item.value
      return {'offering': 
                {'offer_value': offer_value},
              'requesting':
                {'request_value': request_value}
             }

import requests
from roblox import roblox

'''
Class used to track inventories
'''

class Inventory:
  def __init__(self, id):
    items = []
    value_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
    request = requests.get(f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?limit=100').json()
    
    # refresh page and append items
    next_page = request['nextPageCursor']
    for item in request['data']:
      items.append(
        roblox.Item(int(item['assetId']), 
                    int(item['serialNumber']) if not item['serialNumber'] is None else None, 
                    int(item['recentAveragePrice']),
                    int(value_data[str(item['assetId'])][4]) if not value_data[str(item['assetId'])][4] == '-4' else int(item['recentAveragePrice'])))

    while next_page != None:
      request = requests.get(f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?limit=100').json()
      next_page = request['nextPageCursor']
      for item in request['data']:
        items.append(
          roblox.Item(int(item['assetId']), 
                      int(item['serialNumber']) if not item['serialNumber'] is None else None, 
                      int(item['recentAveragePrice']),
                      int(value_data[str(item['assetId'])][4]) if not value_data[str(item['assetId'])][4] == '-4' else int(item['recentAveragePrice'])))
    self.items = items

  def total_values(self):
    total_values = {'rap': 0, 'value': 0}
    for item in self.items:
      total_values['rap'] += item.rap
      total_values['value'] += item.value
    return total_values

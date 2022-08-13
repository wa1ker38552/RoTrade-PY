import os
import sys
import time
import requests
import threading

'''
Client class to handle client level events
Login handler as well loop refreshes
'''

class Client:
  def __init__(self, token, parameters=None):
    self.file = sys.argv[0]
    self.file_data = __import__(self.file.replace('.py', ''))
    
    # get token paths/token
    if os.path.exists(token):
      with open(token, 'r') as file:
        self.token = file.read()
    else:
      self.token = token

    # declare settings
    if parameters is not None:
      self.parameters = parameters
    else:
      self.parameters = roblox.Settings()

    # log in
    self.client = requests.Session()
    self.client.cookies['.ROBLOSECURITY'] = self.token
    try:
      raise roblox.robloxError(self.client.get('https://auth.roblox.com/v1/account/pin').json()['errors'][0]['message'])
    except KeyError: 
      # succesfull authenticated

      self.xcsrf = threading.Thread(target=lambda: self.refresh_xcsrf()).start()
      self.value_data = threading.Thread(target=lambda: self.refresh_rolimons_loop()).start()
    
      # reset last scanned trade
      try:
        request = self.client.get(f'https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit={self.parameters.refresh_limit}', 
                                  headers={'x-csrf-token': self.xcsrf}).json()
        # self.last_scanned_inbound = request['data'][self.parameters.refresh_limit-1]['id']
        self.last_scanned_inbound = None
      except IndexError:
        self.last_scanned_inbound = None
      try:
        request = self.client.get(f'https://trades.roblox.com/v1/trades/Completed?sortOrder=Asc&limit={self.parameters.refresh_limit}', 
                                  headers={'x-csrf-token': self.xcsrf}).json()
        self.last_scanned_completed = request['data'][self.parameters.refresh_limit-1]['id']
      except IndexError:
        self.last_scanned_outbound = None

  def run(self):   
    # run loop to start threads
    with open(self.file) as file:
      if 'on_trade_recieved' in file.read():
        threading.Thread(target=self.on_trade_recieved_listener).start()
      if 'on_trade_completed' in file.read():
        threading.Thread(target=self.on_trade_completed_listener).start()
      if 'on_ready()' in file.read():
        self.file_data.on_ready()
        
  # basic loops and listeners
  def refresh_xcsrf_loop(self):
    while True:
      self.xcsrf = self.refresh_xcsrf()
      time.sleep(self.parameters.xcsrf_refresh)

  def refresh_rolimons_loop(self):
    while True:
      self.value_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
      time.sleep(self.parameters.rolimons_refresh)
      
  def on_trade_recieved_listener(self):
    while True:
      request = self.client.get(f'https://trades.roblox.com/v1/trades/Inbound?sortOrder=Asc&limit={self.parameters.refresh_limit}', 
                                headers={'x-csrf-token': self.xcsrf})
      try:
        request = request.json()['data']
        if request[0]['id'] != self.last_scanned_inbound:
          for index, item in enumerate(request):
            if not request[len(request)-index-1]['id'] == self.last_scanned_inbound:
              self.file_data.on_trade_recieved(roblox.Trade(self, request[len(request)-index-1]))
              self.last_scanned_inbound = request[len(request)-index-1]['id']
          
      except KeyError:
        raise roblox.robloxError(request['errors'][0]['message'])
      time.sleep(self.parameters.roblox_refresh)

  def on_trade_recieved_completed(self):
    while True:
      request = self.client.get(f'https://trades.roblox.com/v1/trades/Completed?sortOrder=Asc&limit={self.parameters.refresh_limit}', 
                                headers={'x-csrf-token': self.xcsrf})
      try:
        request = request.json()['data']
        for index, item in enumerate(request):
          if request[self.parameters.refresh_limit-index-1]['id'] != self.last_scanned_completed:
            for i in range(index):
              self.file_data.on_trade_completed(roblox.Trade(self, request[index-i-1]))
              self.last_scanned_completed = request[index-i-1]['id']
            break
          
      except KeyError:
        raise roblox.robloxError(request['errors'][0]['message'])
      time.sleep(self.parameters.roblox_refresh)

  # refreshes xcsrf token for roblox
  def refresh_xcsrf(self):
    response = self.client.post('https://auth.roblox.com/v1/login')
    if "X-CSRF-TOKEN" in response.headers:
      return response.headers["X-CSRF-TOKEN"]
    else:
      raise roblox.robloxError('Unable to locate refresh token!')

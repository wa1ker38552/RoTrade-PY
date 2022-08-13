'''
Class that sets up Settings later passed onto Client
Settings are run in Client.run()
'''

class Settings:
  def __init__(self,
    roblox_refresh=None,
    rolimons_refresh=None,
    xcsrf_refresh=None,
    refresh_limit=None):
    if roblox_refresh is None: self.roblox_refresh=10
    else: self.roblox_refresh = roblox_refresh
      
    if rolimons_refresh is None: self.rolimons_refresh=60
    else: self.rolimons_refresh = rolimons_refresh
      
    if xcsrf_refresh is None: self.xcsrf_refresh=60
    else: self.xcsrf_refresh = xcsrf_refresh

    if refresh_limit is None: self.refresh_limit=10
    else: self.refresh_limit = refresh_limit
      
  def default(self):
    self.roblox_refresh = 10
    self.rolimons_refresh = 60
    self.xcsrf_refresh = 60
    self.refresh_limit = 10

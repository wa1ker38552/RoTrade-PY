from roblox import roblox

params = roblox.Settings()
params = params.default()

client = roblox.Client('./token.txt', parameters=params)

def on_ready():
  print(clinet.user, client.id)
  
  for item in roblox.Inventory(client.id):
    print(item.id)
  print(roblox.Inventory(client.id).total_values())

if __name__ == '__main__':
  clinet.run()

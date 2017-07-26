"""
Import sample data for similar product engine
"""

import predictionio
import argparse
import xlrd
import random

def import_events(client):
  count = 0
  print client.get_status()
  print "Importing data..."

  # generate 10 users, with user ids u1,u2,....,u10
  user_ids = read_users('UsersPio.xlsx')
  for user_id in user_ids:
    print "Set user", user_id
    client.create_event(
      event="$set",
      entity_type="user",
      entity_id=user_id
    )
    count += 1

  # generate 50 items, with itemEntityId ids i1,i2,....,i50
  # random assign 1 to 4 categories among c1-c6 to items
  items = read_items('ItemsPio.xlsx')
  
  for item_info in items:
    item_id = item_info[1]
    category = item_info[0]
    print "Set itemEntityId", item_id
    client.create_event(
      event="$set",
      entity_type="item",
      entity_id=item_id,
      properties={
        "categories" : category
      }
    )
    count += 1

  item_ids = []
  for item_info in items:
    item_ids.append(item_info[1])

  # each user randomly viewed 5 items
  for user_id in user_ids:
    for viewed_item in random.sample(item_ids, 5):
      print "User", user_id ,"views itemEntityId", viewed_item
      client.create_event(
        event="view",
        entity_type="user",
        entity_id=user_id,
        target_entity_type="item",
        target_entity_id=viewed_item
      )
      count += 1

  # each user randomly bought 3  items
  for user_id in user_ids:
    for item in random.sample(item_ids, 3):
      print "User", user_id ,"buys itemEntityId", item
      client.create_event(
        event="buy",
        entity_type="user",
        entity_id=user_id,
        target_entity_type="item",
        target_entity_id=item
      )
      count += 1


  print "%s events are imported." % count

def read_users(file):
  book = xlrd.open_workbook(file)
  sheet = book.sheet_by_index(0)
  data = [sheet.cell_value(r, 0).encode('utf-8')  for r in range(sheet.nrows)]
  # Profit !
  print data
  return data

def read_items(file):
  book = xlrd.open_workbook(file)
  sheet = book.sheet_by_index(0)
  data = [[sheet.cell_value(r, c).encode('utf-8') for c in range(sheet.ncols)] for r in range(sheet.nrows)]
  # Profit !
  print data
  return data

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="Import sample data for similar product engine")
  parser.add_argument('--access_key', default='invalid_access_key')
  parser.add_argument('--url', default="http://localhost:7070")

  args = parser.parse_args()
  print args

  client = predictionio.EventClient(
    access_key=args.access_key,
    url=args.url,
    threads=5,
    qsize=500)
  import_events(client)
  #read_users('UsersPio.xlsx')
  #read_items('ItemsPio.xlsx')
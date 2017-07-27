"""
Import sample data for ECommerce product engine
"""

import predictionio
import argparse
import random
import xlrd
import ast

def read_users(file):
  book = xlrd.open_workbook(file)
  sheet = book.sheet_by_index(0)
  data = [sheet.cell_value(r, 0).encode('utf-8')  for r in range(sheet.nrows)]
  return data

def read_items(file):
  book = xlrd.open_workbook(file)
  sheet = book.sheet_by_index(0)
  data = [[sheet.cell_value(r, c).encode('utf-8') for c in range(sheet.ncols)] for r in range(sheet.nrows)]
  return data

def read_events(file):
  with open(file) as eventsFile:
    events = ast.literal_eval(eventsFile.read())
  return events

def import_events(client):
  count = 0
  print client.get_status()
  print "Importing data..."

  # read users from excel file
  user_ids = read_users('UsersPio.xlsx')
  for user_id in user_ids:
    print "Set user", user_id
    client.create_event(
      event="$set",
      entity_type="user",
      entity_id=user_id
    )
    count += 1

  # read items from excel file
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
        "category" : category
      }
    )
    count += 1

  # create an array with all the items
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

  for user_id in user_ids:
    for bought_item in random.sample(item_ids,3):
      print "User", user_id ,"buy itemEntityId", viewed_item
      client.create_event(
        event="buy",
        entity_type="user",
        entity_id=user_id,
        target_entity_type="item",
        target_entity_id=viewed_item
      )
      count += 1

  # # read events from json file
  # events = read_events('eventsPio.json')
  
  # #submit events 
  # for event in events:
  #   print "User", event['entity_id'], event['event'], event['target_entity_id']
  #   client.create_event(
  #     event=event['event'],
  #     entity_type=event['entity_type'],
  #     entity_id=event['entity_id'],
  #     target_entity_type=event['target_entity_type'],
  #     target_entity_id=event['target_entity_id']
  #   )
  #   count += 1


  print "%s events are imported." % count


#main function
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
  #read_events('eventsPio.json')
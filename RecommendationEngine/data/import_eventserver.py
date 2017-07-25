"""
Import sample data for similar product engine
"""

import predictionio
import argparse
import random

SEED = 3

def import_events(client):
  random.seed(SEED)
  count = 0
  print client.get_status()
  print "Importing data..."

  # generate 10 users, with user ids u1,u2,....,u10
  user_ids = ["%s" % i for i in ["Lucian", "Elena", "Cristian", "Catalin", "Ciprian", "Florin", "Larisa","Lucian", "Elena", "Cristian", "Catalin", "Ciprian", "Florin", "Larisa"]]
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
  categories = ["c%s" % i for i in ["Lactate", "Electronice", "Bricolaj", "Sucuri", "Ceaiuri"]]
  item_ids = ["i%s" % i for i in ["Lapte Covalact", "Televizor Samsung FullHD", "Ceai lamaie", "Coca cola", "Grebla"]]
  for item_id in item_ids:
    print "Set itemEntityId", item_id
    client.create_event(
      event="$set",
      entity_type="item",
      entity_id=item_id,
      properties={
        "categories" : random.sample(categories, random.randint(1, 4))
      }
    )
    count += 1

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

  # each user randomly bought 3 items
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


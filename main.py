#!/usr/bin/env python3

import os
import redis
import time

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from elasticsearch import Elasticsearch
from elasticsearch import helpers

class Runner:
	def __init__(self):	
		self.r = redis.Redis(os.getenv("HOST"), db=os.getenv("DB"))
		self.es = Elasticsearch(os.getenv("ELASTIC_HOST"))


	def elastic_send(self, events):
		actions = []
		for event in events:
			actions.append({
				"_index": os.getenv("INDEX")+'-'+datetime.today().strftime('%Y.%m.%d'),
				"_source": event[1]
		})
		helpers.bulk(self.es, actions)


	def run(self):
		while True:
			events = []
			streams = self.r.keys(os.getenv("STREAM_PATTERN"))
			for stream in streams:
				last_id = self.r.get("elastic:"+stream.decode())
				if not last_id:
					last_id = "0-0"
				redis_events = self.r.xread({stream:last_id})
				if not redis_events:
					continue
				events.extend(redis_events[0][1])
				self.r.set("elastic:"+stream.decode(), redis_events[0][1][-1][0])
				self.elastic_send(events)
				

			time.sleep(int(os.getenv("LOOP")))


if __name__ == "__main__":
	load_dotenv(find_dotenv())
	runner = Runner()
	runner.run()

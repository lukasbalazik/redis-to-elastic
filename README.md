# redis-to-elastic

Simple tool in python3 for reading streams from redis and sending to elastic index, we dont need logstash for simple tasks :)

.env:
```bash
REDIS_HOST="127.0.0.1:6379" # redis host
DB=0 # redis db
STREAM_PATTERN="organization:*" # pattern for our redis streams

ELASTIC_HOST="localhost:9200"
INDEX="events" # index name where we send data from redis (will add to name -acutal_date)
LOOP=1 # time in seconds for looping
```

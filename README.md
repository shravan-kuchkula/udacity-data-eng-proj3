# Data-Streaming-Using-Kafka
Stream data into Kafka and process the data using KSQL and Faust

## Producers
Mainly, we are going to be creating 3 Producers:

* The first thing we are going to do in this project is we're going to create a `Kafka Producer` which produces **train arrival** and **turnstile** information into our Kafka cluster. Arrivals will simply indicate that a train has arrived at a particular station and a turnstile event will simply indicate that a passenger has entered the station.
* Next, we are going to create a `REST Proxy Producer`. So, this will be a python script, that simply runs and periodically emits weather data via REST Proxy and puts it into Kafka.
* And, finally, we are going to build a `Kafka Connect` JDBC source connector, which is going to connect to Postgres and extract data from our stations table and place it into Kafka.

## Consumers
* On the other side of this, we are going to a `Kafka Consumer` to consume data from these Kafka topics.
* We are also going to be using `Faust` and `KSQL` to **extract** data and **transform** it.

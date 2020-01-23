# Data-Streaming-Using-Kafka
Stream data into Kafka and process the data using KSQL and Faust

**Project Description**: The Chicago Transit Authority (CTA) is interested in developing a data dashboard that displays the system status for its commuters. As their data engineer, I was tasked to build a **real-time stream processing data pipeline** that will take the *arrival* and *turnstile* events emitted by devices installed by CTA at each train station. The *station* data is located in an in-house POSTGRES database that needs to be leveraged by the pipeline to feed into the dashboard. Lastly, CTA also wishes to display the live *weather* data - which is served through a weather REST endpoint.

**Project architecture**: Since our goal is to get data from disparate systems to the dashboard, we can make use of Kafka and its ecosystem as an intermediary. Shown below is the high-level architecture of the flow of data into and out of Kafka using various components of the Kafka ecosystem, such as: `Kafka Connect` to ingest data from the database, `Kafka REST Proxy` to interface with a REST endpoint, `KSQL` to aggregate turnstile data at each station, `Faust` to transform the stream/table before it is consumed by the web server application running the dashboard.
![project-architecture](images/project-architecture.png)

## Producers
Mainly, we are going to be creating 3 Producers:

* The first thing we are going to do in this project is we're going to create a `Kafka Producer` which produces **train arrival** and **turnstile** information into our Kafka cluster. Arrivals will simply indicate that a train has arrived at a particular station and a turnstile event will simply indicate that a passenger has entered the station.
* Next, we are going to create a `REST Proxy Producer`. So, this will be a python script, that simply runs and periodically emits weather data via REST Proxy and puts it into Kafka.
* And, finally, we are going to build a `Kafka Connect` JDBC source connector, which is going to connect to Postgres and extract data from our stations table and place it into Kafka.

## Consumers
* On the other side of this, we are going to a `Kafka Consumer` to consume data from these Kafka topics.
* We are also going to be using `Faust` and `KSQL` to **extract** data and **transform** it.

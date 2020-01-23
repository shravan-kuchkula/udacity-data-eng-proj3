"""Defines trends calculations for stations"""
import logging
import faust

logger = logging.getLogger(__name__)

# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool

# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str

#  Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#  places it into a new topic with only the necessary information.
app = faust.App("stations-streams", broker="kafka://localhost:9092", store="memory://")

# Define the input Kafka Topic. Should be same topic as used by Kafka Connect
topic = app.topic("org.chicago.cta.stations", value_type=Station)

# Define the output Kafka Topic
out_topic = app.topic("org.chicago.cta.stations.transformed",
                      partitions=1,
                      key_type=str,
                      value_type=TransformedStation)

# Define a Faust Table
table = app.Table(
     "stations_table",
     default=TransformedStation,
     partitions=1,
     changelog_topic=out_topic,
)

# Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
@app.agent(topic)
async def transform_stations(stations):
    async for station in stations:

        # determine linecolor
        if station.red:
            linecolor = 'red'
        elif station.blue:
            linecolor = 'blue'
        elif station.green:
            linecolor = 'green'
        else:
            linecolor = 'unknown'

        transformed_station = TransformedStation(
            station_id = station.station_id,
            station_name = station.station_name,
            order = station.order,
            line = linecolor
        )

        await out_topic.send(key=station.station_name, value=transformed_station)


if __name__ == "__main__":
    app.main()

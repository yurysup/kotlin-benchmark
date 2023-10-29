import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import csv


BUCKET = "kotlinx-sandbox"
ORG = "tr"
INFLUX_URL="http://localhost:8086"
TOKEN = "TNB_q9VKKARIpJOneG6l3Hmqlncw_iMPf07LKAngJlXUVHDs63kRPwtMd7NqTXGENMG2dY1r7FHkkGLZC-6w9A=="
MEASUREMENT = "benchmark"
STAT_FILE = "benchmarks.csv"

client = influxdb_client.InfluxDBClient(
   url=INFLUX_URL,
   token=TOKEN,
   org=ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)

# convert raw point from csv to influxdb Point
def convert_point(raw_point:dict) -> influxdb_client.Point:
    return (influxdb_client.Point(MEASUREMENT)
    .tag("label", f'{raw_point["Benchmark"]}_n_{raw_point["Param: n"]}')
    .tag("env", 'local')
    .tag("mode", raw_point["Mode"])
    .field("score", round(float(raw_point["Score"]),2))
    .field("score_error", round(float(raw_point["Score Error (99.9%)"]),2)))


# batch write of points to influxdb
records = []
with open(STAT_FILE, "r") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for raw_point in csvreader:
        records.append(convert_point(raw_point))

write_api.write(bucket=BUCKET, org=ORG, record=records)

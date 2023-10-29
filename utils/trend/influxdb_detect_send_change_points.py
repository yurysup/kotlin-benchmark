import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from signal_processing_algorithms.energy_statistics import energy_statistics


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
query_api = client.query_api()

query = f'from(bucket: "{BUCKET}")\
|> range(start: -7d)\
|> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")\
|> filter(fn: (r) => r["_field"] == "score")\
|> group(columns: ["label", "env"], mode: "by")\
|> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'


result = query_api.query(org=ORG, query=query)
change_points = {}
timestamps = {}
for table in result:
    values = []
    timestamps_ = []
    for record in table.records:
        values.append(record.values['_value'])
        timestamps_.append(record.values['_time'])
    change_points[table.records[0].values['label']] = energy_statistics.e_divisive(values, pvalue=0.01, permutations=100)
    timestamps[table.records[0].values['label']] = timestamps_
print(change_points)
for label, cps in change_points.items():
    for index in cps:
        print(timestamps[label][index])

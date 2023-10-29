import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from signal_processing_algorithms.energy_statistics import energy_statistics


BUCKET = "kotlinx-sandbox"
ORG = "tr"
INFLUX_URL="http://localhost:8086"
TOKEN = "TNB_q9VKKARIpJOneG6l3Hmqlncw_iMPf07LKAngJlXUVHDs63kRPwtMd7NqTXGENMG2dY1r7FHkkGLZC-6w9A=="
MEASUREMENT = "benchmark"
CP_MEASUREMENT = "change_points"

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
for table in result:
    values = []
    timestamps = []
    for record in table.records:
        values.append(record.values['_value'])
        timestamps.append(record.values['_time'])
    cps = energy_statistics.e_divisive(values, pvalue=0.01, permutations=100)
    record_key = (table.records[0].values['label'], table.records[0].values['env'])
    change_points[record_key] = [timestamps[idx] for idx in cps]
#print(change_points)


def convert_point(raw_point:dict) -> influxdb_client.Point:
    return (influxdb_client.Point(CP_MEASUREMENT)
    .tag("label", raw_point['label'])
    .tag("env", raw_point['env'])
    .field("score", 1)
    .time(raw_point['timestamp']))

# batch write of change points to influxdb
records = []
for label, cps in change_points.items():
    raw_point = {}
    raw_point['label'] = label[0]
    raw_point['env'] = label[1]
    for cp in cps:
        raw_point['timestamp'] = cp
        records.append(convert_point(raw_point))

write_api.write(bucket=BUCKET, org=ORG, record=records)

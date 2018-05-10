from datadog import initialize, api
import time
from datetie import datetime

now = int(time.time())
dt_now = datetime.now()

year, month, day = dt_now.year, dt_now.month, dt_now.day

to = datetime(year, month, day, 23, 59).strftime("%s")
fr = datetime(year, month, day, 0, 0).strftime("%s")

initialize(api_key="", app_key="")

query = "sum:bidder.auctions{*}.as_rate()"
result = api.Metric.query(query=query, start=now-(86400*30), end=now)
result = api.Metric.query(query=query, start=fr, end=to)

def human_readable(result):
    out = []
    for s in result['series']:
        for p in s['pointlist']:
            out.append((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p[0]/1000.0)), p[1]))
    return out

times_and_qps = human_readable(result)
grouped_by_date = {}

for date, qps in times_and_qps:
    day = date[:10]
    time = date[11:]
    if day not in grouped_by_date:
        grouped_by_date[day] = []
    grouped_by_date[day].append((qps, time))

for date, qps_and_time in grouped_by_date.iteritems():
    print (date, sorted(qps_and_time, reverse=True)[0])

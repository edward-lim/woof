from datadog import initialize, api
import time
from datetime import datetime, timedelta

now = int(time.time())
dt_now = datetime.now()
days_back = 30

initialize()

query = "sum:bidder.auctions{env:prod}.as_rate()"
# result = api.Metric.query(query=query, start=now-(86400*30), end=now)

def human_readable(result):
    out = []
    for s in result['series']:
        for p in s['pointlist']:
            out.append((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p[0]/1000.0)), p[1]))
    return out


def max_of_day(result):
    times_and_qps = human_readable(result)
    grouped_by_date = {}

    for date, qps in times_and_qps:
        day = date[:10]
        time = date[11:]
        if day not in grouped_by_date:
            grouped_by_date[day] = []
        grouped_by_date[day].append((qps, time))

    for date, qps_and_time in grouped_by_date.iteritems():
        max_qps, time = sorted(qps_and_time, key=lambda x: x[0], reverse=True)[0]
        print("{}, {}, {}".format(date, time, max_qps))


for day_back in xrange(days_back):
    the_day = datetime.today() - timedelta(days=day_back)
    year, month, day = the_day.year, the_day.month, the_day.day
    end = datetime(year, month, day, 23, 59).strftime("%s")
    start = datetime(year, month, day, 0, 0).strftime("%s")
    result = api.Metric.query(query=query, start=start, end=end)
    max_of_day(result)

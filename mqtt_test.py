import asyncio
import time

import requests

data = [(1, 1)]

url = 'http://127.0.0.1:1880/aaao'
session = requests.Session()
session.get(url)


async def post(url, data):
    response = requests.post(url, data=data)
    return response

for i in range(100):
    time1 = time.perf_counter_ns()
    asyncio.run(post(url, data))
    time2 = (time.perf_counter_ns() - time1)/1000000
    print(f"{time2}")

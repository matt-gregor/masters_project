import csv
import time

import requests

# Define the URL of the endpoint
url = 'http://16.16.220.162:8090/your-endpoint'  # cloud
# url = 'http://127.0.0.1:8080/your-endpoint'    # on-premise
# Define the data to send in the request body

data = {
    'value': 15
}
sum = 0

# for i in range(100):
#     time1 = time.perf_counter_ns()
#     # Send the POST request to the endpoint
#     response = requests.post(url, json=data)
#     time2 = (time.perf_counter_ns() - time1)/1000000
#     print(time2)
#     sum += time2

# print(f"average response time: {sum/100} ms")

path = 'C:\\Projekty\\mgr\\measurements\\fastapi_session_times.csv'
header = "fastapi_time"
with open(path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([header])
    # for i in range(1000):
    #     time1 = time.perf_counter_ns()
    #     response = requests.post(url, json=data)
    #     time2 = (time.perf_counter_ns() - time1)/1000000
    #     writer.writerow([time2])
    #     print(time2)

    session = requests.Session()
    session.get(url)
    for i in range(1000):
        time1 = time.perf_counter_ns()
        response = session.post(url, json=data)
        time2 = (time.perf_counter_ns() - time1)/1000000
        writer.writerow([time2])
        print(time2)



# # Check the response status code
# if response.status_code == 200:
#     # Request was successful
#     result = response.json()
#     print('Result:', result)
# else:
#     # Request encountered an error
#     print('Error:', response.status_code, response.json())

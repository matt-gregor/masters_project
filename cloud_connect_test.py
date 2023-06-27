import time

import requests

# Define the URL of the endpoint
# url = 'http://16.16.220.162:8080/your-endpoint'  # cloud
url = 'http://127.0.0.1:8080/your-endpoint'    # on-premise
# Define the data to send in the request body

data = {
    'value': 15
}
sum = 0
for i in range(100):
    time1 = time.perf_counter_ns()
    # Send the POST request to the endpoint
    response = requests.post(url, json=data)
    time2 = (time.perf_counter_ns() - time1)/1000000
    print(time2)
    sum += time2

print(f"average response time: {sum/100} ms")
# # Check the response status code
# if response.status_code == 200:
#     # Request was successful
#     result = response.json()
#     print('Result:', result)
# else:
#     # Request encountered an error
#     print('Error:', response.status_code, response.json())

import csv
import os
import signal
import time

time_sum = 0
msg_count = 0


f = None


def close_file(signal_num, frame):
    global f
    if f:
        f.close()
    print("Program interrupted by Ctrl + C.")
    exit(0)


signal.signal(signal.SIGINT, close_file)


path = 'C:\\Projekty\\mgr\\measurements\\measurements1.csv'


if os.path.exists(path):
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
else:
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(['aa', 'bb', 'cc','dd','ee'])


data = {
        'SetPoint': 4,
        'a': str([3, 1])
            }
d = [data[a] for a in data]

print(d)
d.extend([1,3])
print(d)
for i in range(1000):
    time1 = time.perf_counter_ns()
    data2 = [1, 2.0, 'amogus1', 69, 3]
    writer.writerow(data2)
    time2 = (time.perf_counter_ns() - time1)/1000000
    time_sum += time2
    msg_count += 1
average = time_sum / msg_count
print(average)
f.close()

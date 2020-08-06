# OMEGA3 Prototype ver.
# Need some Direct Command inputs in SCION VM
# Results Can be different by VM Settings, Network Status, ...

import subprocess
import time
import omega3

Core_AS = [
    "18-ffaa:0:1201",
    "17-ffaa:0:1101",
    "20-ffaa:0:1401",
    "16-ffaa:0:1006",
    "23-ffaa:0:1701"
]

Source_Core_AS = Core_AS[0]
Destination_Core_AS = [Core_AS[3], Core_AS[4]]
Destination_AS = "22-ffaa:0:1601"


def detect():
    f = open('./normal_ping.txt', 'r')
    sum_ttl = 0.0

    for i in range(5):
        line = f.readline()
        item = line.split("=")
        ttl = item[2]
        sum_ttl += float(ttl)

    avg_ttl = sum_ttl / 5

    while True:
        line = f.readline()
        item = line.split("=")
        ttl = item[2]
        last_ttl = float(ttl)
        avg_ttl = (avg_ttl * 0.8) + (last_ttl * 0.2)    # exponential average

        if (avg_ttl / last_ttl) < 0.8:     # Threshold = 0.8 (Temporary)
            omega_3()
            f.close()
            break


def omega_3():
    # Phase 1
    avail_paths = [5000, 5000, 5000, 5000]
    unavail_paths = [-1, -1, -1, -1]

    for path in range(2):
        omega3.PingToTargetAS(Source_Core_AS, path)
    time.sleep(10)
    for path in range(2):
        result = omega3.IsAvailable(Source_Core_AS, path)

        if not result:      # Unavailable
            unavail_paths[path] = path
        else:               # Available
            avail_paths[path] = result

    temp_paths = avail_paths
    temp_paths.sort()

    if temp_paths[0] != 5000:   # Available Path exists
        min_ttl = temp_paths[0]
    else:                       # Communication Impossible
        print("Communication Impossible in Phase 1..")
        print("All paths are affected..")
        return

    for i in range(2):
        if avail_paths[i] == min_ttl:
            min_path = i
            break

    # Phase 2
    avail_paths = [5000, 5000, 5000, 5000]
    unavail_paths = [-1, -1, -1, -1]

    for k in range(2):
        for path in range(4):
            omega3.PingToTargetAS(Destination_Core_AS[k], path)
        time.sleep(10)
        for path in range(4):
            result = omega3.IsAvailable(Destination_Core_AS[k], path)

            if not result:      # Unavailable
                unavail_paths[path] = path
            else:               # Available
                avail_paths[path] = result

        temp_paths = avail_paths
        temp_paths.sort()

        if temp_paths[0] != 5000:   # Available Path exists
            min_ttl = temp_paths[0]
        else:                       # Communication Impossible
            print("Communication Impossible to {0}".format(Destination_Core_AS[k]))
            if k == 1:      # Every Core Paths are affected
                print("Communication Impossible in Phase 2..")
                print("All paths are affected..")
                return
            continue

        for i in range(2):
            if avail_paths[i] == min_ttl:
                min_path = i
                break

    # Phase 3
    avail_paths = [5000, 5000, 5000, 5000]
    unavail_paths = [-1, -1, -1, -1]

    for path in [1, 3, 6, 8]:
        omega3.PingToTargetAS(Destination_AS, path)
    time.sleep(10)
    for path in [1, 3, 6, 8]:
        result = omega3.IsAvailable(Destination_AS, path)

        if not result:      # Unavailable
            unavail_paths[path] = path
        else:               # Available
            avail_paths[path] = result

    temp_paths = avail_paths
    temp_paths.sort()

    if temp_paths[0] != 5000:   # Available Path exists
        min_ttl = temp_paths[0]
    else:                       # Communication Impossible
        print("Communication Impossible in Phase 3..")
        print("All paths are affected..")
        return

    for i in range(2):
        if avail_paths[i] == min_ttl:
            min_path = i
            print("Optimal Path found!..")
            print("Optimal Path to {0} is Path {1}".format(Destination_AS, min_path))
            break

    return


subprocess.call('scmp echo -remote {0},[0.0.0.0] | tee -a ./normal_ping.txt'.format(Destination_AS), shell=True)
time.sleep(10)
detect()
print("End of Simulation")

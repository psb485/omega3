# Functions for OMEGA3
# Need some Direct command in SCION VM
# Can be different by VM Settings, Network Status, ...

import subprocess

def PingToTargetAS(AS_Name, Path_Num):
    subprocess.call('scmp echo -remote {0},[0.0.0.0] -i \
    | tee -a ./omega_{0}_path_{1}.txt'.format(AS_Name, Path_Num), shell=True)

def IsAvailable(AS_Name, Path_Num):
    f = open('./omega_{0}_path_{1}.txt'.format(AS_Name, Path_Num), 'r')
    sum_ttl = 0.0

    for i in range(5):
        line = f.readline()
        item = line.split("=")
        ttl = item[2]
        sum_ttl += float(ttl)

    avg_ttl = sum_ttl / 5

    for i in range(5):
        line = f.readline()
        item = line.split("=")
        ttl = item[2]
        last_ttl = float(ttl)
        avg_ttl = (avg_ttl * 0.8) + (last_ttl * 0.2)    # exponential average

        if (avg_ttl / last_ttl) < 0.8:     # Threshold = 0.8 (Temporary), Affected by DDoS
            print("Path {0} to AS {1} is affected by Link Flooding DDoS..".format(Path_Num, AS_Name))
            print("Unavailable...")
            f.close()
            return False

        else:
            if i < 4:
                continue
            else:
                print("Path {0} to AS {1} is NOT affected by Link Flooding DDoS!".format(Path_Num, AS_Name))
                print("Available!...")
                f.close()
                return avg_ttl

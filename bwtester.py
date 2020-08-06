# DDoS Simulation with SCION bandwidth tester
# DDoS Affected Links: SCION_KU - 1404 - 1402 - 1401 - 1006 - 1005

# (S->C) Attempted Bandwidth: 48000000bps / 48.00Mbps
# (C->S) Attempted Bandwidth: 64000000bps / 64.00Mbps

import subprocess
import time


DDoS_Target_AS = "16-ffaa:0:1005,[172.31.26.94]:30100"


def bwtest(num):
    subprocess.call("scion-bwtestclient -s {0} -cs 10,1000,80000,? -sc 10,1000,60000,? \
    | tee -a ./DDoS_bwtester_{1}.txt".format(DDoS_Target_AS, num))


for i in range(4):
    bwtest(i)
    time.sleep(25)
    print("[{0}] DDoS Simulation".format(i))
# Parser for ping logs
# Extract TTL Data for drawing chart
# Unit: ms(millisecond)

input_file = open('C:/PATH/TO/INPUT/PING_LOG.txt', 'r')
output_file = open('C:/PATH/TO/OUTPUT/PING_LOG.txt', 'w')

lines = input_file.readlines()
for line in lines:
    item = line.split("=")
    #seq = item[1]
    time = item[2]
    #output_file.write(seq[0:2])
    #output_file.write(" ")
    output_file.write(time[0:7])
    output_file.write("\n")

input_file.close()
output_file.close()
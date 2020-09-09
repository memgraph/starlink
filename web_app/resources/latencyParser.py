import csv


readFromFile = open("latenciesTables.txt", "r")
lines = readFromFile.readlines()
cleanLines = []

for line in lines:
    newLine = line.split("\t")
    newLine.pop()
    cleanLines.append(newLine)


with open("latencies.csv", mode="w", newline='') as latencies:
    latency_writer = csv.writer(latencies, delimiter=",")
    header = ["Source", "Destination", "Latency"]
    latency_writer.writerow(header)
    for i in range(1, len(cleanLines)):
        for j in range(1, len(cleanLines[i])):
            source = cleanLines[i][0]
            destination = cleanLines[0][j]
            latency = cleanLines[i][j]
            if(source != destination):
                latency = latency[:-2]
                builder = [source, destination, latency]
                latency_writer.writerow(builder)
    print("success")

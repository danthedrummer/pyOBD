import json, csv

data = []

with open('recorded_obd_data', 'r') as file:
  for line in file.readlines():
    data.append(json.loads(line))

with open('recorded_obd_data.csv', 'w') as file:
  writer = csv.writer(file)
  row = []

  for key in data[0].keys():
    row.append(key)
  writer.writerow(row)

  for set in data:
    row = []
    for key in set:
      row.append(set[key])
    writer.writerow(row)

import csv, os, requests, re

csv_file = 'daz-images-new.csv'
output_folder = 'output'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

with open(csv_file) as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        # 0 web-scraper-order
        # 1 web-scraper-start-url
        # 2 product image-src
        # 3 id
        file_type = re.findall('.[a-z]+', row[2])
        file_type = file_type[len(file_type) -1]
        file_final = output_folder + '\\' + row[3] + file_type

        if os.path.isfile(file_final):
            print(row[3] + ' already downloaded')
            continue

        with open(file_final, 'wb') as cur_file:
            print(row[3])
            try:
                r = requests.get(row[2])
                cur_file.write(r.content)
            except requests.exceptions.MissingSchema:
                continue
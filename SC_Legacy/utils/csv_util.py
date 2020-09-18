import csv


# def get_csv_data1(file_name):
#     rows = []
#     data_file = open(file_name, "r")
#     reader = csv.reader(data_file)
#     # skip the headers
#     next(reader)
#     # add rows from reader to list
#     for row in reader:
#         rows.append(row)
#     return rows


def get_csv_data(file_name):
    rows = []
    with open(file_name, "r") as data_file:
        # data_file.seek(0)
        reader = csv.reader(data_file)
        # skip the headers
        next(reader)
        # add rows from reader to list
        for row in reader:
            rows.append(row)
        # data_file.seek(0)
    return rows

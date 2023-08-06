import os
import csv


def split(filepath, target_dir, column_set):
    os.makedirs(os.path.dirname(target_dir + '/'), exist_ok=True)
    print(f"writing to '{target_dir}' directory")

    for fIndex in range(len(column_set)):
        remove(data_file(fIndex, target_dir, filepath))

    rows = 0
    columns = {}
    files = []

    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')

        for i in range(len(column_set)):
            files.append(open(data_file(i, target_dir, filepath), 'a'))

        for row in reader:
            read_columns = 0
            for i in range(len(column_set)):
                f = files[i]
                w = csv.writer(f, delimiter=',')
                row_subset = row[read_columns:read_columns + column_set[i]]
                w.writerow(row_subset)
                read_columns += column_set[i]
                columns.update({i: len(row_subset)})
            rows += 1
            print(f"\rprogress: {rows} rows processed", end="")

    for f in files:
        f.close()

    print(f"\n\r{len(column_set)} file(s) created")
    for i in range(len(column_set)):
        print(f"\t - {data_file(i, target_dir, filepath)} [{columns[i]} column(s)]")


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def data_file(i, target_dir, input_file):
    f_name_with_extension = os.path.basename(input_file)
    segments = list(filter(lambda x: x != '', f_name_with_extension.split(".csv")))
    return f'{target_dir}/{segments[0]}_{i + 1}.csv'
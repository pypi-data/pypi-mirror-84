#!/usr/bin/python3

import csv
import getopt
import os
import sys
import math
import pathlib


def main():
    argv = sys.argv[1:]
    input_file = ''
    output_dir = 'output'
    split_pattern = ''
    batch_size = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:p:b:", ["inputFile=", "outputDir=", "splitPattern=", "batchSize="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt in ("-i", "--inputFile"):
            input_file = arg
        elif opt in ("-o", "--outputDir"):
            output_dir = arg
        elif opt in ("-p", "--splitPattern"):
            split_pattern = arg
        elif opt in ("-b", "--batchSize"):
            batch_size = arg

    if input_file == '':
        print("please specify input file")
        print_help(2)

    if (split_pattern == '') & (batch_size == ''):
        print("please specify split pattern or batch size")
        print_help(2)

    file = pathlib.Path(input_file)
    if not file.exists():
        print("input file does not exist")
        sys.exit(1)

    csv_columns = get_column_length(input_file)
    print(f"reading {input_file}")
    print(f"total {csv_columns} column(s)")

    if split_pattern != '':
        sp = list(map(int, split_pattern.split(',')))
        sp_sum = sum(sp)
        if sp_sum > csv_columns:
            print(f"split pattern contains more columns ({sp_sum}) than csv ({csv_columns})")
            sys.exit(1)
        split(input_file, output_dir, sp)
    else:
        files = math.ceil(csv_columns / int(batch_size))
        sp = [int(batch_size)] * files
        split(input_file, output_dir, sp)


def print_help(exit_code=0):
    print('csv-split -i <inputFile> -o <outputDir> (default: output/) -p <splitPattern> (comma separated)\n'
          'OR\n'
          'csv-split -i <inputFile> -o <outputDir> (default: output/) -b <batchSize>')
    sys.exit(exit_code)


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def data_file(i, target_dir, input_file):
    f_name_with_extension = os.path.basename(input_file)
    segments = list(filter(lambda x: x != '', f_name_with_extension.split(".csv")))
    return f'{target_dir}/{segments[0]}_{i + 1}.csv'


def get_column_length(filepath):
    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        return len(next(reader))


def split(filepath, target_dir, column_set):
    os.makedirs(os.path.dirname(target_dir + '/'), exist_ok=True)
    print(f"writing to '{target_dir}' directory")

    for fIndex in range(len(column_set)):
        remove(data_file(fIndex, target_dir, filepath))

    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        rows = 0
        columns = {}
        for row in reader:
            read_columns = 0
            for i in range(len(column_set)):
                f = open(data_file(i, target_dir, filepath), 'a')
                w = csv.writer(f, delimiter=',')
                row_subset = row[read_columns:read_columns + column_set[i]]
                w.writerow(row_subset)
                read_columns += column_set[i]
                columns.update({i: len(row_subset)})
                f.close()
            rows += 1
            print(f"\rprogress: {rows} rows processed", end="")
    print(f"\n\r{len(column_set)} file(s) created")
    for i in range(len(column_set)):
        print(f"\t - {data_file(i, target_dir, filepath)} [{columns[i]} column(s)]")


if __name__ == '__main__':
    main()

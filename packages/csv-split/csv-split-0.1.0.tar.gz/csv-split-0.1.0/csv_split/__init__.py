import csv
import getopt
import sys
import math
import pathlib
from csv_split.splitter import split
from horology import timed
from importlib.metadata import version


@timed
def run():
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
    print(f'[csv-split] version: {version("csv-split")}\n'
          ':: split csv files by columns ::\n'
          '\n'
          'USAGE:\n'
          'csv-split -i <inputFile> -o <outputDir> (default: output/) -p <splitPattern> (comma separated)\n'
          'OR\n'
          'csv-split -i <inputFile> -o <outputDir> (default: output/) -b <batchSize>')
    sys.exit(exit_code)


def get_column_length(filepath):
    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        return len(next(reader))

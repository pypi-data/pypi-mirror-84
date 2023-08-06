# SplitCSV

## Vertical splitting (columns)
Splits a given CSV file vertically.
Accepts either a batch-size, or a split-pattern to create multiple files
from a single files. All files will contain different columns of original csv.
Order of columns will be maintained.

## Horizontal splitting (rows)

Not supported yet

## Usage

The below command will take large-file.csv and split it vertically into 3 files.
First file will have 10 columns, 2nd file will have 5, and the 3rd will have 12.
If there are more columns in the original file, they will be ignored.   

```bash
splitcsv -i ~/Downloads/large-file.csv -p 10,5,12
```

By default, all the output files will be stored in a new directory called 
`output`. Generated file names will have index number appended. For example,
`large-file_1.csv`, `large-file_2.csv`, ...

If you want to change the output directory, you can use `-o` option as shown below.

 
```bash
splitcsv -i ~/Downloads/large-file.csv -p 10,5,12 -o ~/Downloads/splitted-data/
```

If this directory does not exist, it will be created.

Instead of split-pattern, you can also specify batch size.

```bash
splitcsv -i ~/Downloads/large-file.csv -b 7
```

This will create csv files and each csv file will contain 7 columns. Number of output files will
depend on number of columns in input files.
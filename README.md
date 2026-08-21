# CSV Data Processor

A command-line Python application for processing CSV files.

The program validates CSV data, filters records, calculates statistics, and creates a cleaned CSV file containing only valid records.

## Features

* Validates the input file and checks that it is a `.csv` file.
* Checks whether the CSV file is empty.
* Validates required columns:

  * `name`
  * `age`
  * `salary`
  * `department`
* Validates row values.
* Skips invalid rows.
* Filters records by:

  * name
  * minimum age
  * maximum age
  * department
  * minimum salary
  * maximum salary
* Calculates statistics:

  * total number of records
  * average salary
  * minimum salary
  * maximum salary
  * number of employees in each department
* Creates a cleaned CSV file containing only valid rows.
* Processes CSV data using generators for memory-efficient streaming.

## Requirements

* Python 3.x
* No external dependencies

The project uses only Python's standard library:

* `csv`
* `pathlib`
* `argparse`

## CSV Format

The input CSV file must contain the following columns in this order:

```csv
name,age,salary,department
Alice,25,3200,IT
Bob,31,4100,HR
Charlie,22,2800,IT
```

## Usage

Basic command:

```bash
python main.py path/to/file.csv
```

### Calculate Statistics

```bash
python main.py employees.csv --stats
```

Example output:

```text
Total records: 3
Average salary: 3366.67
Maximum salary: 4100
Minimum salary: 2800

Employees by department:
IT: 2
HR: 1
```

### Filter by Name

```bash
python main.py employees.csv --stats --name Alice
```

### Filter by Minimum Age

```bash
python main.py employees.csv --stats --min_age 25
```

### Filter by Maximum Age

```bash
python main.py employees.csv --stats --max_age 40
```

### Filter by Department

```bash
python main.py employees.csv --stats --department IT
```

### Filter by Salary

Minimum salary:

```bash
python main.py employees.csv --stats --min_salary 3000
```

Maximum salary:

```bash
python main.py employees.csv --stats --max_salary 5000
```

### Combine Filters

Filters can be combined:

```bash
python main.py employees.csv --stats --department IT --min_age 25 --min_salary 3000
```

### Create a Cleaned CSV

To create a new CSV file containing only valid rows:

```bash
python main.py employees.csv --clean_data
```

The cleaned file will be created in the same directory as the original file.

For example:

```text
employees.csv
cleaned_employees.csv
```

## Data Validation

A row is considered invalid if:

* one or more values are missing;
* `age` is less than 18.
* `salary` less than 100.
* `age` is not a number;
* `salary` is not a number;
* `name` contains non-alphabetical characters;
* `department` contains non-alphabetical characters.

Invalid rows are skipped during processing.
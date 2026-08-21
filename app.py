import csv
from pathlib import Path
import argparse

FIELDS = ["name", "age", "salary", "department"]

def get_csv(path: Path) -> Path:
    '''Returns the path to csv'''

    path_to_csv_file = Path(path)

    if not path_to_csv_file.is_file():
        raise ValueError("Your path refers to something, but not file.")

    if not path_to_csv_file.suffix == '.csv':
        raise ValueError("It's not a .csv file")

    return path_to_csv_file


def row_validator(row: dict) -> bool:
    '''Checks if the row's values are valid'''

    if any(data is None for data in row.values()):
        print(f"Missing value(-s): {row}")
        return False
    name, age, salary, department = row["name"].strip(), row["age"].strip(), row["salary"].strip(), row["department"].strip()
    if any((not age.isdigit(), not salary.isdigit(), not name.isalpha(), not department.isalpha())):
        return False
    if int(age) < 18 or int(salary) < 100:
        return False
    return True


def retrieve_data(csv_file: Path):
    '''Retrieves all data with filters'''

    with csv_file.open('r', encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        columns = reader.fieldnames
        if not columns:
            raise ValueError("File is empty")
        if [c.strip().lower() for c in columns] != FIELDS:
            raise ValueError(f"Fields are not valid. Valid fields: {FIELDS}")

        for row in reader:  # достает данные
            if not row_validator(row):
                print(f"\nInvalid row: {row}\n")
                continue
            yield row


def filter_row(row: dict, name: str, min_age: int, department: str, max_age: int, max_salary: int, min_salary: int):
    '''Filters row'''
    if min_age is not None and int(row["age"].strip()) < min_age:
        return
    
    if max_age is not None and int(row["age"].strip()) > max_age:
        return
    
    if department is not None and row["department"].strip() != department:
        return
    
    if name is not None and row["name"].strip() != name:
        return
    
    if max_salary is not None and int(row["salary"].strip()) > max_salary:
        return
    
    if min_salary is not None and int(row["salary"].strip()) < min_salary:
        return

    return row


def parser_engine():
    '''Creates parser and returns retrieved args'''

    parser = argparse.ArgumentParser()
    parser.add_argument("path")

    parser.add_argument("--name", type=str, help="Name filter")
    parser.add_argument("--min_age", type=int, help="Minimum age filter")
    parser.add_argument("--max_age", type=int, help="Maximum age filter")
    parser.add_argument("--department", type=str, help="Department filter")
    parser.add_argument("--min_salary", type=int, help="Minimum salary filter")
    parser.add_argument("--max_salary", type=int, help="Maximum salary filter")
    parser.add_argument("--stats", action="store_true", help="Statistics parameter")
    parser.add_argument("--clean_data", action="store_true", help="Creates a new file with valid rows.")

    args = parser.parse_args()
    return args


def info(csv_file: Path, name: str, min_age: int, department: str, max_age: int, max_salary: int, min_salary: int):
    '''Collects and prints data'''

    departments = []
    sum_of_salaries = 0
    minimum_salary, maximum_salary = None, None
    for row in retrieve_data(csv_file):
        data = filter_row(row, name, min_age, department, max_age, max_salary, min_salary)
        if data is None:
            continue
        departments.append(data["department"].strip())
        salary = int(data["salary"])
        sum_of_salaries += salary

        if minimum_salary is None or salary < minimum_salary:
            minimum_salary = salary
        if maximum_salary is None or salary > maximum_salary:
            maximum_salary = salary

    departments_set = set(departments)
    entries = len(departments)
    try: 
        av_salary = sum_of_salaries / entries 
    except ZeroDivisionError:
        print("No records matched the filters.")
    else:    
        print(f"Total records: {entries}")
        print(f"Average salary: {av_salary}\nMaximum salary: {maximum_salary}\nMinimum salary: {minimum_salary}")

        print("\nEmployees by department:")
        for department in departments_set:
            print(f"{department}: {departments.count(department)}")


def clean_csv(csv_file: Path):
    '''Retrieves only valid rows and inserts them into new .csv file.'''

    with open(csv_file.parent / f"cleaned_{csv_file.stem}.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for row in retrieve_data(csv_file): 
            writer.writerow(row)
    print("File was successfully written")    


def main():
    '''Main function: gets args from cli and executes users's request.'''
    args = parser_engine()
    clean_data, stats, path, min_age, max_age, department, name, max_salary, min_salary = args.clean_data, args.stats, args.path, args.min_age, args.max_age, args.department, args.name, args.max_salary, args.min_salary

    csv_file = get_csv(path) 

    if stats:
        info(csv_file=csv_file, min_age=min_age, max_age=max_age, department=department, max_salary=max_salary, min_salary=min_salary, name=name) 

    if clean_data:
        clean_csv(csv_file=csv_file)


if __name__ == "__main__":
    main()
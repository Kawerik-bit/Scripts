import sys
import os
import re

def error_search(log_file):
    error = input("What error are you looking for? ").strip()
    returned_errors = []
    error_pattern = re.compile(r"\b{}\b".format(re.escape(error.lower())), re.IGNORECASE)

    try:
        with open(log_file, mode='r', encoding='UTF-8') as file:
            for log in file:
                if 'error' in log.lower() and error_pattern.search(log.lower()):
                    returned_errors.append(log)
    except FileNotFoundError:
        print(f"Error: The file '{log_file}' was not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{log_file}': {e}")
        sys.exit(1)

    return returned_errors

def file_output(returned_errors):
    output_dir = os.path.expanduser('~') + '/data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'errors_found.log')

    with open(output_file, 'w', encoding='UTF-8') as file:
        file.writelines(returned_errors)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    returned_errors = error_search(log_file)
    file_output(returned_errors)
    print(f"Found {len(returned_errors)} errors. See '{os.path.expanduser('~')}/data/errors_found.log'.")
    sys.exit(0)

  
  # Script for searching for errors in the log file
  # #!/usr/bin/env python3 can be added to the top to make the file executable without the need of invoking python
  # python3 search_errors_log.py - to invoke the script otherwise, specify what you are looking for in the input

import json
import csv


def load_data(file_name: str):
    try:
        # Load JSON data
        data_path = file_name
        with open(data_path, 'r') as file:
            json_data = json.load(file)

        return json_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def save_result_as_csv(result_data, file_name: str = 'output.csv'):
    # Specify the file path
    csv_file_path = file_name

    # Get the header from the first dictionary
    header = list(result_data[0].keys())

    # Write to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)

        # Write the header
        writer.writeheader()

        # Write the data
        writer.writerows(result_data)

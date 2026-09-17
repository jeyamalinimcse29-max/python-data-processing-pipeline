import csv


def read_data(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    return data


if __name__ == "__main__":
    file_path = r"C:\Users\jeyam\Downloads\yuvtech\input.csv"
    data = read_data(file_path)
    print(data)
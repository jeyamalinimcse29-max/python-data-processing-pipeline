def clean_data(data):

    cleaned_data = []

    for row in data:

        # Handle missing age
        if row["age"] == "":
            row["age"] = "0"

        # Convert age to integer
        try:
            row["age"] = int(row["age"])
        except ValueError:
            row["age"] = 0

        # Handle missing salary
        if row["salary"] == "":
            row["salary"] = "0"

        # Convert salary to float
        try:
            row["salary"] = float(row["salary"])
        except ValueError:
            row["salary"] = 0.0

        # Handle missing department
        if row["department"] == "":
            row["department"] = "Unknown"

        cleaned_data.append(row)

    return cleaned_data
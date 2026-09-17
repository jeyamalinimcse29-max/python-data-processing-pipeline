def transform_data(data):

    transformed_data = []

    for row in data:

        salary = row["salary"]

        if salary < 20000:
            row["salary_category"] = "Low"
        elif salary <= 40000:
            row["salary_category"] = "Medium"
        else:
            row["salary_category"] = "High"

        transformed_data.append(row)

    return transformed_data
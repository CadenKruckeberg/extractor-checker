def standardize_my_grades(rows: list):
    standardized = []

    for row in rows[1:]:
        working_row = row
        working_row = working_row[5:]

        a = working_row[0].split()[0]
        b = working_row[0].split()[1]
        working_row[0] = a
        working_row.insert(1, b)

        standardized.append(working_row)

    return standardized

def standardize_madgrades_grades(rows: list):
    standardized = []

    for row in rows:
        working_row = row
        working_row = working_row[1:]

        try:
            int(working_row[0])
        except:
            continue

        working_row[1] = working_row[1].split()[0]

        standardized.append(working_row)

    return standardized

def standardize_my_dir_1(rows: list):
    standardized = []

    for row in rows[1:]:
        working_row = row

        working_row = working_row[1:]

        day_string = ''
        day_string += " ".join(day for day in working_row[6:13] if day) + " "
        day_string = day_string.strip()
        working_row = working_row[:6] + [day_string] + working_row[13:]

        standardized.append(working_row)

    return standardized

def standardize_madgrades_dir_1(rows: list):
    standardized = []

    for row in rows:
        working_row = row

        try:
            int(working_row[1])
        except:
            continue

        standardized.append(working_row)

    return standardized

def standardize_my_dir_2(rows: list):
    standardized = []

    for row in rows[1:]:
        working_row = row

        working_row = working_row[1:]

        day_string = ''
        day_string += " ".join(day for day in working_row[5:12] if day) + " "
        day_string = day_string.strip()
        working_row = working_row[:5] + [day_string] + working_row[12:]

        standardized.append(working_row)

    return standardized

def standardize_madgrades_dir_2(rows: list):
    standardized = []

    for row in rows:
        working_row = row

        try:
            int(working_row[1])
        except:
            continue

        standardized.append(working_row)

    return standardized

def standardize_my_dir_3(rows: list):
    standardized = []

    for row in rows[1:]:
        working_row = row

        working_row = working_row[2:]

        day_string = ''
        day_string += " ".join(day for day in working_row[6:13] if day) + " "
        day_string = day_string.strip()
        working_row = working_row[:6] + [day_string] + working_row[13:]

        standardized.append(working_row)

    return standardized

def standardize_madgrades_dir_3(rows: list):
    standardized = []

    for row in rows:
        working_row = row

        try:
            int(working_row[1])
        except:
            continue

        standardized.append(working_row)

    return standardized

import sqlite3


headers = ["name", "age_upon_outcome", "animal_type", "breed", "date_of_birth", "outcome_subtype", "outcome_type",
           "outcome_month", "outcome_year", "color1", "color2"]


def convert_response_to_dict(response):
    converted_dict = {}
    for pair in response:
        converted_dict[pair[0]] = pair[1]
    return converted_dict


def insert_data(data_type, col_name_1, col_name_2, col_name_3=""):
    print(f"insertion {data_type}")
    types = list(set(list(my_dict[data_type].values())))
    i = 1

    if col_name_3:
        col_name_3 = ", " + col_name_3
        val = "(?, ?, ?)"
    else:
        val = "(?, ?)"

    for prop in types:
        query_prop = f"""INSERT INTO {data_type} ({col_name_1}, {col_name_2}{col_name_3})
                                  VALUES {val}"""

        if col_name_3:
            pr_1 = prop[0]
            pr_2 = prop[1]
            prop = (i, pr_1, pr_2)
        else:
            prop = (i, prop)
        cur.execute(query_prop, prop)
        i += 1
    print(f"{data_type} inserted")


con = sqlite3.connect("animal.db")
print("connection with animal.db established")
cur = con.cursor()
query_animals_list = "CREATE TABLE IF NOT EXISTS animals_list (" \
        "animal_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
        "age_upon_outcome INT, " \
        "animal_type_id NVARCHAR(50), " \
        "name NVARCHAR(50) CONSTRAINT DF_name DEFAULT 'Noname', " \
        "breed_id NVARCHAR(50), " \
        "color_id INT, " \
        "color_1 NVARCHAR(20), " \
        "color_2 NVARCHAR(20), " \
        "date_of_birth DATE, " \
        "outcome_subtype NVARCHAR(200), " \
        "outcome_type_id NVARCHAR(50), " \
        "outcome_month INT, " \
        "outcome_year INT, " \
        "id NVARCHAR(20))"


query_animal_type = "CREATE TABLE IF NOT EXISTS animal_type (" \
                    "id INT, " \
                    "type NVARCHAR(100), " \
                    "FOREIGN KEY (id) REFERENCES animals_list (animal_type_id)" \
                    ")"

query_breed = "CREATE TABLE IF NOT EXISTS breed (" \
              "id INT," \
              "breed NVARCHAR(50), " \
              "FOREIGN KEY (id) REFERENCES animals_list(breed_id)" \
              ")"

query_color = "CREATE TABLE IF NOT EXISTS color (" \
              "id INT," \
              "color_1 NVARCHAR(20), " \
              "color_2 NVARCHAR(20), " \
              "FOREIGN KEY (id) REFERENCES animals_list (color_id)" \
              ")"

query_outcome = "CREATE TABLE IF NOT EXISTS outcome_type (" \
              "id INT, " \
              "outcome NVARCHAR(200), " \
              "FOREIGN KEY (id) REFERENCES animals_list(outcome_type_id)" \
              ")"


print("trying to create tables")
try:
    cur.execute(query_animals_list)
    print("Table animals_list created")
    cur.execute(query_animal_type)
    print("Table animals_type created")
    cur.execute(query_breed)
    print("Table breed created")
    cur.execute(query_color)
    print("Table color created")
    cur.execute(query_outcome)
    print("Table outcome created")

    my_dict = {}
    for header in headers:
        query = f"SELECT animal_id, {header} FROM animals"
        cur.execute(query)
        response = convert_response_to_dict(cur.fetchall())

        my_dict[header] = response

# working with colors
    query_colors = "SELECT animal_id, color1, color2 FROM animals"
    cur.execute(query_colors)
    animal_colors = {}
    for line in cur.fetchall():
        animal_colors[line[0]] = (line[1], line[2])

    my_dict["color"] = animal_colors

    print("starting insertion cycle")
    for key in my_dict["name"].keys():

        params = (my_dict['age_upon_outcome'][key],
                  my_dict['name'][key],
                  my_dict['animal_type'][key],
                  my_dict['breed'][key],
                  1,
                  my_dict['color1'][key],
                  my_dict['color2'][key],
                  '2020-01-01',
                  my_dict['outcome_subtype'][key],
                  my_dict['outcome_type'][key],
                  my_dict['outcome_month'][key],
                  my_dict['outcome_year'][key],
                  key)

        query = f"""INSERT INTO animals_list (age_upon_outcome, 
                name,
                animal_type_id,
                breed_id,
                color_id,
                color_1,
                color_2,
                date_of_birth,
                outcome_subtype,
                outcome_type_id,
                outcome_month,
                outcome_year,
                id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        cur.execute(query, params)
    print("insertion cycle finished")

    insert_data("animal_type", "id", "type")
    insert_data("breed", "id", "breed")
    insert_data("outcome_type", "id", "outcome")
    insert_data("color", "id", "color_1", "color_2")
    
    # connecting tables
    
    # matching breeds
    
    print("Trying to match breeds")
    query = "SELECT id, breed FROM breed"
    cur.execute(query)
    all_breeds = cur.fetchall()
    all_breeds = convert_response_to_dict(all_breeds)

    for breed_id, breed in all_breeds.items():
        query = f"UPDATE animals_list SET breed_id = {breed_id} WHERE breed_id = '{breed}'"
        cur.execute(query)
    con.commit()
    print("breeds are matched")
    
    # matching animal types
    
    print("Trying to match animal types")
    query = "SELECT id, type FROM animal_type"
    cur.execute(query)
    all_types = cur.fetchall()
    all_types = convert_response_to_dict(all_types)

    for type_id, animal_type in all_types.items():
        query = f"UPDATE animals_list SET animal_type_id = {type_id} WHERE animal_type_id = '{animal_type}'"
        cur.execute(query)
    con.commit()
    print("animal types are matched")
    
    # matching outcome type
    
    print("Trying to match outcome types")
    query = "SELECT id, outcome FROM outcome_type"
    cur.execute(query)
    all_outcomes = cur.fetchall()
    all_outcomes = convert_response_to_dict(all_outcomes)

    for outcome_id, outcome in all_outcomes.items():
        query = f"UPDATE animals_list SET outcome_type_id = {outcome_id} WHERE outcome_type_id = '{outcome}'"
        cur.execute(query)
    con.commit()
    print("outcome types are matched")
    
    # matching color
    
    print("Trying to match color")
    query = "SELECT id, color_1, color_2 FROM color"
    cur.execute(query)
    all_colors = cur.fetchall()
    animal_colors = {}
    for line in cur.fetchall():
        animal_colors[line[0]] = (line[1], line[2])

    for color_id, animal_color in animal_colors.items():
        query = f"UPDATE animals_list SET color_id = {color_id} WHERE color_1 = '{animal_color[0]}' AND color_2 = '{animal_color[1]}'"
        cur.execute(query)
    con.commit()
    print("colors are matched")

    # dropping color columns

    print("Dropping color columns")
    query_dr = "ALTER TABLE animals_list DROP COLUMN color_1"
    cur.execute(query_dr)
    query_dr = "ALTER TABLE animals_list DROP COLUMN color_2"
    cur.execute(query_dr)
    print("Color columns dropped")


except sqlite3.Error as err:
    print("execute error: ", err)
finally:
    print("committing tables...")
    con.commit()
    print("commited")
    con.close()
    print("connection with animal.db closed")
    con.close()
    print("connection closed")

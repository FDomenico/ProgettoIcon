import pandas as pd
from Utils import NEW_TRAFFIC_VIOLATIONS_PATH


def create_kb(path: str, name: str):
    print("Reading data...")
    violation = pd.read_csv(NEW_TRAFFIC_VIOLATIONS_PATH, low_memory=False)
    prolog_file = open(path + name, "w")
    print(f"Creating knowledge base at {path + name}...")
    prolog_file.write(":-style_check(-discontiguous).\n")

    # accident
    print("Writing violation facts...")
    for index, row in violation.iterrows():
        violation_code = f"violation(\"{row['UniqueCode']}\")"
        prolog_file.write(f"belts({violation_code}, \"{row['belts']}\").\n")
        prolog_file.write(f"personal_injury({violation_code}, \"{row['personal_injury']}\").\n")
        prolog_file.write(f"property_damage({violation_code}, \"{row['property_damage']}\").\n")
        prolog_file.write(f"commercial_license({violation_code}, \"{row['commercial_license']}\").\n")
        prolog_file.write(f"commercial_vehicle({violation_code}, \"{row['commercial_vehicle']}\").\n")
        prolog_file.write(f"year({violation_code}, {row['year']}).\n")
        prolog_file.write(f"make({violation_code}, \"{row['make']}\").\n")
        prolog_file.write(f"model({violation_code},\"{row['model']}\").\n")
        prolog_file.write(f"color({violation_code}, \"{row['color']}\").\n")
        prolog_file.write(f"charge({violation_code}, \"{row['charge']}\").\n")
        prolog_file.write(f"gender({violation_code}, \"{row['gender']}\").\n")
        prolog_file.write(f"driver_state({violation_code}, \"{row['driver_state']}\").\n")
        prolog_file.write(f"dL_state({violation_code},\"{row['dL_state']}\").\n")
        prolog_file.write(f"arrest_type({violation_code}, \"{row['arrest_type']}\").\n")
        prolog_file.write(f"violation_type({violation_code}, \"{row['violation_type']}\").\n")
    prolog_file.close()
    print("Knowledge base created!")


create_kb("../dataset/", "kb.pl")

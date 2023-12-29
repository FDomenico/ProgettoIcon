from datetime import datetime

import pandas as pd
from pyswip import Prolog
from Utils import NEW_TRAFFIC_VIOLATIONS_PATH


def define_clause(kb_path: str, kb_name: str) -> Prolog:
    prolog = Prolog()

    prolog.consult(f"{kb_path}{kb_name}")
    current_year = datetime.now().year  # Ottieni l'anno corrente
    prolog.assertz(f"current_year({current_year})")
    prolog.assertz("same_state(violation(V1), violation(V2)) :- dl_state(violation(V1), DLS), dl_state(violation(V2), DLS)")
    prolog.assertz("same_models(violation(V1), violation(V2)) :- model(violation(V1), MOD), model(violation(V2), MOD)")
    prolog.assertz("same_make(violation(V1), violation(V2)) :- make(violation(V1), MAKE), make(violation(V2), MAKE)")
    prolog.assertz("same_color(violation(V1), violation(V2)) :- color(violation(V1), COL), color(violation(V2), COL)")
    prolog.assertz("same_year(violation(V1), violation(V2)) :- year(violation(V1), Y), years(violation(V2), Y)")
    prolog.assertz("same_vehicle(violation(V1), violation(V2)) :- vehicle_type(violation(V1), VT), vehicle_type(violation(V2), VT)")
    prolog.assertz("same_arrest(violation(V1), violation(V2)) :- arrest_type(violation(V1), AT), arrest_type(violation(V2), AT)")
    prolog.assertz("same_charge(violation(V1), violation(V2)) :- charge(violation(V1), CH), charge(violation(V2), CH)")
    prolog.assertz("same_driver_state(violation(V1), violation(V2)) :- driver_state(violation(V1), DS), driver_state(violation(V2), DS)")

    prolog.assertz("is_belts(violation(V)) :- belts(violation(V1), B), (B = \"Yes\")")
    prolog.assertz("is_commercial_licence(violation(V)) :- commercial_licence(violation(V), CL), (CL = \"Yes\")")
    prolog.assertz("is_commercial_vehicle(violation(V)) :- commercial_vehicle(violation(V), CV), (CV = \"Yes\")")
    prolog.assertz("is_contributed_to_accident(violation(V)) :- contributed_to_accident(violation(V), CTA), (CTA = \"Yes\")")
    prolog.assertz("is_property_damaged(violation(V)) :- property_damage(violation(V), PD), (PD = \"Yes\")")
    prolog.assertz("is_personal_injured(violation(V)) :- personal_injury(violation(V), PI), (PI = \"Yes\")")

    prolog.assertz(f"vehicle_age(violation(V), Age) :- year(violation(V), Year), current_year(CurrentYear), Age is CurrentYear - Year")

    prolog.assertz("is_automobile(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"02 - Automobile\")")
    prolog.assertz("is_l_truck(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"05 - Light Duty Truck\")")
    prolog.assertz("is_other(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"28 - Other\")")
    prolog.assertz("is_motorcycle(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"01 - Motorcycle\")")
    prolog.assertz("is_r_vehicle(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"08 - Recreational Vehicle\")")
    prolog.assertz("is_h_truck(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"06 - Heavy Duty Truck\")")
    prolog.assertz("is_s_wagon(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"03 - Station Wagon\")")
    prolog.assertz("is_moped(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"19 - Moped\")")
    prolog.assertz("is_tractor(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"07 - Truck/Road Tractor\")")
    prolog.assertz("is_u_trailer(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"25 - Utility Trailer\")")
    prolog.assertz("is_t_bus(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"10 - Transit Bus\")")
    prolog.assertz("is_c_rig(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"20 - Commercial Rig\")")
    prolog.assertz("is_s_bus(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"12 - School Bus\")")
    prolog.assertz("is_limousine(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"04 - Limousine\")")
    prolog.assertz("is_farm_e(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"27 - Farm Equipment\")")
    prolog.assertz("is_unknown(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"29 - Unknown\")")
    prolog.assertz("is_ambulance(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"14 - Ambulance(Non-Emerg)\")")
    prolog.assertz("is_f_vehicle(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"09 - Farm Vehicle\")")
    prolog.assertz("is_b_trailer(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"26 - Boat Trailer\")")
    prolog.assertz("is_t_trailer(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"21 - Tandem Trailer\")")
    prolog.assertz("is_cc_bus(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"11 - Cross Country Bus\")")
    prolog.assertz("is_camper(violation(V)) :- vehicle_type(violation(V), VT), (VT = \"24 - Camper\")")

    prolog.assertz("is_citation(violation(V)) :- violation_type(violation(V), VT), (VT = \"Citation\")")
    prolog.assertz("is_sero(violation(V)) :- violation_type(violation(V), VT), (VT = \"SERO\")")
    prolog.assertz("is_warning(violation(V)) :- violation_type(violation(V), VT), (VT = \"Warning\")")

    prolog.assertz("vehicle_category(violation(V), 1) :- is_automobile(violation(V)); is_s_wagon(violation(V)); is_limousine(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 2) :- is_l_truck(violation(V)); is_h_truck(violation(V)); is_c_rig(violation(V)); is_tractor(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 3) :- is_r_vehicle(violation(V)); is_farm_e(violation(V)); is_camper(violation(V)); is_f_vehicle(violation(V)); is_ambulance(violation(V)); is_other(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 4) :- is_motorcycle(violation(V)); is_moped(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 5) :- is_t_bus(violation(V)); is_s_bus(violation(V)); is_cc_bus(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 6) :- is_unknown(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 7) :- is_b_trailer(violation(V)); is_t_trailer(violation(V)); is_u_trailer(violation(V))")
    prolog.assertz("violation_type(violation(V), 1) :- is_citation(violation(V))")
    prolog.assertz("violation_type(violation(V), 2) :- is_sero(violation(V))")
    prolog.assertz("violation_type(violation(V), 3) :- is_warning(violation(V))")
    
    return prolog


def query_to_dict_list(prolog: Prolog):
    violation = pd.read_csv(NEW_TRAFFIC_VIOLATIONS_PATH, low_memory=False)
    dict_list = []
    for v in violation['UniqueCode']:
        print(violation[violation['UniqueCode'] == v].index[0], "/", len(violation))
        try:
            features_dict = {}
            v = f"\"{v}\""
            features_dict["UniqueCode"] = v
            citation = list(prolog.query(f"violation_type(violation({v}), Citation)"))
            sero = list(prolog.query(f"violation_type(violation({v}), SERO)"))
            warning = list(prolog.query(f"violation_type(violation({v}), Warning)"))
            if len(citation):
                features_dict["violation_type"] = citation[0]["Citation"]
            elif len(sero):
                features_dict["violation_type"] = sero[0]["SERO"]
            elif len(warning):
                features_dict["violation_type"] = warning[0]["Warning"]
            else:
                features_dict["violation_type"] = "N/A"

            #features_dict["violation_type"] = list(prolog.query(f"violation_type(violation({v}), VT)"))[0]["VT"]
            features_dict["vehicle_age"] = list(prolog.query(f"vehicle_age(violation({v}),Age)"))[0]["Age"]
            features_dict["belts"] = int(bool(list(prolog.query(f"is_belts(violation({v}))"))))
            features_dict["personal_injured"] = int(bool(list(prolog.query(f"is_personal_injured(violation({v}))"))))
            features_dict["contributed_to_accident"] = int(bool(list(prolog.query(f"is_contributed_to_accident(violation({v}))"))))
            features_dict["property_damaged"] = int(bool(list(prolog.query(f"is_property_damaged(violation({v}))"))))
            car = list(prolog.query(f"vehicle_category(violation({v}), Car)"))
            truck = list(prolog.query(f"vehicle_category(violation({v}), Truck)"))
            other = list(prolog.query(f"vehicle_category(violation({v}), Other)"))
            unknown = list(prolog.query(f"vehicle_category(violation({v}), Unknown)"))
            bus = list(prolog.query(f"vehicle_category(violation({v}), Bus)"))
            trailer = list(prolog.query(f"vehicle_category(violation({v}), Trailer)"))
            motorcycle = list(prolog.query(f"vehicle_category(violation({v}), Motorcycle)"))

            if len(car):
                features_dict["vehicle_category"] = car[0]["Car"]
            elif len(truck):
                features_dict["vehicle_category"] = truck[0]["Truck"]
            elif len(other):
                features_dict["vehicle_category"] = other[0]["Other"]
            elif len(unknown):
                features_dict["vehicle_category"] = unknown[0]["Unknown"]
            elif len(bus):
                features_dict["vehicle_category"] = bus[0]["Bus"]
            elif len(trailer):
                features_dict["vehicle_category"] = trailer[0]["Trailer"]
            elif len(motorcycle):
                features_dict["vehicle_category"] = motorcycle[0]["Motorcycle"]
            else:
                features_dict["vehicle_category"] = "N/A"

            """features_dict["automobile"] = int(bool(list(prolog.query(f"is_automobile(violation({v}))"))))
            features_dict["light_truck"] = int(bool(list(prolog.query(f"is_l_truck(violation({v}))"))))
            features_dict["violation_type"] = list(prolog.query(f"violation_type(violation({v}), VT)"))[0]["VT"]
            features_dict["automobile"] = int(bool(list(prolog.query(f"is_automobile(violation({v}))"))))
            features_dict["light_truck"] = int(bool(list(prolog.query(f"is_l_truck(violation({v}))"))))
            features_dict["other"] = int(bool(list(prolog.query(f"is_other(violation({v}))"))))
            features_dict["motorcycle"] = int(bool(list(prolog.query(f"is_motorcycle(violation({v}))"))))
            features_dict["r_vehicle"] = int(bool(list(prolog.query(f"is_r_vehicle(violation({v}))"))))
            features_dict["station_wagon"] = int(bool(list(prolog.query(f"is_s_wagon(violation({v}))"))))
            features_dict["heavy_truck"] = int(bool(list(prolog.query(f"is_h_truck(violation({v}))"))))
            features_dict["moped"] = int(bool(list(prolog.query(f"is_moped(violation({v}))"))))
            features_dict["tractor"] = int(bool(list(prolog.query(f"is_tractor(violation({v}))"))))
            features_dict["utility_trailer"] = int(bool(list(prolog.query(f"is_u_trailer(violation({v}))"))))
            features_dict["transit_bus"] = int(bool(list(prolog.query(f"is_t_bus(violation({v}))"))))
            features_dict["commercial_rig"] = int(bool(list(prolog.query(f"is_c_rig(violation({v}))"))))
            features_dict["school_bus"] = int(bool(list(prolog.query(f"is_s_bus(violation({v}))"))))
            features_dict["limousine"] = int(bool(list(prolog.query(f"is_limousine(violation({v}))"))))
            features_dict["farm_e"] = int(bool(list(prolog.query(f"is_farm_e(violation({v}))"))))
            features_dict["unknown"] = int(bool(list(prolog.query(f"is_unknown(violation({v}))"))))
            features_dict["farm_v"] = int(bool(list(prolog.query(f"is_f_vehicle(violation({v}))"))))
            features_dict["boat_trailer"] = int(bool(list(prolog.query(f"is_b_trailer(violation({v}))"))))
            features_dict["cc_bus"] = int(bool(list(prolog.query(f"is_cc_bus(violation({v}))"))))
            features_dict["ambulance"] = int(bool(list(prolog.query(f"is_ambulance(violation({v}))"))))
            features_dict["t_trailer"] = int(bool(list(prolog.query(f"is_t_trailer(violation({v}))"))))
            features_dict["camper"] = int(bool(list(prolog.query(f"is_camper(violation({v}))"))))"""

            dict_list.append(features_dict)
        except ValueError as e:
            print("exception", violation[violation['UniqueCode'] == v].index[0])
    return dict_list


print("Defining clauses...")
p = define_clause("../dataset/", "kb.pl")
print("Querying...")
new_dataset = pd.DataFrame(query_to_dict_list(p))
new_dataset.to_csv("../dataset/new_dataset.csv", index=False)
print("Done!")


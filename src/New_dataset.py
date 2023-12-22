import pandas as pd
from pyswip import Prolog
from Utils import NEW_TRAFFIC_VIOLATIONS_PATH


def define_clause(kb_path: str, kb_name: str) -> Prolog:
    prolog = Prolog()
    prolog.consult(f"{kb_path}{kb_name}")
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
            features_dict["violation_type"] = list(prolog.query(f"violation_type(violation({v}), VT)"))[0]["VT"]
            features_dict["automobile"] = int(bool(list(prolog.query(f"is_automobile(violation({v}))"))))
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
            features_dict["camper"] = int(bool(list(prolog.query(f"is_camper(violation({v}))"))))

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

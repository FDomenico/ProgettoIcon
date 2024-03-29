from datetime import datetime

import pandas as pd
from pyswip import Prolog
from Utils import NEW_TRAFFIC_VIOLATIONS_PATH


def define_clause(kb_path: str, kb_name: str) -> Prolog:
    prolog = Prolog()

    prolog.consult(f"{kb_path}{kb_name}")
    current_year = datetime.now().year  # Ottieni l'anno corrente
    prolog.assertz(f"current_year({current_year})")
    prolog.assertz("is_belts(violation(V)) :- belts(violation(V1), B), (B = \"Yes\")")
    prolog.assertz("is_commercial_licence(violation(V)) :- commercial_licence(violation(V), CL), (CL = \"Yes\")")
    prolog.assertz("is_commercial_vehicle(violation(V)) :- commercial_vehicle(violation(V), CV), (CV = \"Yes\")")
    prolog.assertz("is_contributed_to_accident(violation(V)) :- contributed_to_accident(violation(V), CTA), (CTA = \"Yes\")")
    prolog.assertz("is_property_damaged(violation(V)) :- property_damage(violation(V), PD), (PD = \"Yes\")")
    prolog.assertz("is_personal_injured(violation(V)) :- personal_injury(violation(V), PI), (PI = \"Yes\")")

    prolog.assertz(f"vehicle_age(violation(V), Age) :- year(violation(V), Year), current_year(CurrentYear), Age is CurrentYear - Year")

    # arrest_type
    prolog.assertz("is_m_patrol(violation(V)) :- arrest_type(violation(V), AT), (AT = \"A - Marked Patrol\")")
    prolog.assertz("is_u_patrol(violation(V)) :- arrest_type(violation(V), AT), (AT = \"B - Unmarked Patrol\")")
    prolog.assertz("is_l_p_recognition(violation(V)) :- arrest_type(violation(V), AT), (AT = \"S - License Plate Recognition\")")
    prolog.assertz("is_m_laser(violation(V)) :- arrest_type(violation(V), AT), (AT = \"Q - Marked Laser\")")
    prolog.assertz("is_motorcycle(violation(V)) :- arrest_type(violation(V), AT), (AT = \"L - Motorcycle\")")
    prolog.assertz("is_f_patrol(violation(V)) :- arrest_type(violation(V), AT), (AT = \"O - Foot Patrol\")")
    prolog.assertz("is_u_laser(violation(V)) :- arrest_type(violation(V), AT), (AT = \"R - Unmarked Laser\")")
    prolog.assertz("is_marked(violation(V)) :- arrest_type(violation(V), AT), (AT = \"M - Marked (Off-Duty)\")")
    prolog.assertz("is_m_s_radar(violation(V)) :- arrest_type(violation(V), AT), (AT = \"E - Marked Stationary Radar\")")
    prolog.assertz("is_m_m_radar_s(violation(V)) :- arrest_type(violation(V), AT), (AT = \"G - Marked Moving Radar (Stationary)\")")
    prolog.assertz("is_m_m_radar_m(violation(V)) :- arrest_type(violation(V), AT), (AT = \"I - Marked Moving Radar (Moving)\")")
    prolog.assertz("is_u_m_radar_s(violation(V)) :- arrest_type(violation(V), AT), (AT = \"H - Unmarked Moving Radar (Stationary)\")")
    prolog.assertz("is_monted_patrol(violation(V)) :- arrest_type(violation(V), AT), (AT = \"P - Mounted Patrol\")")
    prolog.assertz("is_unmarked(violation(V)) :- arrest_type(violation(V), AT), (AT = \"N - Unmarked (Off-Duty)\")")
    prolog.assertz("is_u_vascar(violation(V)) :- arrest_type(violation(V), AT), (AT = \"D - Unmarked VASCAR\")")
    prolog.assertz("is_u_m_radar_m(violation(V)) :- arrest_type(violation(V), AT), (AT = \"J - Unmarked Moving Radar (Moving)\")")
    prolog.assertz("is_u_s_radar(violation(V)) :- arrest_type(violation(V), AT), (AT = \"F - Unmarked Stationary Radar\")")
    prolog.assertz("is_m_vascar(violation(V)) :- arrest_type(violation(V), AT), (AT = \"C - Marked VASCAR\")")
    prolog.assertz("is_a_aircraft(violation(V)) :- arrest_type(violation(V), AT), (AT = \"K - Aircraft Assist\")")

    prolog.assertz("arrest_category(violation(V), 1) :- is_m_patrol(violation(V)); is_u_patrol(violation(V)); is_f_patrol(violation(V)); is_monted_patrol(violation(V))")
    prolog.assertz("arrest_category(violation(V), 2) :- is_l_p_recognition(violation(V)); is_u_laser(violation(V)); is_m_laser(violation(V)); is_m_s_radar(violation(V)); is_m_m_radar_s(violation(V)); is_m_m_radar_m(violation(V)); is_u_m_radar_s(violation(V)); is_u_m_radar_m(violation(V)); is_u_s_radar(violation(V)); is_m_vascar(violation(V)); is_u_vascar(violation(V))")
    prolog.assertz("arrest_category(violation(V), 3) :- is_motorcycle(violation(V)); is_a_aircraft(violation(V)); is_unmarked(violation(V)); is_marked(violation(V))")

    # vehicle_type
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

    prolog.assertz("vehicle_category(violation(V), 1) :- is_automobile(violation(V)); is_s_wagon(violation(V)); is_limousine(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 2) :- is_l_truck(violation(V)); is_h_truck(violation(V)); is_c_rig(violation(V)); is_tractor(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 3) :- is_r_vehicle(violation(V)); is_farm_e(violation(V)); is_camper(violation(V)); is_f_vehicle(violation(V)); is_ambulance(violation(V)); is_other(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 4) :- is_motorcycle(violation(V)); is_moped(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 5) :- is_t_bus(violation(V)); is_s_bus(violation(V)); is_cc_bus(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 6) :- is_unknown(violation(V))")
    prolog.assertz("vehicle_category(violation(V), 7) :- is_b_trailer(violation(V)); is_t_trailer(violation(V)); is_u_trailer(violation(V))")

    return prolog


def query_to_dict_list(prolog: Prolog):
    violation = pd.read_csv(NEW_TRAFFIC_VIOLATIONS_PATH, low_memory=False)
    dict_list = []
    for v in violation['unique_code']:
        print(violation[violation['unique_code'] == v].index[0], "/", len(violation))
        try:
            features_dict = {}
            v = f"\"{v}\""
            features_dict["unique_code"] = v
            features_dict["violation_type"] = list(prolog.query(f"violation_type(violation({v}), VT)"))[0]["VT"]
            features_dict["category"] = list(prolog.query(f"category(violation({v}), VT)"))[0]["VT"]
            features_dict["vehicle_age"] = list(prolog.query(f"vehicle_age(violation({v}),Age)"))[0]["Age"]
            features_dict["belts"] = int(bool(list(prolog.query(f"is_belts(violation({v}))"))))
            features_dict["personal_injured"] = int(bool(list(prolog.query(f"is_personal_injured(violation({v}))"))))
            features_dict["contributed_to_accident"] = int(bool(list(prolog.query(f"is_contributed_to_accident(violation({v}))"))))
            features_dict["property_damaged"] = int(bool(list(prolog.query(f"is_property_damaged(violation({v}))"))))

            # vehicle_type
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

            # arrest_type
            traffic = list(prolog.query(f"arrest_category(violation({v}), Traffic)"))
            survey = list(prolog.query(f"arrest_category(violation({v}), Survey)"))
            other1 = list(prolog.query(f"arrest_category(violation({v}), Other1)"))

            if len(traffic):
                features_dict["arrest_category"] = traffic[0]["Traffic"]
            elif len(survey):
                features_dict["arrest_category"] = survey[0]["Survey"]
            elif len(other1):
                features_dict["arrest_category"] = other1[0]["Other1"]
            else:
                features_dict["arrest_category"] = "N/A"

            dict_list.append(features_dict)
        except ValueError as e:
            print("exception", violation[violation['unique_code'] == v].index[0])
    return dict_list


print("Defining clauses...")
p = define_clause("../dataset/", "kb.pl")
print("Querying...")
new_dataset = pd.DataFrame(query_to_dict_list(p))
new_dataset.to_csv("../dataset/new_dataset.csv", index=False)
print("Done!")


from Utils import *
from sklearn.preprocessing import LabelEncoder


def preprocessing():
    print("Reading data...")
    violation = pd.read_csv('../dataset/traffic_violations.csv')
    print("Preprocessing...")

    violation = add_unique_code(violation)
    le = LabelEncoder()
    violation['violation_type'] = le.fit_transform(violation['violation_type'])
    drop_column_traffic = ['description', 'race', 'state', 'driver_city']
    violation.drop(drop_column_traffic, axis=1, inplace=True)
    column_check_na_traffic = ['belts', 'personal_injury', 'property_damage',
                               'commercial_license', 'commercial_vehicle', 'vehicle_type',
                               'year', 'make', 'model', 'color', 'charge', 'contributed_to_accident',
                               'gender', 'driver_state', 'dL_state', 'arrest_type', 'violation_type']
    violation.dropna(subset=column_check_na_traffic, inplace=True)

    # Rimuovi il ".0" da ogni elemento nella colonna 'NumeroConDecimale'
    violation['year'] = violation['year'].apply(lambda x: int(x) if x.is_integer() else x)

    print("Preprocessing done!")

    plot_violation_type(violation, save=True, show=True)

    print("Balancing data...")
    min_samples = violation['violation_type'].value_counts().min()
    balanced_violation_type = pd.DataFrame()
    for violation_type in violation['violation_type'].unique():
        sampled_data = violation[violation['violation_type'] == violation_type].sample(n=min_samples, random_state=42)
        balanced_violation_type = balanced_violation_type._append(sampled_data)

    print("Balancing done!")
    stats(violation, save=True, display=False)

    plot_violation_type(balanced_violation_type)

    return balanced_violation_type


t = preprocessing()
print("Saving preprocessed data...")
t.to_csv(NEW_TRAFFIC_VIOLATIONS_PATH, index=False)
print("Preprocessed data saved!")

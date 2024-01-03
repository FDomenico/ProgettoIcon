import pandas as pd

# Carica il dataset con le violazioni
df = pd.read_csv("../dataset/traffic_violation_keyword.csv")

# Definisci le categorie
categorie = {
    'registration problems': ['suspended registration', 'operating unregistered motor vehicle highway'],
    'tag problem': ['failure attach veh reg plates front rear','failure attach vehicle registration plates front rear', 'without current registration plates validation tabs', 'displaying expired registration plate issued state', 'displaying reg plate issued vehicle', 'displaying reg plate issued vehicle person', 'displaying registration plate issued vehicle'],
    'stop lights': ['stop lights', 'stop red traffic signal', 'stop steady circular red signal', 'stop steady red arrow signal'],
    'failure device instructions': ['traffic control device instructions'],
    'color window': ['window tint'],
    'exceeding speed': ['driving veh excess reasonable prudent speed hwy', 'driving vehicle excess reasonable prudent speed highway', 'exceeding maximum', 'exceeding posted', 'exceeding highway work zone speed limit'],
    'failure registration card': ['failure display registration card upon demand police officer'],
    'problem vehicle lamp': ['lighted lamps illuminating device', 'tag light', 'veh failure display reflect amber color light lamps reflectors req', 'trailer wo required stop lamps equipment', 'motor veh wo required stop lamps equipment', 'failure display two lighted front lamps required', 'failure display reflect red color light rear lamps reflectors req', 'clearance lamps', 'fog auxilary lamps', 'parking lamps', 'failure equip hwy veh required lamps reflectors'],
    'careless driving': ['failure dr make lane change avail lane immed adj stopped emerg veh', 'driver motor vehicle following vehicle closer reasonable prudent', 'driver changing lanes prohibited traffic control device', 'driver changing lanes unsafe', 'unsafe lane changing', 'failure drive vehicle right half roadway required', 'negligent driving vehicle careless imprudent manner', 'driver using hands use handheld telephone whilemotor vehicle motion'],
    'administration problem': ['notify adm address', 'failure display tab plates veh required adm', 'notify administration'],
    'driving alcohol': ['alcohol'],
    'license problem': ['failure individual driving highway display license uniformed police demand', 'revoked outofstate license', 'person driving motor vehicle license suspended', 'without required license authorization', 'revoked license privilege', 'suspended license privilege', 'expired license'],
    'sign violation': ['stop sign', 'stop sign line', 'flashing red traffic signal without stopping'],
    'belts': ['operator restrained seatbelt', 'operator restrained seat belt', 'occupant 16 restrained seatbelt'],
    'other': ['failure control vehicle speed highway avoid collision', 'failure control veh speed hwy avoid collision'],
    'problem vehicle lp': ['motor veh wo required stop lamps equipment', 'failure display two lighted front lamps required'],
    # Aggiungi altre categorie in base alle tue esigenze
}

# Aggiungi una colonna 'categoria' al DataFrame
df['categoria'] = None

# Assegna ogni violazione a una categoria
for categoria, parole_chiave in categorie.items():
    for parola_chiave in parole_chiave:
        df.loc[df['parole_chiave'].str.contains(parola_chiave, case=False), 'categoria'] = categoria

# Visualizza il DataFrame con le categorie assegnate
print(df[['parole_chiave', 'categoria']])

# Salva il risultato in un nuovo file CSV
df.to_csv("dataset_categorizzato.csv", index=False)

import pandas as pd
import matplotlib.pyplot as plt
import uuid
from sklearn.metrics import ConfusionMatrixDisplay


NEW_TRAFFIC_VIOLATIONS_PATH = '../dataset/traffic_violations_preprocessing.csv'
PLOT_PATH = "../plots/"


def add_unique_code(df):
    # Aggiungi una nuova colonna chiamata 'UniqueCode' con un codice univoco per ogni riga
    df['UniqueCode'] = [f'Code_{i + 1}' for i in range(len(df))]

    # Riorganizza le colonne per mettere 'UniqueCode' all'inizio
    columns = ['UniqueCode'] + [col for col in df.columns if col != 'UniqueCode']
    df = df[columns]

    return df


def plot_violation_type(violation: pd.DataFrame, save=True, show=False):
    plt.pie(violation['violation_type'].value_counts(), labels=['Warning', 'Sero', 'Citation'], autopct='%1.1f%%')
    plt.title("violation_type")
    if show:
        plt.show()
    if save:
        plt.savefig("../plot/violation_type.png")
    plt.close()


def code_label_dict(field_name: str, inverse=False) -> dict:
    df_guide = pd.read_excel('../Dataset/Road-Safety-Open-Dataset-Data-Guide.xlsx')
    d = {}
    for index, row in df_guide[df_guide['field name'] == field_name][['code/format', 'label']].iterrows():
        k = row['code/format']
        v = row['label']
        if inverse:
            d[v] = k
        d[k] = v
    return d


def change_code_to_description_df(df: pd.DataFrame, inverse=False):
    for col in df.columns:
        df[col] = df[col].replace(code_label_dict(col, inverse))


def stats(violation: pd.DataFrame, save=True, display=True):
    stat_g = violation[['gender']].describe()
    stat_m = violation[['model']].describe()
    stat_make = violation[['make']].describe()
    stat_c = violation[['charge']].describe()
    stat_vt = violation['vehicle_type'].unique()
    df_stat_vt = pd.DataFrame(stat_vt)
    stat_at = violation['arrest_type'].unique()
    df_stat_at = pd.DataFrame(stat_at)
    if display:
        print(stat_g)
        print(stat_m)
        print(stat_make)
        print(stat_c)
        print(stat_vt)
        print(stat_at)
    if save:
        stat_g.to_csv("../Dataset/gender_stat.csv")
        stat_m.to_csv("../Dataset/model_stat.csv")
        stat_make.to_csv("../Dataset/make_stat.csv")
        stat_c.to_csv("../Dataset/charge_stat.csv")
        df_stat_vt.to_csv("../Dataset/vehicle_type_stat.csv")
        df_stat_at.to_csv("../Dataset/arrest_type_stat.csv")


def cross_val_score_plot(score, name, save: True, display: False):
    plt.plot(range(1, 11), score)
    plt.title(f"{name} Cross Validation Score")
    plt.xlabel("k")
    plt.ylabel("score")
    if display:
        plt.show()
    if save:
        plt.savefig(PLOT_PATH + name + "_cross_val_score.png")
    plt.close()


def confusion_matrix_plot(confusion_matrix, labels, name, save: True, display: False):
    cm = ConfusionMatrixDisplay(confusion_matrix, display_labels=labels)
    cm.plot()
    if display:
        plt.show()
    if save:
        plt.savefig(PLOT_PATH + name + "_confusion_matrix.png")
    plt.close()


#data = pd.read_csv('../dataset/traffic_violations.csv')
#plot_violation_type(data)

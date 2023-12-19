import pandas as pd
import matplotlib.pyplot as plt


NEW_TRAFFIC_VIOLATIONS_PATH = '../dataset/traffic_violations_prepocessing.csv'
PLOT_PATH = "../plots/"


def plot_violation_type(violation: pd.DataFrame, save=True, show=False):
    plt.pie(violation['violation_type'].value_counts(), labels=['Warning', 'Sero', 'Citation'], autopct='%1.1f%%')
    plt.title("violation_type")
    if show:
        plt.show()
    if save:
        plt.savefig("../plot/violation_type.png")
    plt.close()


def stats(violation: pd.DataFrame, save=True, display=True):
    stat_g = violation[['gender']].describe()
    stat_m = violation[['model']].describe()
    stat_make = violation[['make']].describe()
    stat_c = violation[['charge']].describe()
    if display:
        print(stat_g)
        print(stat_m)
        print(stat_make)
        print(stat_c)
    if save:
        stat_g.to_csv("../Dataset/gender_stat.csv")
        stat_m.to_csv("../Dataset/model_stat.csv")
        stat_make.to_csv("../Dataset/make_stat.csv")
        stat_c.to_csv("../Dataset/charge_stat.csv")



#data = pd.read_csv('../dataset/traffic_violations.csv')
#plot_violation_type(data)



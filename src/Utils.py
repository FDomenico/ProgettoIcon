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


data = pd.read_csv('../dataset/traffic_violations.csv')
plot_violation_type(data)



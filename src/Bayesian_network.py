
import pandas as pd
import itertools
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference.ExactInference import VariableElimination
from string import ascii_uppercase
from pandas import DataFrame
import numpy as np
import tqdm
import matplotlib.pyplot as plt
import networkx as nx

# Gathering data
nodes = [
    "arrest_category",
    "category",
    "vehicle_age",
    "belts",
    "personal_injured",
    "contributed_to_accident",
    "property_damaged",
    "vehicle_category",
    "violation_type",
]
df = pd.read_csv("../dataset/new_dataset.csv", usecols=nodes)

# apply discretization
N_BINS = 3


def equal_width(values, n_bins):
    min_val = min(values)
    max_val = max(values)
    interval_width = (max_val - min_val) / n_bins
    intervals = [min_val + interval_width * i for i in range(n_bins + 1)]
    return intervals


def count_per_interval(values, intervals):
    n_bins = len(intervals) - 1
    count_arr = [0 for _ in range(n_bins)]
    for j, val in enumerate(values):
        for i in range(n_bins):
            if intervals[i] <= val <= intervals[i + 1]:
                count_arr[i] += 1
                break
        else:
            print(j, val)
    return count_arr


def get_index_of_count(val: float, intervals: list) -> int:
    for i in range(len(intervals) - 1):
        if intervals[i] <= val <= intervals[i + 1]:
            return ascii_uppercase[i]


def create_dataframe(nodes: list, df: DataFrame, n_bins: int) -> dict:
    dataframe = {}
    for col in nodes[:-1]:
        values = df[col]
        intervals = equal_width(values, n_bins)
        dataframe[col] = [get_index_of_count(value, intervals) for value in values]
    return dataframe


def val_counter(cols: str, data: DataFrame) -> dict:
    val_count = {ascii_uppercase[i]: 0 for i in range(0, N_BINS)}
    for val in data[cols]:
        val_count[val] += 1
    return val_count


def multi_val_counter(cols: list, indexMatrix: str, data: DataFrame) -> int:
    val_count = 0
    for v in data.iloc:
        for i, c in enumerate(cols):
            if v[c] != indexMatrix[i]:
                break
        else:
            val_count += 1
    return val_count


def generate_tuples(cols: list, indexLen: int):
    tup = [chr(ord("A") + c) for c in range(indexLen)]
    return [p for p in itertools.product(tup, repeat=len(cols))]


def calc_matrix_with_cols(cols: list, indexes: str):
    matrix = [[] for _ in range(len(indexes))]
    t = generate_tuples(cols, len(indexes))
    for i, index in enumerate(indexes):
        part = [p for p in t if p[0] == index]
        for p in part:
            matrix[i].append(multi_val_counter(cols, "".join(p), data))
    matrix_sum = []
    N_ROWS = len(matrix)
    for i in range(len(matrix[0])):
        sum_col = 0
        for j in range(N_ROWS):
            sum_col += matrix[j][i]
        matrix_sum.append(sum_col)
    for i, s in enumerate(matrix_sum):
        if s == 0:
            perc_temp = 1 / N_ROWS
            for j in range(len(matrix)):
                matrix[j][i] = perc_temp
        else:
            for j in range(len(matrix)):
                matrix[j][i] /= s
    return matrix


new_column = create_dataframe(nodes, df, N_BINS)
data = DataFrame(data=new_column)
violation_type = {
    1: "A",
    2: "B",
    3: "C"
}
data["violation_type"] = [violation_type[r] for r in df["violation_type"]]

# Setting the model
# set the structure
model = BayesianNetwork(
    [
        ("category", "violation_type"),
        ("contributed_to_accident", "violation_type"),
        ("arrest_category", "violation_type"),
        ("vehicle_category", "violation_type"),
        ("vehicle_age", "violation_type"),
        ('belts', 'violation_type'),
        ("personal_injured", "contributed_to_accident"),
        ("property_damaged", "contributed_to_accident"),
    ]
)

total = len(df['violation_type'])
features_count = {node: val_counter(node, data) for node in nodes[:-1]}


print('TabularCPD category')
category_cpd = TabularCPD(
    variable="category",
    variable_card=N_BINS,
    values=[
        [features_count['category']['A'] / total],
        [features_count['category']['B'] / total],
        [features_count['category']['C'] / total]
    ],
)
print('TabularCPD arrest_category')
arrest_category_cpd = TabularCPD(
    variable="arrest_category",
    variable_card=N_BINS,
    values=[
        [features_count['arrest_category']['A'] / total],
        [features_count['arrest_category']['B'] / total],
        [features_count['arrest_category']['C'] / total]
    ],
)
print('TabularCPD vehicle_category')
vehicle_category_cpd = TabularCPD(
    variable="vehicle_category",
    variable_card=N_BINS,
    values=[
        [features_count['vehicle_category']['A'] / total],
        [features_count['vehicle_category']['B'] / total],
        [features_count['vehicle_category']['C'] / total]
    ],
)

print('TabularCPD vehicle_age')
vehicle_age_cpd = TabularCPD(
    variable="vehicle_age",
    variable_card=N_BINS,
    values=[
        [features_count['vehicle_age']['A'] / total],
        [features_count['vehicle_age']['B'] / total],
        [features_count['vehicle_age']['C'] / total]
    ],
)

print('TabularCPD belts')
belts_cpd = TabularCPD(
    variable="belts",
    variable_card=N_BINS,
    values=[
        [features_count['belts']['A'] / total],
        [features_count['belts']['B'] / total],
        [features_count['belts']['C'] / total]
    ],
)

print('TabularCPD personal_injured')
personal_injured_cpd = TabularCPD(
    variable="personal_injured",
    variable_card=N_BINS,
    values=[
        [features_count['personal_injured']['A'] / total],
        [features_count['personal_injured']['B'] / total],
        [features_count['personal_injured']['C'] / total]
    ],
)

print('TabularCPD property_damaged')
property_damaged_cpd = TabularCPD(
    variable="property_damaged",
    variable_card=N_BINS,
    values=[
        [features_count['property_damaged']['A'] / total],
        [features_count['property_damaged']['B'] / total],
        [features_count['property_damaged']['C'] / total]
    ],
)

print('TabularCPD contributed_to_accident')
contributed_to_accident_cpd = TabularCPD(
    variable="contributed_to_accident",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["contributed_to_accident", "personal_injured", "property_damaged"], 'ABC'),
    evidence=["personal_injured", "property_damaged",],
    evidence_card=[N_BINS, N_BINS],
)

print('TabularCPD violation_type')
violation_type_cpd = TabularCPD(
    variable="violation_type",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["violation_type", "category", "contributed_to_accident", "arrest_category", "vehicle_category", "belts", "vehicle_age"], 'ABC'),
    evidence=["category", "contributed_to_accident", "arrest_category", "vehicle_category", "belts", "vehicle_age",],
    evidence_card=[N_BINS, N_BINS, N_BINS, N_BINS, N_BINS, N_BINS],
)

print('Adding cpds')

model.add_cpds(
    category_cpd,
    arrest_category_cpd,
    vehicle_age_cpd,
    vehicle_category_cpd,
    belts_cpd,
    personal_injured_cpd,
    property_damaged_cpd,
    contributed_to_accident_cpd,


    violation_type_cpd,
)

print('calculating inference')
inference = VariableElimination(model)

max_n = 7194
correct = 0

for i, r in enumerate(tqdm.tqdm(data.iloc)):
    if i > max_n:
        break
    obj = {**r}
    corr_dict = {
        'A': 0,
        'B': 1,
        'C': 2,
    }
    expected_result = df.iloc[i]['violation_type']
    del obj['violation_type']
    obj = {k: corr_dict[v] for k, v in obj.items()}
    prob = inference.query(variables=["violation_type"], evidence=obj, show_progress=False)
    str_int = {
        1: 0,
        2: 1,
        3: 2,
    }
    if i >= max_n-3:
        print(f'expected_result: {expected_result}, {np.argmax(prob)},\nactual_result: {prob}')
    if np.argmax(prob) == str_int[expected_result]:
        correct += 1

print(f"Accuracy: {correct / i}")


# Get the graph representation of the model
G = nx.DiGraph(model.edges())
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_size=10, node_size=1000, node_color='lightblue')
plt.savefig("../plot/bayesian_network.png")
plt.show()


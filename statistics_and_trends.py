"""
This is the template file for the statistics and trends assignment.
You will be expected to complete all the sections and
make this a fully working, documented file.
You should NOT change any function, file or variable names,
 if they are given to you here.
Make use of the functions presented in the lectures
and ensure your code is PEP-8 compliant, including docstrings.
"""
from corner import corner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns


def plot_relational_plot(df):
    fig, ax = plt.subplots()
    countries = ["United Kingdom", "United States", "China", "India"]
    df_plot = df[df["Country Name"].isin(countries)]

    df_melt = df_plot.melt(
        id_vars="Country Name",
        var_name="Year",
        value_name="CO2"
    )

    df_melt["Year"] = df_melt["Year"].astype(int)

    sns.lineplot(data=df_melt,
                 x="Year",
                 y="CO2",
                 hue="Country Name",
                 ax=ax)

    ax.set_title("CO2 Emissions Over Time")
    plt.savefig('relational_plot.png')
    return


def plot_categorical_plot(df):
    fig, ax = plt.subplots()
    countries = ["United Kingdom", "United States", "China", "India"]
    df_plot = df[df["Country Name"].isin(countries)]

    averages = df_plot.set_index("Country Name").mean(axis=1)

    sns.barplot(x=averages.index,
                y=averages.values,
                ax=ax)

    ax.set_title("Average CO2 Emissions by Country")
    plt.xticks(rotation=30)
    plt.savefig('categorical_plot.png')
    return


def plot_statistical_plot(df):
    fig, ax = plt.subplots()

    countries = ["United Kingdom", "United States", "China", "India"]
    df_plot = df[df["Country Name"].isin(countries)]

    df_melt = df_plot.melt(
        id_vars="Country Name",
        var_name="Year",
        value_name="CO2"
    )

    sns.boxplot(data=df_melt,
                x="Country Name",
                y="CO2",
                ax=ax)

    ax.set_title("Distribution of CO2 Emissions by Country")
    plt.savefig('statistical_plot.png')
    return


def statistical_analysis(df, col: str):
    mean = df[col].mean()
    stddev = df[col].std()
    skew = ss.skew(df[col].dropna())
    excess_kurtosis = ss.kurtosis(df[col].dropna())
    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    print(df.head())
    print(df.describe())

    df = df.dropna(how="all")

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def writing(moments, col):
    print(f'For the attribute {col}:')
    print(f'Mean = {moments[0]:.2f}, '
          f'Standard Deviation = {moments[1]:.2f}, '
          f'Skewness = {moments[2]:.2f}, and '
          f'Excess Kurtosis = {moments[3]:.2f}.')

    if moments[2] > 0.5:
        skew_desc = "right skewed"
    elif moments[2] < -0.5:
        skew_desc = "left skewed"
    else:
        skew_desc = "not skewed"
        
    if moments[3] > 2:
        kurt_desc = "leptokurtic"
    elif moments[3] < -2:
        kurt_desc = "platykurtic"
    else:
        kurt_desc = "mesokurtic"
    
    print(f'The data was {skew_desc} and {kurt_desc}.')
    return


def main():
    df = pd.read_csv('data.csv')
    df = preprocessing(df)
    col = '2018'
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)
    moments = statistical_analysis(df, col)
    writing(moments, col)
    return


if __name__ == '__main__':
    main()

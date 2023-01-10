import pandas as pd
import streamlit as st

df = pd.read_csv("https://data-vins.s3.amazonaws.com/vins.csv")


def main():
    st.title("Les vins que nous vous conseillons")
    
    display_data()


def display_data():
    if st.checkbox("Voir tous"):
        st.dataframe(get_data())


def get_data():
    category = "Fromages"
    newdf = df.loc[df['target'] == category]
    return newdf[['vin', 'type', 'region']]


if __name__ == "__main__":
    main()
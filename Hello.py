# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

LOGGER = get_logger(__name__)


# Import Data
data_path = os.path.join(os.getcwd(), 'data.csv')
df = pd.read_csv(data_path)

df['date'] = pd.to_datetime(df['date'])
df.sort_values(by="date", inplace=True)
df.reset_index(inplace=True)

min_date = df["date"].min()
max_date = df["date"].max()


# Resource
season_mapping = {
    1: "Summer",
    2: "Fall",
    3: "Winter",
    4: "Spring"
}

weather_mapping = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow",
    4: "Heavy Rain"
}


# Function
def calculate_mean_count(main_df, column, target):
    mean_count = main_df[main_df[column] == target]['count'].mean()
    mean_count = 0 if pd.isnull(mean_count) else mean_count
    mean_count_rounded = round(mean_count, 4)
    
    return mean_count_rounded


def run():
    st.set_page_config(
        page_title="Dasboard",
        page_icon="📊",
    )

    st.title('Bike Sharing')

    with st.sidebar:
      st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

      start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
      )

      main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]


    with st.container():
      st.subheader('Statistics')
      col1, col2, col3 = st.columns(3)

      with col1:
          total_rent = main_df["count"].sum()
          st.metric("Total Renter", value=total_rent)
      
      with col2:
          total_casual = main_df["casual"].sum()
          st.metric("Casual", value=total_casual)
          
      with col3:
          total_registered = main_df["registered"].sum()
          st.metric("Registered", value=total_registered)

      plt.figure(figsize=(10, 4))
      sns.lineplot(data=main_df.groupby('hour')['count'].mean().reset_index(), 
                  x='hour', 
                  y='count', 
                  color='blue',
                  marker='o')
      plt.xticks(main_df.groupby('hour')['count'].mean().reset_index()['hour'])
      plt.xlabel(None)
      plt.ylabel(None)
      plt.title("Average Bike Rentals Based on Hours")
      st.pyplot(plt)
    

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.subheader("Based on Season")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            summer_mean = calculate_mean_count(main_df, 'season', 1)
            st.metric("Summer", value=summer_mean)
        
        with col2:
            fall_mean = calculate_mean_count(main_df, 'season', 2)
            st.metric("Fall", value=fall_mean)

        with col3:
            winter_mean = calculate_mean_count(main_df, 'season', 3)
            st.metric("Winter", value=winter_mean)

        with col4:
            spring_mean = calculate_mean_count(main_df, 'season', 4)
            st.metric("Spring", value=spring_mean)
        
        seasons_data = main_df.groupby('season')['count'].mean().reset_index()
        seasons_data = seasons_data.set_index('season').reindex(range(1, 5), fill_value=0).reset_index()
        seasons_data = seasons_data.sort_values(by='count', ascending=False)
        seasons_data['season'] = seasons_data['season'].map(season_mapping)
        
        plt.figure(figsize=(8, 4))
        sns.barplot(data=seasons_data,
                    x='count', 
                    y='season', 
                    orient="h", 
                    color='blue',
                    order=seasons_data['season'])
        plt.xlabel(None)
        plt.ylabel(None)
        plt.title("Average Bike Rentals Based on Season")
        
        st.pyplot(plt)


    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.subheader("Based on Weather")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            summer_mean = calculate_mean_count(main_df, 'weathersit', 1)
            st.metric("Clear", value=summer_mean)
        
        with col2:
            fall_mean = calculate_mean_count(main_df, 'weathersit', 2)
            st.metric("Mist", value=fall_mean)

        with col3:
            winter_mean = calculate_mean_count(main_df, 'weathersit', 3)
            st.metric("Light Snow", value=winter_mean)

        with col4:
            spring_mean = calculate_mean_count(main_df, 'weathersit', 4)
            st.metric("Heavy Rain", value=spring_mean)
        
        weathersit_data = main_df.groupby('weathersit')['count'].mean().reset_index()
        weathersit_data = weathersit_data.set_index('weathersit').reindex(range(1, 5), fill_value=0).reset_index()
        weathersit_data = weathersit_data.sort_values(by='count', ascending=False)
        weathersit_data['weathersit'] = weathersit_data['weathersit'].map(weather_mapping)
        
        plt.figure(figsize=(8, 6)) 
        sns.barplot(data=weathersit_data, 
                    x='weathersit', 
                    y='count', 
                    orient='v', 
                    color='blue',
                    order=weathersit_data['weathersit'])
        plt.xlabel(None)
        plt.ylabel(None)
        plt.title("Average Bike Rentals Based on Weather")

        st.pyplot(plt)


if __name__ == "__main__":
    run()

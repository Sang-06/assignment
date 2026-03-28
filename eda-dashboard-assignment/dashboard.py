import streamlit as st
import plotly.express as px
from fetch_data import get_cleaned_data

#Load the data from other file
df = get_cleaned_data()

st.title("strategic Post Analysis Dashboard")

#Task : Dataset preview
st.subheader("Data Preview")
st.dataframe(df.head()) # Interactive table

# Task: Exploratory Analysis (Groupby)
# count (posts) per user_id how many
posts_per_user = df.groupby('user_id').size().reset_index(name='post_count')

#Task : Visualize - Bar Chart
st.subheader("Posts Created per User")
fig_bar = px.bar(posts_per_user, x='user_id', y='post_count', color='user_id')
st.plotly_chart(fig_bar)

#Task : Visualize - Histogram(post length distribution)
st.subheader("Distribution of Post Lengths")
fig_hist = px.histogram(df, x='post_length', nbins=20, color_discrete_sequence=['indianred'])
st.plotly_chart(fig_hist)
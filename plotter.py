import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("CSV Data Visualizer")

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Display the first few rows of the dataframe
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())

        # Select column for grouping
        group_column = st.selectbox("Select column to group by", df.columns)

        # Select column for aggregation
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        agg_column = st.selectbox("Select numeric column to aggregate", numeric_columns)

        if group_column and agg_column:
            # Group and aggregate the data
            summary_df = df.groupby(group_column)[agg_column].sum().reset_index()

            # Display the summary table
            st.subheader("Summary Table")
            st.dataframe(summary_df)

            # Plot using Matplotlib
            st.subheader("Matplotlib Visualization")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(summary_df[group_column], summary_df[agg_column], color='skyblue')
            ax.set_xlabel(group_column)
            ax.set_ylabel(f"Total {agg_column}")
            ax.set_title(f"{agg_column} by {group_column}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Plot using Plotly
            st.subheader("Plotly Visualization")
            fig_plotly = px.bar(
                summary_df, 
                x=group_column, 
                y=agg_column,
                title=f"{agg_column} by {group_column}",
                labels={group_column: group_column, agg_column: f"Total {agg_column}"}
            )
            st.plotly_chart(fig_plotly)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to begin.")

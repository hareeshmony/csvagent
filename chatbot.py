import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

if user_input := st.chat_input("........"):
    with st.chat_message("User"):
        st.markdown(user_input)
        st.session_state.chat_history.append({"role": "User", "content": user_input})

    if temp_file_path == '':
        with st.chat_message("Assistant"):
            st.markdown("Please upload a .csv file for Q&amp;amp;A")
            st.session_state.chat_history.append({"role": "Assistant", "content": "Please upload a .csv file for Q&amp;amp;A"})
    else:
        # Load the CSV
        df = pd.read_csv(temp_file_path)

        # Example: If user asks for a plot or summary, trigger the logic
        if "plot" in user_input.lower() or "summary" in user_input.lower():
            with st.chat_message("Assistant"):
                st.subheader("Preview of Uploaded Data")
                st.dataframe(df.head())

                # Let user select columns for grouping and aggregation
                group_column = st.selectbox("Select column to group by", df.columns, key="group_col")
                numeric_columns = df.select_dtypes(include='number').columns.tolist()
                agg_column = st.selectbox("Select numeric column to aggregate", numeric_columns, key="agg_col")

                if group_column and agg_column:
                    summary_df = df.groupby(group_column)[agg_column].sum().reset_index()

                    st.subheader("Summary Table")
                    st.dataframe(summary_df)

                    # Matplotlib plot
                    st.subheader("Matplotlib Visualization")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(summary_df[group_column], summary_df[agg_column], color='skyblue')
                    ax.set_xlabel(group_column)
                    ax.set_ylabel(f"Total {agg_column}")
                    ax.set_title(f"{agg_column} by {group_column}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                    # Plotly plot
                    st.subheader("Plotly Visualization")
                    fig_plotly = px.bar(
                        summary_df,
                        x=group_column,
                        y=agg_column,
                        title=f"{agg_column} by {group_column}",
                        labels={group_column: group_column, agg_column: f"Total {agg_column}"}
                    )
                    st.plotly_chart(fig_plotly)

                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "Assistant",
                        "content": f"Summary and plots for {agg_column} by {group_column} shown above."
                    })
                else:
                    st.warning("Please select valid columns for grouping and aggregation.")
                    st.session_state.chat_history.append({
                        "role": "Assistant",
                        "content": "Please select valid columns for grouping and aggregation."
                    })
        else:
            # Default: Use your csv_agent and plotter logic for other questions
            csv_agent_response = csv_agent.csv_agent_invoker(temp_file_path, user_input, GROQ_API_KEY)
            html_content, response = plotter.output_formatter(user_input, csv_agent_response)

            with st.chat_message("Assistant"):
                st.markdown(response)
                if html_content != "":
                    with st.expander("📈📝 See explanation "):
                        st.components.v1.html(html_content, height=600, scrolling=True)

                st.session_state.chat_history.append({"role": "Assistant", "content": response, "html_content": html_content})

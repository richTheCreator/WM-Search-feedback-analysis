import urllib.error


def time_chart():
    import streamlit as st
    import pandas as pd
    import altair as alt

    @st.cache(allow_output_mutation=True)
    def fetch_dates():
        df = pd.read_csv('./csv/search_feedback.csv',
                         usecols=['created_at', 'isHelpful'])
        return df
        # df = df_loc.join(df_loc['location'].str.split(',', expand=True))

    df_datetime = fetch_dates()
    df_datetime['created_at'] = df_datetime['created_at'].astype('datetime64')

    st.write('### Monthly')
    month_of_year = alt.Chart(df_datetime).mark_bar().encode(
        x="yearmonth(created_at):O",
        y="count(isHelpful)):Q",
        tooltip=['count(created_at):Q'],
        color='isHelpful'
    ).properties(
        height=500
    )
    st.altair_chart(month_of_year, True)
    st.info('Why did this drop off by 40% since October?')

    st.write('### Day of month')
    day_of_month = alt.Chart(df_datetime).mark_bar(opacity=.8).encode(
        x="monthdate(created_at):O",
        y="count(isHelpful):Q",
        tooltip=['count(created_at):Q', 'monthdate(created_at):O'],
        color='isHelpful'
    ).properties(
        height=500
    )

    line = alt.Chart(df_datetime).mark_line(color='green').encode(
        x="month(created_at):O",
        y="count(isHelpful):Q",
    ).properties(
        height=500
    )

    layered = alt.layer(day_of_month, line).resolve_scale(y='independent')
    st.altair_chart(layered, True)
    st.info('The start of Oct is when the drop-off for submissions started.')

    st.write('### Time of day')
    hour_of_day = alt.Chart(df_datetime).mark_bar().encode(
        x="hours(created_at):O",
        y="count(isHelpful):Q",
        tooltip=['count(created_at):Q', 'hours(created_at):O'],
        color='isHelpful'
    ).properties(
        height=500
    )
    st.altair_chart(hour_of_day, True)
    st.info('This doesn"t lineup with search volume trends. Search peeks at noon and drops rapidly after.')

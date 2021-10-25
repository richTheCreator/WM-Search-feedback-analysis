def intro():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('./csv/search_feedback.csv',
                     usecols=['location', 'regionSlug', 'queryText', 'isHelpful', 'created_at', 'isMobileDevice', 'email'])

    st.markdown(
        """
        # Goal ⛰
        >*The goal of this analysis is to get a more intiment understanding of how
        real Weedmaps users are talking about search. In turn this should provide actionable
        insights to improve our search experience with.*

        # Strategy
        Apply several text mining methods to the unstructured responses that users submit on search.
        
        ---
        
        # Data-set info
    """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"### Date Range")
        st.write("7/8 - 11/25")
        # st.write(f"{str(start_date)} - {str(end_date)}")
    with col2:
        st.write(f"### # of results")
        n = len(df.index)
        st.write(n)
    with col3:
        st.write(f"### Unique regions")
        n = len(pd.unique(df['regionSlug']))
        st.write(n)

    col4, col5 = st.columns(2)
    with col4:
        n = df['isMobileDevice'].value_counts()

        st.write(f"### User device \n Whether the device is mobile or not")
        fig, ax = plt.subplots()
        ax.pie(n, labels=['Is Mobile', 'Not Mobile'], autopct='%1.1f%%',
               shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        st.pyplot(fig)

        st.table(n)
    with col5:
        st.write(f"### Helpfulness \n The yes/no response users submit")
        n = df['isHelpful'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(n, labels=['No', 'Yes'], autopct='%1.1f%%',
               shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        st.pyplot(fig)

        st.table(n)

    col6, col7 = st.columns(2)
    with col6:
        st.write(f"### User auth \n How many people are signed in?")
        n = df['email'].isnull().value_counts()
        fig, ax = plt.subplots()
        ax.pie(n, labels=['Logged In', 'Logged out'], autopct='%1.1f%%',
               shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        st.pyplot(fig)

        st.table(n)
    with col7:
        st.write(f"### Has search term \n Was a term entered in the search bar?")
        n = df['queryText'].isnull().value_counts()
        fig, ax = plt.subplots()
        ax.pie(n, labels=['No Term', 'Has Term'], autopct='%1.1f%%',
               shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        st.pyplot(fig)

        st.table(n)

    # labels = ['Has term', 'No term']

    # fig, ax = plt.subplots()
    # ax.pie(df['hasSearchTerm'], autopct='%1.1f%%',
    #        shadow=True, startangle=90)
    # # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax.axis('equal')
    # st.pyplot(fig)

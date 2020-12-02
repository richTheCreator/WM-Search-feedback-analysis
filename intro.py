def intro():
    import streamlit as st
    import pandas as pd
    df = pd.read_csv('./csv/search_feedback.csv',
                     usecols=['location', 'regionSlug', 'isHelpful', 'created_at', 'isMobileDevice', 'email'])

    st.markdown(
        """
        ### Goal ⛰
        >*The goal of this analysis is to get a more intiment understanding of how 
        real Weedmaps users are talking about search. In turn this should provide actionable
        insights to improve our search experience with.* 
        
        ### Strategy
        Apply several text mining methods to the unstructured responses that users submit on search. 

        # Data-set info
    """
    )

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.write(f"### Date Range")
        st.write("7/8 - 11/25")
        # st.write(f"{str(start_date)} - {str(end_date)}")
    with col2:
        st.write(f"### Helpfulness")
        neg = df['isHelpful'] == 0
        neg_amount = len(df[neg])
        st.write(f"* Not helpful - {neg_amount}")
        pos = df['isHelpful'] == 1
        pos_amount = len(df[pos])
        st.write(f"* Is helpful - {pos_amount}")
    with col3:
        st.write(f"### User device")
        notMobile = df['isMobileDevice'] == 0
        notMobile_amount = len(df[notMobile])
        st.write(f"* Not Mobile - {notMobile_amount}")

        mweb = df['isMobileDevice'] == 1
        mweb_amount = len(df[mweb])
        st.write(f"* Is Mobile - {mweb_amount}")

    col4, col5 = st.beta_columns(2)
    with col4:
        st.write(f"### Unique regions")
        n = len(pd.unique(df['regionSlug']))
        st.write(n)
    with col5:
        st.write(f"### # of results")
        n = len(df.index)
        st.write(n)
    # with col6:
    #     st.write(f"### Logged in")
    #     hasEmail = df['email'] != ''
    #     n = len(df[hasEmail])
    #     st.write(n)

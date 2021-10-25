def entities():
    import streamlit as st
    import pandas as pd
    import altair as alt

    st.write('# All entities \n The amount of times an entity was recognized in the search-feedback response.')
    df = pd.read_json(
        './csv/entities_agg.json', typ='series').reset_index()
    df = df.rename(
        columns={'index': 'Entity', 0: 'Freq'})

    ent_chart = alt.Chart(df).mark_bar(size=20).encode(
        x=alt.X('Freq', axis=alt.Axis(title='Counts')),
        y=alt.Y('Entity',
                sort=alt.EncodingSortField(
                    field='Freq', order='descending', op='sum'),
                axis=alt.Axis(title='Title')
                ),
        tooltip=['Freq'],
        color='Entity',
    ).configure_axis(
        labelFontSize=18,
        titleFontSize=20
    )
    st.altair_chart(ent_chart, True)

    df_feedback = pd.read_csv(
        './csv/WM_Entities.csv', usecols=['response', 'isHelpful', 'created_at', 'WM Entities'])
    df_feedback.dropna(subset=['WM Entities'], inplace=True)

    entity_dict = {}
    entities_df = {}

    def entity_dict_from_df(ent_cell):
        ent_dict = eval(ent_cell)
        dataList = ent_dict['entities']
        for dic in dataList:
            label = dic['label']
            key = dic['key']
            if label in entity_dict:
                entity_dict[label].append(key)
            else:
                entity_dict[label] = [key]

    # change the df used pos/neg to view different results
    df_feedback['WM Entities'].apply(entity_dict_from_df)
    # st.write(entity_dict)

    def df_entity_gen(ent_dict):
        for dic in ent_dict:
            series = (pd.Series(entity_dict[dic]).value_counts())
            df = series.to_frame().reset_index()
            df = df.rename(
                columns={'index': 'Term', 0: 'Freq'})
            entities_df[dic] = df

    df_entity_gen(entity_dict)
    # st.write(entities_df)

    def chart_gen(entity_df):
        ent_chart = alt.Chart(entity_df).mark_bar(size=20).encode(
            x=alt.X('Freq', axis=alt.Axis(title='Counts')),
            y=alt.Y('Term',
                    sort=alt.EncodingSortField(
                        field='0', order='descending', op='sum'),
                    axis=alt.Axis(title='Terms')
                    ),
            tooltip=['Freq'],
            color='Term',
        ).configure_axis(
            labelFontSize=18,
            titleFontSize=20
        )
        return st.altair_chart(ent_chart, True)

    # for df in entities_df:
    #     st.write(f'### {df}')
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         chart_gen(entities_df[df][:25])
    #     with col2:
    #         st.write(entities_df[df])

    # sidebar config
    sidebar_entity_select = st.sidebar.selectbox(
        " Entity type", ['PRODUCT', 'GPE', 'PRODUCT_TAG', 'STRAIN', 'SERVICE', 'ORG', 'RETAILER', 'TAGKIND', 'QUANTITY', 'MONEY', 'CARDINAL'], 0)
    st.write(f'# {sidebar_entity_select.capitalize()} \n ## Top 25  terms')
    chart_gen(entities_df[sidebar_entity_select][:25])
    st.write('## All terms')
    st.table(entities_df[sidebar_entity_select])


entities()

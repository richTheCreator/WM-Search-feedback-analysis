def entities():
    import nltk
    import streamlit as st
    import requests
    from nltk.corpus import stopwords
    from collections import Counter
    from io import StringIO
    import pandas as pd
    import altair as alt
    import json

    # alt.themes.enable('vox')
    # df = pd.read_json(
    #     './csv/entities_agg.json', typ='series').reset_index()
    # df = df.rename(
    #     columns={'index': 'Entity', 0: 'Freq'})

    # ent_chart = alt.Chart(df).mark_bar(size=20).encode(
    #     x=alt.X('Freq', axis=alt.Axis(title='Counts')),
    #     y=alt.Y('Entity',
    #             sort=alt.EncodingSortField(
    #                 field='Freq', order='descending', op='sum'),
    #             axis=alt.Axis(title='Title')
    #             ),
    #     tooltip=['Freq'],
    #     color='Entity',
    # ).configure_axis(
    #     labelFontSize=18,
    #     titleFontSize=20
    # )
    # st.altair_chart(ent_chart, True)

    # GENERATOR FN
    df_feedback = pd.read_csv(
        './csv/search_feedback.csv', usecols=['response', 'isHelpful', 'created_at'])
    df_feedback.dropna(subset=['response'], inplace=True)

    url = 'https://weedmaps-api-ner-acceptance.internal-weedmaps.com/entities?term='

    entity_dict = {}

    # def entity_agg_gen(text):
    #     req = requests.get(
    #         url + text).json()
    #     if 'error' not in req:
    #         if 'data' in req:
    #             for key, value in req['data']['entity_labels'].items():
    #                 if key in entity_dict:
    #                     entity_dict[key] += value
    #                 else:
    #                     entity_dict[key] = value
    # with open('./csv/entities_agg.json', 'w', encoding='utf-8') as f:
    #     json.dump(entity_dict, f, ensure_ascii=False, indent=4)

    # create a col with the raw response from the entity API
    # @st.cache
    def entity_col(text):
        req = requests.get(
            url + text).json()
        if 'error' not in req:
            if 'data' in req:
                res_dict = {
                    'labels': req['data']['entity_labels'],  # dict
                    'entities': req['data']['entities']  # list
                }
                return res_dict
    # df_feedback = df_feedback.head(20)

    df_feedback['WM Entities'] = df_feedback['response'].apply(entity_col)
    df_feedback.to_csv('./csv/WM_Entities.csv', index=False)

    st.write('### Entities')
    st.write(df_feedback)
    #  save as csv

    # parse the entity column to create new dict of entities and associated terms

    # def entity_dict_from_df(ent_dict):
    #     dataList = ent_dict['entities']
    #     for dic in dataList:
    #         label = dic['label']
    #         key = dic['key']
    #         if label in entity_dict:
    #             entity_dict[label].append(key)
    #         else:
    #             entity_dict[label] = [key]

    # # change the df used pos/neg to view different results
    # df_feedback['WM Entities'].apply(entity_dict_from_df)
    # st.write(entity_dict)

    # product_series = (pd.Series(entity_dict['PRODUCT']).value_counts())[:25]

    # product_df = product_series.to_frame().reset_index()
    # st.write(product_df)

    # ner_df = pd.DataFrame.from_dict(entity_dict['PRODUCT'])
    # st.write(ner_df)
# {
#     'labels': {'PRODUCT': 1},
#     'entities': [
#         {
#             'key': 'investment',
#             'label': 'PRODUCT',
#             'text': 'Investments',
#             'token_end': 1,
#             'token_start': 0
#         }
#     ]
# }

# # GOAL: Create a list of all terms that are associated with an entity

# # this might need to be several dataframes
# # a data frame for each entity


entities()

import urllib.error


def mapping_demo():
    import matplotlib.pyplot as plt
    import pandas as pd
    import pydeck as pdk
    import streamlit as st

    # @st.cache
    def fetch_geos():
        df_loc = pd.read_csv('./csv/search_feedback.csv',
                             usecols=['location', 'regionSlug', 'isHelpful'])
        df_geos = df_loc.join(df_loc['location'].str.split(',', expand=True))
        del df_geos['location']
        geos_res = df_geos.rename(
            columns={'regionSlug': 'Region', 0: 'latitude', 1: 'longitude', 2: 'isHelpful'})

        # add frequency col
        geos_res['Freq'] = geos_res['Region'].groupby(
            geos_res['Region']).transform('count')
        # create new df groupedby region, lat, long
        geos_res = geos_res.groupby(['Region', 'latitude', 'longitude', 'isHelpful'])[
            'Freq'].count().reset_index()
        # cast to numeric
        geos_res[['latitude', 'longitude']] = geos_res[[
            'latitude', 'longitude']].apply(pd.to_numeric)
        return geos_res

    # sidebar config
    # feedback type selector
    feedback_type = st.sidebar.selectbox(
        " Feedback type", ['All', '👍 Positive', '👎 Negative'], 0)
    df_geos = fetch_geos()
    if feedback_type == "All":
        df_geos = fetch_geos()
    elif feedback_type == '👎 Negative':
        df_geos = fetch_geos()
        neg = df_geos['isHelpful'] == 0
        df_geos = df_geos[neg]
    elif feedback_type == '👍 Positive':
        df_geos = fetch_geos()
        pos = df_geos['isHelpful'] == 1
        df_geos = df_geos[pos]

    st.write('### Number of results:', df_geos['Freq'].sum())

    try:
        ALL_LAYERS = {
            "Heatmap": pdk.Layer(
                "HeatmapLayer",
                data=df_geos,
                get_position="[longitude, latitude]",
                auto_highlight=False,
                aggregation="MEAN",
                opacity=0.4,
                get_weight="Freq"
            ),
            # "Hexagon": pdk.Layer(
            #     'HexagonLayer',  # `type` positional argument is here
            #     data=df_geos,
            #     get_position="[longitude, latitude]",
            #     auto_highlight=True,
            #     elevation_scale=100,
            #     pickable=True,
            #     elevation_range=[0, 3000],
            #     # aggregation="SUM",
            #     extruded=True,
            #     get_elevation_weight="Freq",
            #     coverage=1,
            #     radius=50
            # ),
            "Scatter": pdk.Layer(
                "ScatterplotLayer",
                data=df_geos,
                pickable=True,
                opacity=1,
                stroked=True,
                filled=True,
                radius_scale=6,
                radius_min_pixels=2,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_position="[longitude, latitude]",
                get_radius="Freq",
                get_fill_color=[78, 208, 208],
                get_line_color=[0, 0, 0],
            ),
        }
    except urllib.error.URLError as e:
        st.error("""
            **This demo requires internet access.**
            Connection error: %s
        """ % e.reason)
        return
    # view stat config
    view_state = pdk.data_utils.viewport_helpers.compute_view(
        df_geos[['longitude', 'latitude']]
    )
    view_state.pitch = 3
    view_state.zoom = 3
    view_state.bearing = 0

    # map layers config
    st.sidebar.markdown('### Map Layers')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(layers=selected_layers, initial_view_state=view_state, tooltip={
            "text": "# of feedback: {Freq}"
        }))
    else:
        st.error("Please choose at least one layer above.")

    # top_regions = df_geos['Freq'] > 25
    st.write('### Top 15 regions \n Sorted by number of submissions. ')
    st.table(df_geos.sort_values('Freq', ascending=False).head(15))
    st.info('Can use this information to drill in to each region and identify why this type of feedback is being submitted.')
    st.info('Can cluster by super regions to identify aggregrate trends.')

# fmt: on

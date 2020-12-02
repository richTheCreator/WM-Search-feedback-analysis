
import inspect
import textwrap
from collections import OrderedDict
import streamlit as st
from streamlit.logger import get_logger
from intro import intro
from map_chart import mapping_demo
from time_chart import time_chart
from freq_NLTK import freq_NLTK
from nounchunks_spaCy import nounchunks
from entity_classification import entities

st.set_page_config(
    page_title="WM Search Feedback",
    page_icon="WM",
    layout="wide",
    initial_sidebar_state="expanded",
)
LOGGER = get_logger(__name__)

# Dictionary of
# demo_name -> (demo_function, demo_description)
DEMOS = OrderedDict(
    [
        ("Overview", (intro, None)),
        (
            "🗺 Geospatial data",
            (
                mapping_demo,
                """
> *Take a look at where in the world WM search feedback is coming from.*
""",
            ),
        ),
        (
            "🕔 Time data",
            (
                time_chart,
                """
> *Take a look at when feedback for WM search is being submitted.*
""",
            ),
        ),
        (
            " 💬 N-Grams ",
            (
                freq_NLTK,
                """
> *The essential concepts in text mining is n-grams, which are a set of co-occurring or continuous sequence of n items from a sequence of large text or sentence.*
""",
            ),
        ),
        (
            " 💬 Noun chunks ",
            (
                nounchunks,
                """
> *Noun chunks are “base noun phrases” – flat phrases that have a noun as their head. You can think of noun chunks as a noun plus the words describing the noun – for example, “the lavish green grass” or “the world’s largest tech fund”. *
""",
            ),
        ),
        (
            " 💬 Entities ",
            (
                entities,
                """
> *Taking a look at topic classifications with help from the WM Entity API.*
""",
            ),
        ),
    ]
)


def run():
    demo_name = st.sidebar.selectbox(
        "Choose an analysis", list(DEMOS.keys()), 0)
    demo = DEMOS[demo_name][0]

    if demo_name == "—":
        show_code = False
        st.write("# Welcome to Streamlit! 👋")
    else:
        show_code = st.sidebar.checkbox("Show code", True)
        st.markdown("# %s" % demo_name)
        description = DEMOS[demo_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(10):
            st.empty()

    demo()

    if show_code:
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


if __name__ == "__main__":
    run()

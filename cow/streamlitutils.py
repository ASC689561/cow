from .class_util import get_subclasses


class Page:
    name = 'NoName'

    def __init__(self):
        pass

    def run(self):
        pass


def set_max_width():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


def run():
    import streamlit as st
    all_class = {x.name: x for x in get_subclasses(Page)}
    arr = sorted(list(all_class.keys()))
    task = st.sidebar.selectbox('Function', arr)
    t = all_class[task]
    e = t()
    e.run()

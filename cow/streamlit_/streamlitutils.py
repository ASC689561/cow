from cow.class_util import get_subclasses


class Page:
    name = 'NoName'

    def __init__(self):
        pass

    def run(self):
        pass


def set_max_width():
    import streamlit as st
    max_width_str = "max-width: 2000px;"
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


def run(selected_page=None):
    import streamlit as st
    all_class = {x.name: x for x in get_subclasses(Page)}
    arr = sorted(list(all_class.keys()))

    if selected_page and selected_page.lower() in [x.lower() for x in arr]:
        arr = sorted(arr, key=lambda x: x.lower() == selected_page.lower(), reverse=True)
    task = st.sidebar.selectbox('Function', arr)
    t = all_class[task]
    e = t()
    e.run()

from .class_util import get_subclasses


class Page:
    name = 'NoName'

    def __init__(self):
        pass

    def run(self):
        pass


def run():
    import streamlit as st
    all_class = {x.name: x for x in get_subclasses(Page)}
    arr = sorted(list(all_class.keys()))
    task = st.sidebar.selectbox('Function', arr)
    t = all_class[task]
    e = t()
    e.run()

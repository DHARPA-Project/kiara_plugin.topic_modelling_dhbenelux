import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation

def app():
    kiara = st.session_state["kiara"]
    df = st.session_state.init_df

    # this is just a test to check that kiara instance can be used
    # in multpage set-up from streamlit session store
    
    result = []
    for alias, alias_item in kiara.alias_registry.aliases.items():
        value = kiara.data_registry.get_value(alias_item.value_id)
        if value.data_type_name == "table":
            result.append(alias)
    
    if not result:
        st.sidebar.write(" -- no tables --")
    else:
        for a in result:
            st.write(a)

    st.dataframe(df)
import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation

def app():
    kiara = st.session_state["kiara"]
    data_alias = st.session_state['data_alias']
    table_value = kiara.data_registry.get_value(f'alias:{data_alias}')
    
    df = st.session_state.init_df

    st.write("##### 2. Tokenization")
    
    col = st.selectbox('Select column for text content', df.columns, index=0)
    button = st.button('Tokenize')

    if col and button:
        op = KiaraOperation(kiara=kiara, operation_name="table.cut_column")
        inputs = {'table': table_value, 'column_name': col}
        job_id = op.queue_job(**inputs)

        try:
             op.save_result(
            job_id=job_id, aliases={'array': 'data_col'}
        )
        except Exception:
            pass

        op = KiaraOperation(kiara=kiara, operation_name="tokenize.texts_array")
        inputs = {'texts_array':'alias:data_col'}
        job_id = op.queue_job(**inputs)

        try:
             op.save_result(
            job_id=job_id, aliases={'tokens_array': 'tokens_array'}
        )
        except Exception:
            pass

        table_value = kiara.data_registry.get_value('alias:tokens_array')

        if not table_value:
            st.write('Table not found')
        
        else:

            tokens_array = table_value.data
            series = tokens_array.arrow_array.to_pandas()
            st.dataframe(series)
import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation


def app():

    kiara = Kiara.instance()

    if 'kiara' not in st.session_state:
        st.session_state['kiara'] = kiara

    st.write("##### 1. Data Onboarding")
    st.markdown("Paste local folder path into input below") 

    path = st.text_input('Path to files folder')
    data_alias = st.text_input('alias')
    button = st.button("Onboard")

    if button and data_alias:

        #print(data_alias)

        st.session_state['data_alias'] = data_alias
        op = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
        inputs = {"path": path}
        job_id = op.queue_job(**inputs)

        try:
            op.save_result(
            job_id=job_id, aliases={'file_bundle': 'text_file_bundle'}
        )
        except Exception:
            pass

       
        op = KiaraOperation(kiara=kiara, operation_name="create.table.from.text_file_bundle")
        inputs = {"text_file_bundle": 'alias:text_file_bundle'}
        job_id = op.queue_job(**inputs)

        try:
            op.save_result(
            job_id=job_id, aliases={"table": data_alias}
        )
        except Exception:
            pass

        
        # result = []
        # for alias, alias_item in kiara.alias_registry.aliases.items():
        #     value = kiara.data_registry.get_value(alias_item.value_id)
        #     if value.data_type_name == "table":
        #         result.append(alias)

        table_value = kiara.data_registry.get_value(f'alias:{data_alias}')

        if not table_value:
            st.write('Table not found')
        
        else:
            actual_table_obj = table_value.data
            arrow_table = actual_table_obj.arrow_table
            df = arrow_table.to_pandas()
            st.dataframe(df)
            if 'init_df' not in st.session_state:
                st.session_state['init_df'] = df

                


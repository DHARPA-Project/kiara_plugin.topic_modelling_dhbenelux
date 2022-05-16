import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation


def app():

    kiara = Kiara.instance()

    if 'kiara' not in st.session_state:
        st.session_state['kiara'] = kiara

    st.markdown("Download the corpus on your computer, unzip and copy local folder path to 1 publication")
    st.markdown("https://zenodo.org/record/4596345/files/ChroniclItaly_3.0_original.zip?download")
    st.markdown("Paste local folder path into input below") 
    st.markdown("Wait for the success message, and then select next page in top left nav menu")

    path = st.text_input('Path to files folder')
    button = st.button("Onboard")

    if button:
        op = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
        inputs = {"path": path}
        job_id = op.queue_job(**inputs)

        op.save_result(
            job_id=job_id, aliases={"file_bundle": 'text_corpus_bundle'}
        )

        op = KiaraOperation(kiara=kiara, operation_name="create.table.from.csv_file_bundle")
        inputs = {"csv_file_bundle": 'alias:text_corpus_bundle.file_bundle'}
        job_id = op.queue_job(**inputs)

        op.save_result(
            job_id=job_id, aliases={"table": 'cronaca_sovversiva'}
        )

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

















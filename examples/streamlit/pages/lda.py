import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation
from kiara_plugin.language_processing.language_processing.tokens import get_stopwords
import pandas as pd

def app():

    kiara = st.session_state["kiara"]

    compute_coherence = st.checkbox("Compute coherence")
    if not compute_coherence:
        number_of_topics_min = st.number_input('Number of topics', min_value = 1, value=7)
        number_of_topics_max = number_of_topics_min
    else:
        number_of_topics_min = st.number_input('Min number of topics', min_value = 1, value=4)
        number_of_topics_max = st.number_input('Max number of topics', min_value=1, value=7)

    button = st.button("Generate topics")
    if button:

        # print(compute_coherence)
        
        table_value = kiara.data_registry.get_value('alias:tokens_array')
        
        op = KiaraOperation(kiara=kiara, operation_name="generate.LDA.for.tokens_array")
        inputs = {
            'tokens_array': table_value,
            'num_topics_min': number_of_topics_min,
            'num_topics_max': number_of_topics_max,
            'compute_coherence': compute_coherence
            }
        job_id = op.queue_job(**inputs)

        try:
             op.save_result(
            job_id=job_id, aliases={'topic_models': 'topic_models', 'coherence_table': 'coherence_table', 'coherence_map': 'coherence_map'}
        )
        except Exception:
            pass
    
    
    topic_models_value = kiara.data_registry.get_value('alias:topic_models')
    topic_models = topic_models_value.data.dict_data
    coherence_table = kiara.data_registry.get_value('alias:coherence_table')
    coherence_map = kiara.data_registry.get_value('alias:coherence_map')

    st.write("### Coherence score")
    if compute_coherence is False:
        st.write("Coherence not considered.")
    else:
        if coherence_map is not None:
            #print(coherence_map)
            c_map = coherence_map.data.dict_data
            
            df_coherence = pd.DataFrame(c_map.keys(), columns=['Number of topics'])
            df_coherence['Coherence'] = c_map.values()


            st.vega_lite_chart(df_coherence, {
                "mark": {"type": "line", "point": True, "tooltip": True},
                "encoding": {
                    "x": {"field": "Number of topics", "type": "quantitative", "axis": {"format": ".0f", "tickCount": len(df_coherence)-1}},
                    "y": {"field": "Coherence", "type": "quantitative", "format": ".3f"}
                }
                
            }, use_container_width=True)


            st.table(df_coherence)
            save = st.checkbox("Save coherence table")
            if save:
                alias = st.text_input("Alias")
                save_btn = st.button("Save")
                if save_btn:
                    if not alias:
                        st.info("Not saving table, no alias provided.")
                    else:
                        saved = coherence_table.save(aliases=[alias])
                        st.info(f"Coherence table saved with alias '{alias}', value id: {saved.id}")

        else:
            st.write("No coherence computed (yet).")

    st.write("### Model details")
    if topic_models is None:
        st.write("No models available (yet).")
    else:
        all_topic_models = topic_models
        
        if not compute_coherence:
            selected_model_idx = number_of_topics_min
        else:
            selected_model_idx = st.selectbox("Number of topics", options=range(number_of_topics_min, number_of_topics_max+1))

        try:
            selected_model_table = all_topic_models[str(selected_model_idx)]
            st.table(pd.DataFrame(selected_model_table, columns=['id','model']))
        except KeyError:
            st.write(f"No model for {selected_model_idx} number of topics.")

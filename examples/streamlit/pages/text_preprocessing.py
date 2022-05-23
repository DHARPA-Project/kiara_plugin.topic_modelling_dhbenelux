import streamlit as st
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation
from kiara_plugin.language_processing.language_processing.tokens import get_stopwords

def app():
    kiara = st.session_state["kiara"]
    data_alias = st.session_state['data_alias']
    
    
    st.write("##### 3. Text pre-processing")

    left, center, right = st.columns([2, 4, 2])
    left.write("##### Lowercase")
    lowercase = left.checkbox("Convert to lowercase")
    
    center.write("##### Numbers and punctuation")
    remove_alphanumeric = center.checkbox("Remove all words that contain numbers (e.g. ex1ample)")
    remove_non_alpha = center.checkbox("Remove all words that contain punctuation and numbers (e.g. ex1a.mple)")
    remove_all_numeric = center.checkbox("Remove numbers only (e.g. 876)")

    right.write("##### Words length")
    display_shorttokens = [0, 1, 2, 3, 4, 5]
    def _temp(token_len):
        if token_len == 0:
            return "Select number of characters"
        else:
            return str(token_len)
    shorttokens = right.selectbox(
        "Remove words shorter than X characters",
        options=display_shorttokens,
        format_func=lambda x: _temp(x),
    )

    st.write("##### Remove stopwords")
    all_stopword_languages = get_stopwords().fileids()
    languages = st.multiselect("Select the preferred language(s) for the stopword list(s) (NLTK)", options=sorted(all_stopword_languages))
    
    if languages:
        # remove_stopwords.from.tokens_array

        op = KiaraOperation(kiara=kiara, operation_name="create.stopwords_list")
        inputs = {
            'languages': languages,
            }
        job_id = op.queue_job(**inputs)

        try:
            op.save_result(
            job_id=job_id, aliases={'stopwords_list': 'stopwords_list'}
        )
        except Exception:
            pass
        
        stopwords_data = kiara.data_registry.get_value("alias:stopwords_list").data
        stopwords_list = stopwords_data.list_data
        st.dataframe(stopwords_list)

    proceed = st.button('Proceed')

    if proceed:

        if stopwords_list:

            op = KiaraOperation(kiara=kiara, operation_name="preprocess.tokens_array")
            inputs = {
                'tokens_array': 'alias:tokens_array', 
                'to_lowercase': lowercase,
                'remove_alphanumeric': remove_alphanumeric,
                'remove_non_alpha': remove_non_alpha,
                'remove_all_numeric': remove_all_numeric,
                'remove_short_tokens': shorttokens,
                'remove_stopwords': 'alias:stopwords_list',
                }
            job_id = op.queue_job(**inputs)

            try:
                op.save_result(
                job_id=job_id, aliases={'tokens_array': 'preprocessed_tokens'}
            )
            except Exception:
                pass
        
        else:

            op = KiaraOperation(kiara=kiara, operation_name="preprocess.tokens_array")
            inputs = {
                'tokens_array': 'alias:tokens_array', 
                'to_lowercase': lowercase,
                'remove_alphanumeric': remove_alphanumeric,
                'remove_non_alpha': remove_non_alpha,
                'remove_all_numeric': remove_all_numeric,
                'remove_short_tokens': shorttokens,
                }
            job_id = op.queue_job(**inputs)

            try:
                op.save_result(
                job_id=job_id, aliases={'tokens_array': 'preprocessed_tokens'}
            )
            except Exception:
                pass
        
        table_value = kiara.data_registry.get_value('alias:preprocessed_tokens')

        if table_value:
            tokens_array = table_value.data
            series = tokens_array.arrow_array.to_pandas()
            st.dataframe(series)


        # tokens = self.get_step_outputs("tokenization")["tokens_array"]

        # preview = None
        # if tokens.item_is_valid():
        #     sample_op = st.kiara.get_operation("sample.array.rows")
        #     sample_token_array = self._cache.get("preprocess_sample_array", None)
        #     if not sample_token_array:
        #         sample_token_array = sample_op.run(array=tokens, sample_size=7).get_value_obj("sampled_value")
        #         self._cache["preprocess_sample_array"] = sample_token_array
        #     preview_op = st.kiara.get_operation("playground.markus.topic_modeling.preprocess")
        #     inputs = {
        #         "to_lowercase": lowercase,
        #         "remove_alphanumeric": remove_alphanumeric,
        #         "remove_non_alpha": remove_non_alpha,
        #         "remove_all_numeric": remove_all_numeric,
        #         "remove_short_tokens": shorttokens,
        #         "remove_stopwords": stopword_list
        #     }
        #     preview = preview_op.run(token_lists=sample_token_array, **inputs)
        # preview_pre_processing = st.checkbox("Test settings on a sample", value=True)
        # if preview_pre_processing and preview:
        #     st.dataframe(preview.get_value_data("preprocessed_token_lists").to_pandas())
        # elif preview_pre_processing:
        #     st.write("No data (yet).")

        # confirmation = st.button("Confirm")

        # if confirmation:

        #     step_inputs = {
        #         "to_lowercase": lowercase,
        #         "remove_alphanumeric": remove_alphanumeric,
        #         "remove_non_alpha": remove_non_alpha,
        #         "remove_all_numeric": remove_all_numeric,
        #         "remove_short_tokens": shorttokens,
        #         "remove_stopwords": stopword_list
        #     }
        #     with st.spinner("Pre-processing texts..."):
        #         self.set_pipeline_inputs(inputs=step_inputs)

        #         print("PROCESSING STEP: 'text_pre_processing'")
        #         preprocess_result = self.process_step("text_pre_processing")

        #     if preprocess_result != "Success":
        #         st.error(preprocess_result)

        # # retrieve the actual table value
        # preprocessed_table_value = self.get_step_outputs("text_pre_processing").get_value_obj(
        #     "preprocessed_token_lists"
        # )

        # if preprocessed_table_value.item_is_valid():
        #     # if the output exists, we write it as a pandas Series (since streamlit supports that natively)
        #     df = preprocessed_table_value.get_value_data().to_pandas()
        #     preview= st.checkbox("Preview results", value=True)
        #     if preview:
        #         st.dataframe(df.head(50))
        # else:
        #     st.write("No result")






    # else:
    #     stopword_list = []
    # stopword_expander = st.expander("Selected stopwords")
    # if stopword_list:
    #     stopword_expander.dataframe(stopword_list)
    # else:
    #     stopword_expander.write("*No stopwords (yet).*")




# -*- coding: utf-8 -*-

import streamlit as st

# Custom imports
from multipage import MultiPage
from pages import (
    data_onboarding,
    tokenization,
    text_preprocessing,
    lda
)

app = MultiPage()


# Add all your application here
app.add_page('1. Data Onboarding', data_onboarding.app)
app.add_page('2. Tokenization', tokenization.app)
app.add_page('3. Remove stop words', text_preprocessing.app)
app.add_page('4. LDA', lda.app)

# The main app
app.run()
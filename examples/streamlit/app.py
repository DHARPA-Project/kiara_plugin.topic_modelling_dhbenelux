# -*- coding: utf-8 -*-

import streamlit as st

# Custom imports
from multipage import MultiPage
from pages import (
    data_onboarding,
    text_preprocessing
)

app = MultiPage()


# Add all your application here
app.add_page('1. Data Onboarding', data_onboarding.app)
app.add_page('2. Text Pre-processing', text_preprocessing.app)

# The main app
app.run()
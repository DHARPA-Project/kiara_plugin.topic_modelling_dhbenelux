# -*- coding: utf-8 -*-

import streamlit as st
from kiara import Kiara

# Custom imports
from multipage import MultiPage
from pages import (
    data_onboarding
)

app = MultiPage()


# Add all your application here
app.add_page('1. Data Onboarding', data_onboarding.app)

# The main app
app.run()
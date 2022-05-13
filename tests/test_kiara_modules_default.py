#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara_plugin.topic_modelling_dhbenelux` package."""

import kiara_plugin.topic_modelling_dhbenelux
import pytest  # noqa


def test_assert():

    assert kiara_plugin.topic_modelling_dhbenelux.get_version() is not None

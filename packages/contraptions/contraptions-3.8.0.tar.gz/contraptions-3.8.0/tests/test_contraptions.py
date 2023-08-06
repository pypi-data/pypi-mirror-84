#!/usr/bin/env python

"""Tests for `contraptions` package."""

# import pytest


from contraptions import contraptions

# @pytest.fixture
# def response():


def test_content():
    assert contraptions.add(1, 2) == 3
    assert contraptions.subtract(2, 1) == 1

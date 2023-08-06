#!/usr/bin/env python

"""Tests for `contraptions` package."""

# import pytest


from contraptions import add, subtract

# @pytest.fixture
# def response():


def test_content():
    assert add(1, 2) == 3
    assert subtract(2, 1) == 1

import pytest


def test_imports():
    from project_name.handler import MyHandler
    from project_name.app import MyApp

    assert MyApp
    assert MyHandler

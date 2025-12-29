from application.menu_options import menu_options


def test_menu_options_structure():
    assert isinstance(menu_options, list)
    assert len(menu_options) > 0

    for option in menu_options:
        assert isinstance(option, dict)
        assert set(option.keys()) == {"name", "url"}
        assert isinstance(option["name"], str)
        assert isinstance(option["url"], str)

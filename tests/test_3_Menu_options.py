def test_menu_options():
    # Definiera menyalternativ
    menu_options = [
        {"name": "Home", "url": "/"},
        {"name": "Option 1", "url": "/option1"},
        {"name": "Option 2", "url": "/option2"},
        {"name": "Option 3", "url": "/option3"},
    ]

    # Kontrollera om varje element i listan är en dictionary med nycklarna 'name' och 'url'
    for option in menu_options:
        assert isinstance(option, dict)
        assert 'name' in option
        assert 'url' in option



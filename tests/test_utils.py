from core.utils import split_to_words

def test_split_to_words_snake_case():
    assert split_to_words("foo_bar_baz") == ["foo", "bar", "baz"]

def test_split_to_words_kebab_case():
    assert split_to_words("foo-bar-baz") == ["foo", "bar", "baz"]

def test_split_to_words_space_separated():
    assert split_to_words("foo bar baz") == ["foo", "bar", "baz"]

def test_split_to_words_camel_case():
    assert split_to_words("fooBarBaz") == ["foo", "Bar", "Baz"]

def test_split_to_words_pascal_case():
    assert split_to_words("FooBarBaz") == ["Foo", "Bar", "Baz"]

def test_split_to_words_acronym_and_word():
    assert split_to_words("HTTPServer") == ["HTTP", "Server"]
    assert split_to_words("parseXMLString") == ["parse", "XML", "String"]
    assert split_to_words("SQLAlchemy") == ["SQL", "Alchemy"]
    assert split_to_words("userID") == ["user", "ID"]

def test_split_to_words_single_word():
    assert split_to_words("foo") == ["foo"]

def test_split_to_words_empty_string():
    assert split_to_words("") == []

def test_split_to_words_only_separators():
    assert split_to_words("___") == []
    assert split_to_words("---") == []
    assert split_to_words("   ") == []

def test_split_to_words_mixed_separators():
    assert split_to_words("foo_bar-baz qux") == ["foo", "bar", "baz", "qux"]

def test_split_to_words_edge_cases():
    assert split_to_words("_fooBar") == ["foo", "Bar"]
    assert split_to_words("fooBar_") == ["foo", "Bar"]
    assert split_to_words("FOOBar") == ["FOO", "Bar"]
    assert split_to_words("fooBARBaz") == ["foo", "BAR", "Baz"]
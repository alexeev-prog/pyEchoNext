from pyechonext.utils.slugger import SlugGenerator


def test_slugs():
    slugger = SlugGenerator()

    assert slugger.generate_slug("Привет мир") == "privet-mir"
    assert slugger.generate_slug("PRI VET WORLD") == "pri-vet-world"

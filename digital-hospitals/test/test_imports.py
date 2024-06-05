import pytest

def test_good_imports():
    from digital_hospitals import bim
    from digital_hospitals import example
    from digital_hospitals import common
    print(bim)
    print(example)
    print(common)

    from digital_hospitals.dev import frontpage
    from digital_hospitals.dev import specs
    print(frontpage)
    print(specs)

def test_bad_import():
    with pytest.raises(ImportError):
        from digital_hospitals import not_exists

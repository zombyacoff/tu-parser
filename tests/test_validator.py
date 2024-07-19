import unittest

from tuparser.constants import LAUNCH_TIME
from tuparser.exceptions import InvalidConfigurationError
from tuparser.validator import (
    boolean,
    ensure_valide_data,
    offset,
    output_file,
    published_years,
    titles,
    validate,
)


class TestValidator(unittest.TestCase):
    def test_titles(self):
        self.assertTrue(titles(["a", "b", "c"]))

        self.assertFalse(titles(["a", "b", None]))
        self.assertFalse(titles("not a list"))

    def test_boolean(self):
        self.assertTrue(boolean(True))
        self.assertTrue(boolean(False))

        self.assertFalse(boolean("not a boolean"))
        self.assertFalse(boolean(123))

    def test_offset(self):
        self.assertTrue(offset(1))
        self.assertTrue(offset(250))

        self.assertFalse(offset(0))
        self.assertFalse(offset(251))
        self.assertFalse(offset("not an integer"))

    def test_output_file(self):
        self.assertTrue(output_file(None))
        self.assertTrue(output_file([{"a": {}}, "b", "c"]))

        self.assertFalse(output_file("not a list"))
        self.assertFalse(output_file([{"a": "not a dict"}, "b", "c"]))
        self.assertFalse(output_file([{"a": {"key": "not_empty"}}, "b", "c"]))
        self.assertFalse(output_file([{"a": {}}, 1, "c"]))
        self.assertFalse(output_file([{"a": {}}, "b", "c", "d"]))

    def test_published_years(self):
        self.assertTrue(published_years(None))
        self.assertTrue(published_years([2020, 2021, LAUNCH_TIME.year]))

        self.assertFalse(published_years("not a list"))
        self.assertFalse(published_years([-1, LAUNCH_TIME.year]))
        self.assertFalse(published_years([2020, "not an integer", 2022]))
        self.assertFalse(published_years([2020, LAUNCH_TIME.year + 1]))

    def test_ensure_valide_data(self):
        with self.assertRaises(InvalidConfigurationError):
            ensure_valide_data(value=0, condition=offset, exception_message="Error: {}")
        ensure_valide_data(value=1, condition=offset, exception_message="Error: {}")

    def test_validate(self):
        valid_config = {
            "titles": ["title1", "title2"],
            "messages": True,
            "offset": 100,
            "output_file": None,
            "progress_bar": False,
            "published_years": [2000, 2020],
        }
        self.assertEqual(validate(valid_config), valid_config)

        invalid_config = {
            "titles": [None, "title2"],
            "messages": "True",
            "offset": 251,
            "output_file": [{"key": "value"}, "path1"],
            "progress_bar": "False",
            "published_years": [-1, 2020],
        }
        with self.assertRaises(InvalidConfigurationError):
            validate(invalid_config)


if __name__ == "__main__":
    unittest.main()

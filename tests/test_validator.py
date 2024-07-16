import unittest

from tuparser.constants import LAUNCH_TIME
from tuparser.exceptions import ValidatorException
from tuparser.validator import boolean, ensure_valide_data, offset, output_file, release_years, titles, validate


class TestValidators(unittest.TestCase):
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
        self.assertTrue(output_file([]))
        self.assertTrue(output_file([{"a": {}}, "b", "c"]))

        self.assertFalse(output_file("not a list"))
        self.assertFalse(output_file([{"a": "not a dict"}, "b", "c"]))
        self.assertFalse(output_file([{"a": {"key": "not_empty"}}, "b", "c"]))
        self.assertFalse(output_file([{"a": {}}, 1, "c"]))

    def test_release_years(self):
        self.assertTrue(release_years([]))
        self.assertTrue(release_years([2020, 2021, 2022]))

        self.assertFalse(release_years("not a list"))
        self.assertFalse(release_years([2020, "not an integer", 2022]))
        self.assertFalse(release_years([2020, LAUNCH_TIME.year + 1]))

    def test_ensure_valide_data(self):
        with self.assertRaises(ValidatorException):
            ensure_valide_data(value="invalid value", validate_func=boolean, exception_message="invalid value: {}")

    def test_validate(self):
        with self.assertRaises(ValidatorException):
            validate({
                "titles": "not a list",
                "messages": True,
                "offset": 2,
                "output_file": [],
                "progress_bar": True,
                "release_years": [2020, 2021],
            })


if __name__ == "__main__":
    unittest.main()

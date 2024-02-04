"""
Unit Tests for Web Scraper Module
2024-01-20
by ajps

Test name matching
"""

# resolve importing project Python files
import sys, os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, project_root)

# resolve finding filenames in tests dir

# import modules
import unittest
import test.scrapedNames
import test.gradeDataNames
import context
import nameMatch

expand_prints = False


class TestAbnormalNames(unittest.TestCase):
    """
    Test for abnormal names in sample data.
    These are provided to improve name matching by analyzing sample data.
    These tests do not test program logic and will always pass.
    """

    def test_empty_names_gradedata(self):
        """
        Check for empty string names in gradedata sample.
        """
        names = test.gradeDataNames.gradedata_names_sample
        empty_names = {}
        for i in range(len(names)):
            if names[i] == "":
                empty_names[i] = names[i]
        # print test results
        if len(empty_names.keys()) > 0:
            if not expand_prints:
                empty_names = len(empty_names)
            print(f"gradedata empty names: {empty_names}")
        else:
            print("No empty names in gradedata sample")

    def test_non_alphabetic_names_gradedata(self):
        """
        Check for names without alphabetic characters in gradedata sample.
        """
        names = test.gradeDataNames.gradedata_names_sample
        non_alpha_names = {}
        for i in range(len(names)):
            for char in names[i]:
                if char.isalpha():
                    break
                non_alpha_names[i] = names[i]
        # print test results
        if len(non_alpha_names.keys()) > 0:
            if not expand_prints:
                non_alpha_names = len(non_alpha_names)
            print(f"gradedata non-alphabetic names: {non_alpha_names}")
        else:
            print("No non-alphabetic names in gradedata sample")

    def test_no_last_name_gradedata(self):
        """
        Check for names with no last name or which only provide last initial in gradedata sample.
        """
        names = test.gradeDataNames.gradedata_names_sample
        no_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            last_name = "".join(char for char in last_name if char.isalpha())
            if len(last_name) <= 1:
                no_last_names[i] = names[i]
        # print test results
        if len(no_last_names) > 0:
            if not expand_prints:
                no_last_names = len(no_last_names)
            print(f"gradedata no last names: {no_last_names}")
        else:
            print("No missing last names in gradedata sample")

    def test_double_last_name_gradedata(self):
        """
        Check for double last names separated by space in gradedata sample.
        """
        names = test.gradeDataNames.gradedata_names_sample
        double_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            if " " in last_name:
                double_last_names[i] = names[i]
        # print test results
        if len(double_last_names) > 0:
            if not expand_prints:
                double_last_names = len(double_last_names)
            print(f"gradedata double last names: {double_last_names}")
        else:
            print("No double last names in gradedata sample")

    def test_hyphenated_last_name_gradedata(self):
        """
        Check for double last names separated by hyphen in gradedata sample.
        """
        names = test.gradeDataNames.gradedata_names_sample
        hyphen_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            if "-" in last_name:
                hyphen_last_names[i] = names[i]
        # print test results
        if len(hyphen_last_names) > 0:
            if not expand_prints:
                hyphen_last_names = len(hyphen_last_names)
            print(f"gradedata hyphenated last names: {hyphen_last_names}")
        else:
            print("No hyphenated last names in gradedata sample")

    def test_wordy_names_scraped(self):
        """
        Check for names with more than 3 words (or initials) in scraped names sample.
        Hyphenated names treated as one word.
        """
        names = test.scrapedNames.scraped_names_sample
        wordy_names = {}
        for i in range(len(names)):
            name_list = names[i].split(" ")
            if len(name_list) >= 4:
                wordy_names[i] = names[i]
        # print test results
        if len(wordy_names) > 0:
            if not expand_prints:
                wordy_names = len(wordy_names)
            print(f"scraped wordy names: {wordy_names}")
        else:
            print("No wordy names in scraped sample")


class TestNameMatch(unittest.TestCase):
    """
    Test for the efficacy of the functions dedicated to matching names.
    """

    def setUp(self):
        """
        Rename the data/faculty_names.py file to preserve it during testing.
        It will be put back into place afterward.
        """
        self.replace = False
        if os.path.exists("./data/faculty_names.py"):
            self.replace = True
            os.rename("./data/faculty_names.py", "./data/tmp_faculty_names.py")

    def tearDown(self):
        """
        Remove the faculty_names.py generated during these unit tests,
        Replace it with the version available prior to testing
        """
        try:
            os.remove("./data/faculty_names.py")
        except:
            pass
        if self.replace:
            os.rename("./data/tmp_faculty_names.py", "./data/faculty_names.py")

    def test_match_simple(self):
        """
        Test the full name matching process with an example name from gradedata sample.
        There is only one logical match in the scraped names sample.
        """
        example_name = "Johnson, Eric Allen"
        # create dict from scraped names sample
        nameMatch.scraped_names_to_dict(test.scrapedNames.scraped_names_sample)
        # try to match name
        result = nameMatch.match_name(example_name)
        self.assertEqual(["Eric A. Johnson"], result)

    def test_match_similar_names(self):
        """
        Test the full name matching process with an example name.
        A contrived scraped names list is given with multiple matching last names.
        """
        example_name = "Doe, Jon A."
        # create dict from this list of contrived names
        scraped_names = ["Jon A. Doe", "John B. Doe", "John C. Smith"]
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name)
        self.assertEqual(["Jon A. Doe"], result)

    def test_match_same_last_name(self):
        """
        Test the full name matching with an example name.
        This uses the sample scraped names, containing entries of same last name.

        The scraped names contains two names of last name Phillips:
        "Patrick C. Phillips"
        "N. Christopher Phillips"
        """
        example_name = "Phillips, N. Christopher"
        # create scraped names dict
        nameMatch.scraped_names_to_dict(test.scrapedNames.scraped_names_sample)
        # try to match name
        result = nameMatch.match_name(example_name)
        self.assertEqual(["N. Christopher Phillips"], result)

    def test_match_wordy_last_name(self):
        """
        Test the full name matching process with an example name.
        The example name has 3 last names.
        """
        example_name = "Chioma Tufayl Regin, Jocelyn Rigantona"
        # create dict from this list of contrived names
        scraped_names = ["Jocelyn Rigantona China Tufayl Regin",
                         "Jocelyn Rigantona Chioma Tulip Regin",
                         "Jocelyn Rigantona Chioma Tufayl Regent",
                         "Jocelyn Rigantona Chioma Tufayl Regin"]
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name)
        self.assertEqual(["Jocelyn Rigantona Chioma Tufayl Regin"], result)

    def test_match_wordy_given_name(self):
        """
        Test the full name matching process with an example name.
        The example name has 3 given names, including one initial.
        The example scraped names will sometimes use initials or extra given names.
        """
        example_name = "Sargon, Jeanne Ita A. Kenina"
        # creat a dict from this list of contrived names
        scraped_names = ["Jeanne Ita Anatu Kenina Sargon",
                         "J. Ita Anatu Kenina Sargon",  # first initial
                         "Jeanne Ita Anatu Kenina Neva Sargon",  # extra given name
                         "Jeanne Ita Antas K. Sargon",  # middle initial
                         "Joanna Ita Anatu Kenina Sargon",  # wrong
                         "Jeanne Ita Anatu Keller Sargon"]  # wrong
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name)
        expected = ["Jeanne Ita Anatu Kenina Sargon",
                    "J. Ita Anatu Kenina Sargon",
                    "Jeanne Ita Anatu Kenina Neva Sargon",
                    "Jeanne Ita Antas K. Sargon"]
        self.assertEqual(expected, result)

    def test_match_whitespaces(self):
        """
        Test the full name matching process when extra white spaces are added to both
        the input name and the available scraped names.
        """
        example_name = " Smith, John A. "
        # create a dict from sample scraped names
        scraped_names = ["  John A. Smith "]
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name)
        self.assertEqual(result, ["John A. Smith"])


class TestNameMatchParts(unittest.TestCase):
    """
    Similar to the TestNameMatch class, but this one specifically tests
    the hidden _match_last_name() and _match_nth_name() functions.
    """

    def setUp(self):
        """
        Rename the data/faculty_names.py file to preserve it during testing.
        It will be put back into place afterward.
        """
        self.replace = False
        if os.path.exists("./data/faculty_names.py"):
            self.replace = True
            os.rename("./data/faculty_names.py", "./data/tmp_faculty_names.py")

    def tearDown(self):
        """
        Remove the faculty_names.py generated during these unit tests,
        Replace it with the version available prior to testing
        """
        try:
            os.remove("./data/faculty_names.py")
        except:
            pass
        if self.replace:
            os.rename("./data/tmp_faculty_names.py", "./data/faculty_names.py")

    def test_match_last_simple(self):
        """
        Test correct matching of an example last name.
        Uses sample scraped names in test/scrapedNames.py
        """
        example_name = "Cresko, William A."
        # create dict from scraped names example
        nameMatch.scraped_names_to_dict(test.scrapedNames.scraped_names_sample)
        # match last name
        matches = nameMatch._match_last_name(example_name)
        self.assertEqual(matches, ["William A. Cresko"])

    def test_match_last_similar_names(self):
        """
        Try to match last name when some options are substrings of the last name.
        """
        example_name = "Matias, Praskovya"
        # create dict from scraped name example
        scraped_names = ["Praskovya L. Matias", "Praskovya L. Matia"]
        nameMatch.scraped_names_to_dict(scraped_names)
        # match last name
        matches = nameMatch._match_last_name(example_name)
        self.assertEqual(matches, ["Praskovya L. Matias"])

    def test_match_last_multiple_last_names(self):
        """
        Try to match last name with multiple last names.
        """
        example_name = "Jeremy Manel Deoiridh, Amalia"
        # create dict from sample
        scraped_names = ["Amalia Jeremiah Manel Deoiridh",
                         "Amalia Jeremy Manuel Deoiridh",
                         "Amalia Jeremy Manel Dawson",
                         "Amalia Jeremy Manel Deoiridh"]
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch._match_last_name(example_name)
        self.assertEqual(["Amalia Jeremy Manel Deoiridh"], result)

    def test_match_last_whitespaces(self):
        """
        Test matching last name when extra white spaces are added to both
        the input name and the available scraped names.
        """
        example_name = "  Smith  ,  John A.  "
        # create a dict from sample scraped names
        scraped_names = [" John A. Smith "]
        nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch._match_last_name(example_name)
        self.assertEqual(["John A. Smith"], result)

    def test_match_last_same_last_name(self):
        """
        Test the last name matching with an example name.
        This uses the sample scraped names, containing entries of same last name.

        The scraped names contains two names of last name Phillips:
        "Patrick C. Phillips"
        "N. Christopher Phillips"
        """
        example_name = "Phillips, N. Christopher"
        # create scraped names dict
        nameMatch.scraped_names_to_dict(test.scrapedNames.scraped_names_sample)
        # try to match name
        result = nameMatch._match_last_name(example_name)
        self.assertEqual(["Patrick C. Phillips", "N. Christopher Phillips"], result)

    def test_match_nth_same_last_name(self):
        """
        Test the nth (first, middle) name matching with an example name.
        This uses the sample scraped names, containing entries of same last name.

        The scraped names contains two names of last name Phillips:
        "Patrick C. Phillips"
        "N. Christopher Phillips"
        """
        example_name = "Phillips, N. Christopher"
        candidates = ["Patrick C. Phillips", "N. Christopher Phillips"]
        # there are 2 given names
        for n in range(2):
            candidates = nameMatch._match_nth_name(example_name, n, candidates)
        self.assertEqual(["N. Christopher Phillips"], candidates)

    def test_match_nth_different_num_given_names(self):
        """
        Test the nth (first, middle) name matching when the candidates have
        different numbers of given (first, middle) names.
        """
        example_name = "Ernesto, Giuseppe Frediano L. Ettore"
        candidates = ["Giuseppe Frediano L. Ernesto",  # correct, just missing one middle name
                      "Giuseppe Ernesto L. Frediano Ernesto",  # wrong, names out of order
                      "Giuseppe F. L. Ettore Ernesto",  # correct, used an initial
                      "Giuseppe Ernesto",  # correct, just missing all middle names
                      "Giuseppe Frediano L. Etar Ernesto"]  # wrong, wrong name
        # there are 4 given names
        for n in range(4):
            candidates = nameMatch._match_nth_name(example_name, n, candidates)
        self.assertEqual(["Giuseppe Frediano L. Ernesto",
                          "Giuseppe F. L. Ettore Ernesto",
                          "Giuseppe Ernesto"], candidates)


class TestAccessScrapedNames(unittest.TestCase):
    """
    Make sure nameMatch.py correctly writes to and reads from the
    faculty_names.py file, which conrains dict of scraped names.
    """

    def setUp(self):
        """
        Rename the data/faculty_names.py file to preserve it during testing.
        It will be put back into place afterward.
        """
        self.replace = False
        if os.path.exists("./data/faculty_names.py"):
            self.replace = True
            os.rename("./data/faculty_names.py", "./data/tmp_faculty_names.py")

    def tearDown(self):
        """
        Remove the faculty_names.py generated during these unit tests,
        Replace it with the version available prior to testing
        """
        try:
            os.remove("./data/faculty_names.py")
        except:
            pass
        if self.replace:
            os.rename("./data/tmp_faculty_names.py", "./data/faculty_names.py")

    def test_read_write_scraped_names_dict(self):
        """
        Read from, write to, and read from the faculty_names.py dict.
        """
        # write sample dict text to file
        dict_file = open("./data/faculty_names.py", "w")
        dict_string = """faculty_names = {"smith": ["John Smith", "Joe Smith"], "doe": ["John Doe"]}"""
        dict_file.write(dict_string)
        dict_file.close()
        # read the file
        nameMatch._reload_names_dict()
        # check that it was read correctly
        result = nameMatch.match_name("Smith, John")
        self.assertEqual(["John Smith"], result)
        # write a new scraped naems dict to the file
        scraped_names = ["Nicolao Robertina", "Ivan Lauro"]
        nameMatch.scraped_names_to_dict(scraped_names)
        # check that it's only reading the new data for matches
        result = nameMatch.match_name("Smith, John")
        self.assertEqual([], result)
        result = nameMatch.match_name("Lauro, Ivan")
        self.assertEqual(["Ivan Lauro"], result)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "expand":
        # enable expanding information for sample name tests
        expand_prints = True if "expand" in sys.argv else False
        sys.argv.pop(1)

    unittest.main()
else:
    print("Importing unit tests is not recommended (unless using iPython interactive shell)")

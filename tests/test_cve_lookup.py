import unittest
from agent.tools.cve_lookup import CVELookup

class TestCVELookup(unittest.TestCase):

    def setUp(self):
        self.cve_lookup = CVELookup()

    def test_lookup_valid_cve(self):
        result = self.cve_lookup.lookup("CVE-2021-34527")
        self.assertIsNotNone(result)
        self.assertEqual(result['CVE_ID'], "CVE-2021-34527")

    def test_lookup_invalid_cve(self):
        result = self.cve_lookup.lookup("CVE-0000-0000")
        self.assertIsNone(result)

    def test_lookup_empty_cve(self):
        result = self.cve_lookup.lookup("")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
''' Kate Grossman and Matt Stritzel
    May 2019
    API tests for web project '''

import api
import unittest
import psycopg2
import json
import csv
import sys
import flask


class APITests(unittest.TestCase):

    def setUp(self):
       pass

    def tearDown(self):
       pass

    def test_get_cause_from_state(self):
        result = api.get_most_deadly("Illinois")
        self.assertEqual(result, [{"cause": "All causes", "deaths": 1872193}, {"cause": "Heart disease", "deaths": 492338}, {"cause": "Cancer", "deaths": 440324}, {"cause": "Stroke", "deaths": 110313}, {"cause": "CLRD", "deaths": 92821}, {"cause": "Unintentional injuries", "deaths": 77883}, {"cause": "Diabetes", "deaths": 51496}, {"cause": "Alzheimer's disease", "deaths": 50732}, {"cause": "Influenza and pneumonia", "deaths": 46952}, {"cause": "Kidney disease", "deaths": 43358}, {"cause": "Suicide", "deaths": 21118}])


    def test_get_cause_from_state_error(self):
        self.assertRaises(ValueError, api.get_most_deadly, "alska")

    def test_get_state_from_cause(self):
        result = api.get_which_state_has_most_deaths_from_db()
        self.assertEqual(result, [{"deaths": 79114118, "state": "United States"}, {"deaths": 7694563, "state": "California"}, {"deaths": 5512136, "state": "Florida"}, {"deaths": 5192340, "state": "Texas"}, {"deaths": 4889235, "state": "New York"}, {"deaths": 4069680, "state": "Pennsylvania"}, {"deaths": 3501123, "state": "Ohio"}, {"deaths": 3299528, "state": "Illinois"}, {"deaths": 2839241, "state": "Michigan"}, {"deaths": 2447232, "state": "North Carolina"}, {"deaths": 2267451, "state": "New Jersey"}, {"deaths": 2182235, "state": "Georgia"}, {"deaths": 1889824, "state": "Tennessee"}, {"deaths": 1871444, "state": "Virginia"}, {"deaths": 1821157, "state": "Indiana"}, {"deaths": 1796910, "state": "Missouri"}, {"deaths": 1712812, "state": "Massachusetts"}, {"deaths": 1535878, "state": "Washington"}, {"deaths": 1515656, "state": "Wisconsin"}, {"deaths": 1510931, "state": "Alabama"}, {"deaths": 1471757, "state": "Arizona"}, {"deaths": 1384915, "state": "Maryland"}, {"deaths": 1340426, "state": "Kentucky"}, {"deaths": 1329242, "state": "Louisiana"}, {"deaths": 1279233, "state": "South Carolina"}, {"deaths": 1212223, "state": "Minnesota"}, {"deaths": 1171193, "state": "Oklahoma"}, {"deaths": 1001266, "state": "Oregon"}, {"deaths": 973746, "state": "Colorado"}, {"deaths": 935091, "state": "Mississippi"}, {"deaths": 929634, "state": "Arkansas"}, {"deaths": 927612, "state": "Connecticut"}, {"deaths": 901497, "state": "Iowa"}, {"deaths": 785398, "state": "Kansas"}, {"deaths": 681657, "state": "West Virginia"}, {"deaths": 609031, "state": "Nevada"}, {"deaths": 489205, "state": "New Mexico"}, {"deaths": 484109, "state": "Nebraska"}, {"deaths": 441702, "state": "Utah"}, {"deaths": 407962, "state": "Maine"}, {"deaths": 351070, "state": "Idaho"}, {"deaths": 332283, "state": "New Hampshire"}, {"deaths": 310105, "state": "Rhode Island"}, {"deaths": 300668, "state": "Hawaii"}, {"deaths": 277255, "state": "Montana"}, {"deaths": 238935, "state": "Delaware"}, {"deaths": 230111, "state": "South Dakota"}, {"deaths": 191032, "state": "North Dakota"}, {"deaths": 168797, "state": "Vermont"}, {"deaths": 160361, "state": "District of Columbia"}, {"deaths": 136865, "state": "Wyoming"}, {"deaths": 110361, "state": "Alaska"}])


    def test_get_trend_of_deaths(self):
        result = api.get_national_trend("Suicide")
        self.assertEqual(result, [{"year": 1999, "deaths": 58398}, {"year": 2000, "deaths": 58700}, {"year": 2001, "deaths": 61244}, {"year": 2002, "deaths": 63310}, {"year": 2003, "deaths": 62968}, {"year": 2004, "deaths": 64878}, {"year": 2005, "deaths": 65274}, {"year": 2006, "deaths": 66600}, {"year": 2007, "deaths": 69196}, {"year": 2008, "deaths": 72070}, {"year": 2009, "deaths": 73818}, {"year": 2010, "deaths": 76728}, {"year": 2011, "deaths": 79036}, {"year": 2012, "deaths": 81200}, {"year": 2013, "deaths": 82298}, {"year": 2014, "deaths": 85652}, {"year": 2015, "deaths": 88386}, {"year": 2016, "deaths": 89930}])

    def test_wrong_cause_input(self):
        self.assertRaises(ValueError, api.get_national_trend, "cough")

    def test_get_table(self):
        result = api.get_table("Suicide", "Illinois", 2000, 2010)
        self.assertEqual(result, [{"deaths": 1003, "year": 2000}, {"deaths": 1139, "year": 2001}, {"deaths": 1145, "year": 2002}, {"deaths": 1011, "year": 2003}, {"deaths": 1028, "year": 2004}, {"deaths": 1086, "year": 2005}, {"deaths": 1010, "year": 2006}, {"deaths": 1108, "year": 2007}, {"deaths": 1198, "year": 2008}, {"deaths": 1177, "year": 2009}, {"deaths": 1178, "year": 2010}])

    def test_end_year_before_start_year(self):
        self.assertRaises(ValueError, api.get_table, "Suicide", "Illinois", 2003, 2000)

    def test_incorrect_cause_name_main(self):
        self.assertRaises(ValueError, api.get_table, "Sde", "Illinois", 2000, 2003)

    def test_incorrect_state_name_main(self):
        self.assertRaises(ValueError, api.get_table, "Suicide", "ILL", 2000, 2003)

    def test_incorrect_start_year_main(self):
        self.assertRaises(ValueError, api.get_table, "Sde", "Illinois", 20, 2003)

    def test_incorrect_start_year_main(self):
        self.assertRaises(ValueError, api.get_table, "Sde", "Illinois", 2000, 20)

if __name__ == '__main__':
    unittest.main()

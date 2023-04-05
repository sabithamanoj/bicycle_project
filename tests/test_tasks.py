import unittest
import pandas as pd

from classes import annotation

# test data was created by taking first 10000 instances from anonymized data

class MyTestCase(unittest.TestCase):
    def test_get_num_of_annotators(self):
        test_data = pd.read_excel('./test_data.xlsx')
        crowd_one = annotation.AnnotationCrowd(test_data)
        self.assertEqual(crowd_one.get_num_of_annotators(), 22)

    def test_get_amount_of_results(self):
        test_data = pd.read_excel('./test_data.xlsx')
        crowd_one = annotation.AnnotationCrowd(test_data)
        self.assertEqual(len(crowd_one.get_amount_of_results()), 22)

    def test_get_highly_disagree_ids(self):
        test_data = pd.read_excel('./test_data.xlsx')
        crowd_one = annotation.AnnotationCrowd(test_data)
        self.assertEqual(len(crowd_one.get_highly_disagree_ids()), 7)

    def test_get_cant_solve_instances(self):
        test_data = pd.read_excel('./test_data.xlsx')
        crowd_one = annotation.AnnotationCrowd(test_data)
        ans = crowd_one.get_cant_solve_instances()
        self.assertEqual(len(ans), 3)


if __name__ == '__main__':
    unittest.main()

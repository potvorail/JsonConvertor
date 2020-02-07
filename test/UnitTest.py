import io
import unittest
import JsonEncoder

from pathlib import Path


class JsonEncoderTestCase(unittest.TestCase):

    @staticmethod
    def compare_json(orig, expected):
        builder = JsonEncoder.ClumpinessTreeBuilder(Path(orig))
        builder.build_tree('tissue')
        json_to_test = io.StringIO()
        builder.dump_tree(json_to_test)
        with open(Path(expected)) as f:
            json_expected = f.read()
#        print("New --> " + json_to_test.getvalue())
#        print("Old --> " + str(json_expected))
        result = json_to_test.getvalue() == str(json_expected)
        json_to_test.close()
        return result

    def test_converter1(self):
        result = JsonEncoderTestCase.compare_json('original_final_1.JSON', 'expected_original_final_1.JSON')
        self.assertTrue(result, "original_final_1.JSON is not equal to expected_original_final_1.JSON")

    def test_converter21(self):
        result = JsonEncoderTestCase.compare_json('clone_957_sykesLiz2019.JSON', 'expected_clone_957_sykesLiz2019.JSON')
        self.assertTrue(result, "clone_957_sykesLiz2019.JSON is not equal to expected_clone_957_sykesLiz2019.JSON")


if __name__ == '__main__':
    unittest.main()

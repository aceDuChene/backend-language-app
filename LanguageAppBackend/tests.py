import unittest
from text_comparison import TextComparison

def retrieveAnswer(str1, str2):
    comparison = TextComparison(str1, str2)
    return comparison.check_answer()

class TestTextComparison(unittest.TestCase):

    # Cases that are expected to be correct
    def test_correct_1(self):
        answer = retrieveAnswer("My name is Gabey.", "My name is Gabey.")
        self.assertEqual(answer, True)

    # Cases that are expected to be incorrect
    def test_incorrect_1(self):
        answer = retrieveAnswer("I want to drink beer.", "I want to drink tea.")
        self.assertEqual(answer, False)
    
    # Cases that could mistakenly be incorrect
    def test_false_neg_1(self):
        answer = retrieveAnswer("I like apples", "I like apples.")
        self.assertEqual(answer, True)

    def test_false_neg_2(self):
        answer = retrieveAnswer("I like apples and bananas.", "I like bananas and apples.")
        self.assertEqual(answer, True)

    def test_false_neg_3(self):
        answer = retrieveAnswer("I believe in Santa Claus.", "I beleive in Santa Claus.")
        self.assertEqual(answer, True)

    # Cases that could mistakenly be correct
    # This test fails, but that may be unavoidable
    def test_false_pos_1(self):
        answer = retrieveAnswer("Yesterday I received a present.", "Yesterday I receive a present.")
        self.assertEqual(answer, False)

    def test_false_pos_2(self):
        answer = retrieveAnswer("I like Daniel.", "Daniel likes me")
        self.assertEqual(answer, False)

    def test_false_pos_3(self):
        answer = retrieveAnswer("The girl likes cats.", "Cats like the girl.")
        self.assertEqual(answer, False)

    # This test fails, but that may be unavoidable
    def test_false_pos_4(self):
        answer = retrieveAnswer("I have a pen.", "I have a pin.")
        self.assertEqual(answer, False)

if __name__ == "__main__":
    unittest.main()
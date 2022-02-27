from fuzzywuzzy import fuzz
from pyxdameraulevenshtein import damerau_levenshtein_distance


class TextComparison:
    def __init__(self, user_answer, correct_answer):
        self.user_answer = self.remove_puncuation(user_answer)
        self.correct_answer = self.remove_puncuation(correct_answer)

    def remove_puncuation(self, sentence):
        puncuation = """!()-[]{};:'",<>./?@#$%^&*_~"""
        for char in puncuation:
            sentence = sentence.replace(char, "")

        return sentence

    def check_answer(self):
        # Check basic Levenshtein Distance
        score = fuzz.ratio(self.correct_answer, self.user_answer)
        if score >= 98:
            return True

        # Transpositions are counted as two edits in Levenshtein Distance. Use Damerau-Levenshtein
        # distance to check if difference is a single transposition
        if score >= 96:
            transposition_score = damerau_levenshtein_distance(
                self.correct_answer, self.user_answer
            )
            if transposition_score <= 1:
                return True

        # Check if string contains the same words in different orders
        any_order_score = fuzz.token_sort_ratio(self.correct_answer, self.user_answer)
        if any_order_score >= 99:
            return True

        return False

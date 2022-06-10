import codecs

half_space = '‌'


class DefinedWordsModification:
    def __init__(self):

        self.persian_words = {x.strip() for x in codecs.open('./sources/persion-words.txt', 'rU', 'utf-8').readlines()}
        self.prefixes = {x.strip() for x in codecs.open('./sources/prefixes.txt', 'rU', 'utf-8').readlines()}
        self.suffixes = {x.strip() for x in codecs.open('./sources/suffixes.txt', 'rU', 'utf-8').readlines()}

    def check_for_concatenation_possibility(self, word1, word2):
        new_word_half_space = word1 + half_space + word2

        if self.persian_words.__contains__(new_word_half_space):
            return new_word_half_space

        new_word_concatenated = word1 + word2

        if not self.persian_words.__contains__(word1) or not self.persian_words.__contains__(word2):
            if self.prefixes.__contains__(word1) or self.suffixes.__contains__(word2):
                return new_word_concatenated

        return None

    def correct_bad_half_spaces_of_word(self, word):
        parts = word.split(half_space)
        if len(parts) == 1:
            return [word]
        result = [parts[0]]
        for part in parts[1:]:
            new_word_half_space = result[-1] + half_space + part
            new_word_concatenated = result[-1] + part
            if self.persian_words.__contains__(new_word_half_space):
                result[-1] = new_word_half_space
            elif self.persian_words.__contains__(new_word_concatenated):
                result[-1] = new_word_concatenated
            else:
                result.append(part)
        return result

    def correct_bad_single_words(self, word):
        if len(word) > 1 and word.startswith('ب'):
            if self.persian_words.__contains__(word[1:]):
                return ['به', word[1:]]
        return [word]

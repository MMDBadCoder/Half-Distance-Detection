half_space = '‌'


class RulesModification:

    def __init__(self):
        self.concatenation_modifications = [
            self.__modify_ha_and_haye_and_hayi,
            self.__modify_mi,
            self.__modify_tar_tarin,
            self.__modify_ye,
            self.__modify_short_verbs
        ]

        self.single_word_correction = [
            self.__modify_hamin_haman,
            self.__modify_hich,
            self.__modify_che,
            self.__modify_last_hamze
        ]

    def correct_bad_formats_of_word(self, word):
        for modification in self.single_word_correction:
            result = modification(word)
            if len(result) == 1:
                word = result[0]
                continue
            else:
                return result
        return [word]

    def check_for_concatenation_possibility(self, word1, word2):
        for modification in self.concatenation_modifications:
            new_word = modification(word1, word2)
            if new_word is not None:
                return new_word
        return None

    def __modify_ha_and_haye_and_hayi(self, word1, word2):
        if word2 == 'ها' or word2 == 'های' or word2 == 'هایی':
            if len(word1) <= 3 and not word1.endswith('ه') and not word1.endswith('ی'):
                return word1 + word2
            else:
                return word1 + half_space + word2

    def __modify_ye(self, word1, word2):
        if word2 == 'ی':
            if word1.endswith('ی'):
                return word1
            else:
                return word1 + half_space + word2

    def __modify_mi(self, word1, word2):
        if word1 == 'می':
            return word1 + half_space + word2

    def __modify_tar_tarin(self, word1, word2):
        if word2 == 'تر' or word2 == 'ترین':
            if len(word1) <= 3:
                return word1 + word2
            else:
                return word1 + half_space + word2

    def __modify_bi(self, word1, word2):
        if word1 == 'بی':
            return word1 + half_space + word2

    def __modify_short_verbs(self, word1, word2):
        if word2 in ['ست', 'اند', 'ام', 'م']:
            return word1 + half_space + word2

    def __modify_hamin_haman(self, word):
        if len(word) > 4 and (word.startswith('همین') or word.startswith('همان')):
            return [word[:4], word[4:]]
        return [word]

    def __modify_hich(self, word):
        if len(word) > 3 and word.startswith('هیچ'):
            return [word[:3], word[3:]]
        return [word]

    def __modify_che(self, word):
        if word in ['چطور', 'چسان', 'چگونه']:
            return ['چه', word[1:]]
        if word in ['آنچه', 'اینچه', 'چنانچه']:
            return [word[:-2], 'چه']
        return [word]

    def __modify_last_hamze(self, word):
        if word.endswith('ۀ'):
            word = word[:-2] + 'ه‌ی'
        return [word]

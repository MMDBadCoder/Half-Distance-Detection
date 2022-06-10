import hazm

from defined_words_modification import DefinedWordsModification
from rules_modification import RulesModification


def replace_underline_by_space(word):
    return word.replace('_', ' ').split(' ')


defined_words_modification = DefinedWordsModification()
rules_modification = RulesModification()

single_word_correction = [
    replace_underline_by_space,
    defined_words_modification.correct_bad_single_words,
    defined_words_modification.correct_bad_half_spaces_of_word,
    rules_modification.correct_bad_formats_of_word,
]


def correct_a_word(word):
    for correction in single_word_correction:
        corrected = correction(word)
        if len(corrected) == 1:
            word = corrected[0]
            continue
        else:
            result = []
            for corrected_item in corrected:
                result += correct_a_word(corrected_item)
            return result
    return [word]


concatenation_possibilities = [
    defined_words_modification.check_for_concatenation_possibility,
    rules_modification.check_for_concatenation_possibility
]


def modify_by_concatenation(words):
    temp_words = words.copy()
    if len(temp_words) <= 1:
        return temp_words
    temp_words.append('$')
    result = []
    index = 0
    while index < len(temp_words) - 1:
        word1 = temp_words[index]
        word2 = temp_words[index + 1]
        new_word = None
        for modification in concatenation_possibilities:
            new_word = modification(word1, word2)
            if new_word is not None:
                break
        if new_word is not None:
            temp_words[index + 1] = new_word
        else:
            result.append(temp_words[index])
        index += 1
    return result


def join_words_of_a_sentence(words):
    sentence = ''
    need_space = False
    for word in words:
        if word in ':)؛.،':
            need_space = False
        if need_space:
            sentence += ' '
        if word in ['(', '[', '{', '«']:
            need_space = False
        else:
            need_space = True
        sentence += word
    return sentence


def get_cleaned_text(lines):
    normalizer = hazm.Normalizer()
    lines = [[normalizer.normalize(y) for y in x] for x in lines]

    sentences_per_line = [hazm.sent_tokenize(' '.join(x)) for x in lines]
    tokens_by_line_by_sents = [[hazm.word_tokenize(sent) for sent in sents_in_line] for sents_in_line in
                               sentences_per_line]

    result = []

    for line in tokens_by_line_by_sents:
        result.append([])
        for sent in line:
            corrected_words = []
            for word in sent:
                corrected_words += correct_a_word(word)
            cleand_words_list = modify_by_concatenation(corrected_words)
            result[-1].append({
                'sentence': join_words_of_a_sentence(cleand_words_list),
                'words': cleand_words_list
            })

    return result


def get_letters(input_text):

    letters = sum(1 for char in input_text if char.isalpha())
    return letters

def get_words(input_text):
    words = sum(1 for char in input_text if char == ' ') + 1
    return words

def get_sentences(input_text):
    sentences = sum(1 for char in input_text if char in '.!?')
    return sentences

def coleman_liau_idx(letters, words, sentences):

    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index

def main():

    input_text = input("Text: ")

    letters = get_letters(input_text)
    words = get_words(input_text)
    sentences = get_sentences(input_text)

    index = coleman_liau_idx(letters, words, sentences)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


main()

function_codes = {
    "\\frac": "~",
    "frac":  "~",
    "\\text": "#",
    "\div": "@",
    "times": "^",
    "$": ""
}


def polish_fractions(raw_frac_string):
    return _reduce(_tokenize(raw_frac_string))


def _tokenize(text):
    result = []
    char_group_symbols = ['{', '}']

    marked_group_chars = ''
    marked_word_chars = ''
    should_mark_word = False
    should_mark_group = False

    # Convert functions in text into corresponding symbols
    for function in function_codes:
        text = text.replace(function, function_codes[function])

    # Loop through each character in the text
    for index, char in enumerate(text):

        # Start capturing group
        if char == "{":
            should_mark_group = True

        # Stop capturing group and append result
        if char == "}":
            should_mark_group = False
            result.append(marked_group_chars)
            marked_group_chars = ""

        # We continue marking
        if char not in char_group_symbols and should_mark_group:
            marked_group_chars = marked_group_chars + char

        # In other cases, check for normal letters
        # Record words, when char is symbol stop recording and keep word
        if char not in char_group_symbols and not should_mark_group:

            # If its alphabet or number, start adding to word
            if char.isdigit() or char.isalpha() or char == '/':
                should_mark_word = True
                marked_word_chars = marked_word_chars + char

            # If its a symbol, stop adding to word
            elif not char.isalpha() and not char.isalpha():
                should_mark_word = False
                marked_word_chars = marked_word_chars + char
                result.append(marked_word_chars)
                marked_word_chars = ""

        # At the end of the text, append result
        if index == len(text) - 1:
            if should_mark_word:
                result.append(marked_word_chars)

    # Filter out unnecessary symbols like [ \\ and " " and "" ]
    refined_result = []
    for char in result:
        if char not in ["", " ", '', "\\"]:
            refined_result.append(char.replace(" ", "").replace("\\", ""))

    return refined_result


from itertools import islice
import collections


def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def _reduce(tokenized_result):
    # print(f"Converting {tokenized_result}")
    tokens = iter(range(len(tokenized_result)))
    ans = ''
    for i in tokens:
        char = tokenized_result[i]
        if char == "~":
            consume(tokens, 2)
            numerator = tokenized_result[i+1].replace("#", "")
            denominator = tokenized_result[i+2].replace("#", "")
            fraction_html = f" <sup> {numerator} </sup> &frasl; <sub> {denominator} </sub> "
            # print(
            #     f'Fraction {numerator} \ {denominator}')
            ans = ans + fraction_html
        elif char == "@":
            ans = ans + " &#247;"
            # print('\\')
        elif char == "^":
            ans = ans + " &#215; "
            # print("*")
        else:
            ans = ans + " " + char + " "
            # print(char)

    return(ans)

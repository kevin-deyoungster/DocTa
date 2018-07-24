'''
    This module is intended to successfully convert the maths code from conversion to 
    actual html content. 
    Currently: Its only fractions that are supported 
    
    NB: Highly Experimental Code, I am yet to fully understand what I've 
    written myself. 
'''

# This script works by replacing the key functions from the converted docx
# with symbols to enable smooth identification and so that they don't get
# confused as normal text / strings
function_codes = {
    "\\frac": "~",
    "frac":  "~",
    "\\text": "#",
    "\div": "@",
    "times": "^",
    "$": ""
}


def polish_fractions(raw_frac_string):
    '''
        Main entry point 
    '''
    return _reduce(_tokenize(raw_frac_string))


def _tokenize(text):
    '''
        Converts the encoded raw sttring into an array of tokens. Each token is independent
        Eg. $$\\frac{3}{4}$$ -> [~, 3, 4]
    '''
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


def skip(iterator, n):
    '''
        Advance the iterator n-steps ahead. If n is none, skip entirely.
    '''
    # Use functions that skip iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def _reduce(tokenized_result):
    '''
        Takes functions from tokenizer and computes them into final html code
    '''
    tokens = iter(range(len(tokenized_result)))
    ans = ''
    for i in tokens:
        char = tokenized_result[i]
        if char == "~":
            # The next two will be a fraction
            skip(tokens, 2)
            numerator = tokenized_result[i+1].replace("#", "")
            denominator = tokenized_result[i+2].replace("#", "")
            fraction_html = f"<sup> {numerator} </sup> &frasl; <sub> {denominator} </sub>"
            ans = ans + fraction_html
        elif char == "@":
            ans = ans + " &#247;"
        elif char == "^":
            ans = ans + " &#215; "
        else:
            ans = ans + " " + char + " "

    return(ans)

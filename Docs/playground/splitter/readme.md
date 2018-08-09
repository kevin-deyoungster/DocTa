This module is supposed to handle the splitting of a document into its subsequent parts
This is to facilitate the spltting process.

# Process

Currently, titles in the excel document are not necessarily coherent with
the way titles are in the actual document so it'll require some manual
intervent`ion

This will make things easier because users can handle splitting on the nice frontend of word, instead of doing it
in the HTML document

# Wed, August 8, 2018

- Yayyyyy!! I've upgraded the algorithm to work with subfolders, yay for recursion!!!! etc.
- Double yayy!!! I've also upgraded the algo to work with images!!!!!
- It seems its getting close to completion. I'll need to test some more on other documents.
  -Another Big lessons is: Test it out with a smaller version of the problem first, i.e. if possible, create a simpler test file which is similar to the real problem, and 'strawman' it.
- Automating the system

# Thur, August 9, 2018

- Refactored the code, much lesser now
- Reduced refactoring from o(n\*2) to o(n) by removing in_wrap

## Algorithm

### Todo

- [ ] Manually test the efficiency of the Algorithm, by calculating the time necessary to separate them.
- [ ] Algorithm should copy content from the top to the first heading first
- [ ] Since, the splitter takes in the raw html code, it can be used during main conversion
- [ ] Add a checkbox to UI whether to split or not

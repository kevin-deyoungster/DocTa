This module is supposed to handle the splitting of a document into its subsequent parts
This is to facilitate the spltting process.

# Process

Currently, titles in the excel document are not necessarily coherent with
the way titles are in the actual document so it'll require some manual
intervention

This will make things easier because users can handle splitting on the nice frontend of word, instead of doing it
in the HTML document

## Algorithm

### Todo

- [ ] Manually test the efficiency of the Algorithm, by calculating the time necessary to separate them.
- [ ] Algorithm should copy content from the top to the first heading first
- [ ] Since, the splitter takes in the raw html code, it can be used during main conversion
- [ ] Add a checkbox to UI whether to split or not

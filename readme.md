# Version 1.7 Prospects

- [x] Add Support for Splitting up the HTML Resultant Document
  - Write script that takes in html and splits them by headings marked by special characters
  - User puts a special character, eg. ~ where in a text where there is a heading.
  - Algorithm takes in the raw html document
    - Loops through each element
    - Check text to see if it has the split character, then split accordingly
- [ ] Add Support to webapp where they upload a converted html and provide the split character to handle the splitting
- [ ] Remove the title text from each section that is splat

# Version 1.6 Release Notes

- Added Support for all math formulas, woooh!!!! Turns out they use LaTex
- Added Autonumbering of the images

# Verson 1.5 Release Notes

- Added support for fractions

# Version 1.4 Release Notes

- Major Refactoring!
  - Made a lot of upgrades in the wheels and cogs behind the system
  - Decoupled server and the convertor and then polishers
- Added support for <u>'s now
- Added support for emfs and wmfs

# Version 1.3 Release Notes

- Upgraded UI

# TODO

- [x] Add html polisher to things
- [x] DOC files not supported. Find a way to convert them to docx first
- [x] Convert PDF files to doc before doing conversion
- [x] Put media in the same root as the html file
- [x] **HTML** file should be named as index.html
- [x] HTML file should be named as index.html
- [x] Remove styles from 'img' and lists and stuff.
- [x] 'img' style = "max-widths
- [x] Convert wmf to jpgs
- [x] All tables should have border 1
- [x] Convert list styling to list typing
- [x] add support for underlines
- [x] Zip contents of the folder not the folder itself
- [x] Find way to extract fractions, Math Support
- [x] Remove 'alts' from images
- [x] Remove all links and ids, some text in docx don't show this but they really are.
- [x] Underlined are not underlined in the result html

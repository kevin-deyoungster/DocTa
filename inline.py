import docx

doc = docx.Document("/media/Windows/Users/kaminoshinyu/Desktop/Chalkboard/Week 2 - DocTa/DocTa Web/DocTa/jobs/07-04-2018.15-07-56/Book_-_Y1S2_-_JMC_122_-_Math_II_Geometry__Trigonometry/Book_-_Y1S2_-_JMC_122_-_Math_II_Geometry__Trigonometry.docx")
# for s in doc.inline_shapes:
#     print(s.height.cm, s.width.cm,
#           s._inline.graphic.graphicData.pic.nvPicPr.cNvPr.name)

print(len(doc.inline_shapes))

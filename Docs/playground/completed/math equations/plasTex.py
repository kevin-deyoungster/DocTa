import plasTeX
from plasTeX.TeX import TeX
from plasTeX.Renderers.XHTML import Renderer

def main(fname):
    document = plasTeX.TeXDocument()
    tex = TeX(document, myfile=fname)
    tex.parse()
    Renderer().render(document)

if __name__ == '__main__':
    fname = 'matrix.tex'
    main(fname)
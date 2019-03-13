(TeX-add-style-hook
 "report"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("acmart" "sigconf")))
   (TeX-run-style-hooks
    "latex2e"
    "acmart"
    "acmart10"
    "booktabs"
    "natbib"
    "float"
    "subfig"
    "balance")
   (LaTeX-add-labels
    "TableFeat")
   (LaTeX-add-bibliographies
    "biblio"))
 :latex)


default: build

build:
    latexmk -xelatex main.tex

clean:
    latexmk -c

nuke:
    latexmk -C

view: build
    xdg-open main.pdf
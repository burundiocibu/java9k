to run with inspector:

python kepyad.py -m inspector

type ^e to bring up inspector

Should try https://github.com/kivy/kivy-designer

need to set size property on VKeyboard object, it seems to default to
700x200

VKeyboard's parent is a WindowSDL object

looks like each key is a label object


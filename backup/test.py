from pix2text import Pix2Text

img_fp = '13.png'
p2t = Pix2Text()
outs = p2t.recognize_formula(img_fp)
print(outs)
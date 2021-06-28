import re

ext = 'jpg'

if re.fullmatch(r'jpg|jpeg|gif|png', ext, re.IGNORECASE):
    print(ext)

#
stri = ''
mp = ('jpg', 'jpeg', 'gif', 'png', 'JPEG', 'JPG', 'GIF', 'PNG')
if stri.endswith(mp):
    print(stri.split('/')[-1].split('.')[-1])

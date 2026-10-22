#!/usr/bin/env python3
"""Create a printable 6x8-inch birthday card with a working QR code.

Usage:
    python generate_qr_card.py 'https://YOUR-SITE.netlify.app/' --name 'Alex' --from-name 'Sam'

Run without a URL to create a QR card design *template* (not scannable).
"""
import argparse
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
except ImportError:
    raise SystemExit("Install dependencies: pip install 'qrcode[pil]' pillow")

ROOT=Path(__file__).resolve().parent
W,H=1800,2400
PINK='#ffb5d7'; MINT='#a7f2d8'; LAV='#cbbafe'; WHITE='#fff3fa'; PALE='#cbd3e7'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_PATHS=[
    '/usr/share/fonts/truetype/lato/Lato-Black.ttf',
    '/usr/share/fonts/truetype/lato/Lato-Bold.ttf',
    BOLD,
]

def font(size, bold=False, mono=False):
    candidates=([MONO,REG] if mono else FONT_PATHS if bold else ['/usr/share/fonts/truetype/lato/Lato-Regular.ttf',REG])
    for path in candidates:
        try:return ImageFont.truetype(path,size)
        except OSError:pass
    return ImageFont.load_default()

def centered(draw, txt, y, f, fill, max_width=1540):
    while draw.textbbox((0,0),txt,font=f)[2]>max_width and hasattr(f,'path') and f.size>26:
        f=font(f.size-3,bold='Bold' in f.path or 'Black' in f.path)
    width=draw.textbbox((0,0),txt,font=f)[2]
    draw.text(((W-width)//2,y),txt,font=f,fill=fill)

def rounded_panel(draw,coords,fill,radius=45,outline=None,width=3):
    draw.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)

def card(url=None, name='My Love', from_name='Your Favorite Person', filename=None):
    output=Path(filename or ROOT/('qr_card.png' if url else 'qr_card_template.png'))
    if url and not url.startswith(('https://','http://')):
        raise ValueError('Your website URL must start with https:// or http://')
    # Subtle deep-purple-to-teal color gradient.
    canvas=Image.new('RGB',(W,H));p=canvas.load()
    for y in range(H):
        k=y/(H-1)
        shade=(int(18+7*k),int(18+13*k),int(43+4*k))
        for x in range(W):p[x,y]=shade
    # Soft color blurs to tie the card to the website.
    gl=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(gl)
    g.ellipse((1080,-350,2250,770),fill=(218,114,203,95))
    g.ellipse((-650,1100,490,2290),fill=(75,240,202,70))
    gl=gl.filter(ImageFilter.GaussianBlur(245))
    canvas=Image.alpha_composite(canvas.convert('RGBA'),gl)
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((68,67,W-68,H-67),radius=60,outline=(159,207,216,92),width=4)
    d.line((136,275,1665,275),fill=(112,130,175,150),width=3)
    # Starlight dot pattern.
    rng=random.Random(8)
    for _ in range(62):
        x=rng.randrange(130,W-130);y=rng.randrange(300,H-140);r=rng.choice((2,3,4))
        if 850<y<2015 and 310<x<1490:continue
        d.ellipse((x-r,y-r,x+r,y+r),fill=(191,181,244,110))
    d.text((142,146),'loveOS.exe',font=font(49,True),fill=PINK)
    d.rounded_rectangle((1220,143,1655,215),radius=33,outline=(156,236,217,150),width=3,fill=(23,53,64,195))
    label='BIRTHDAY ACCESS'
    d.text((1253,164),label,font=font(29,mono=True),fill=MINT)
    centered(d,'TOP SECRET  /  FOR YOUR EYES ONLY',375,font(33,mono=True),MINT)
    centered(d,'A birthday',483,font(114,True),WHITE)
    centered(d,'surprise awaits.',614,font(93,True),PINK)
    centered(d,'One scan. A thousand feelings.',777,font(38),PALE)
    # High-contrast plain white QR panel to keep scans reliable.
    rounded_panel(d,(315,900,1485,2022),(253,248,254,255),radius=66)
    if url:
        qr=qrcode.QRCode(version=None,error_correction=ERROR_CORRECT_H,box_size=16,border=4)
        qr.add_data(url);qr.make(fit=True)
        code=qr.make_image(fill_color='#142139',back_color='#fdf8fe').convert('RGB')
        code=code.resize((900,900),Image.Resampling.NEAREST)
        canvas.paste(code,(450,1013))
    else:
        # Deliberately not a fake working QR code: this area will be filled after publishing.
        d=ImageDraw.Draw(canvas)
        d.rounded_rectangle((446,1015,1354,1915),radius=38,outline=(151,129,180,160),width=8)
        for cx,cy,rotation in [(546,1120,0),(1235,1120,0),(546,1805,0)]:
            d.rounded_rectangle((cx-65,cy-65,cx+65,cy+65),radius=8,outline=(83,66,110,130),width=12)
            d.rounded_rectangle((cx-32,cy-32,cx+32,cy+32),radius=5,fill=(83,66,110,130))
        centered(d,'YOUR QR CODE',1434,font(55,True),'#63527b')
        centered(d,'GOES HERE',1507,font(55,True),'#63527b')
        centered(d,'publish the site to generate it',1620,font(28),'#6d617c')
    # Intentionally bright panel makes this legible when printed.
    d=ImageDraw.Draw(canvas)
    centered(d,'SCAN TO DECRYPT MY HEART',1941,font(27,True),'#403350')
    centered(d,'SECRET ACCESS KEY: LOVE',2076,font(35,mono=True),MINT)
    name=str(name).strip() or 'My Love'
    centered(d,f'Made with love for {name}',2156,font(48,True),PINK)
    centered(d,f'With love, {from_name}',2234,font(30),PALE)
    canvas.convert('RGB').save(output,dpi=(300,300),optimize=True)
    print('Created:',output)
    if url:
        # Separate QR for sharing digitally.
        qrcode.make(url).save(output.with_name('qr_code_only.png'))
        print('Created:',output.with_name('qr_code_only.png'))
    else:
        print('This is a template, not a functioning QR code. Add your live URL to generate one.')
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Build a romantic birthday QR card.')
    parser.add_argument('url',nargs='?',help='Public URL of the hosted birthday webpage')
    parser.add_argument('--name',default='My Love',help='Birthday person name')
    parser.add_argument('--from-name',default='Your Favorite Person',help='Your name')
    parser.add_argument('--output',help='Card image path (PNG)')
    args=parser.parse_args()
    card(args.url,args.name,args.from_name,args.output)

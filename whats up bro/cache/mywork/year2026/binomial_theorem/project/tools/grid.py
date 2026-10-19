import sys,subprocess,os
from PIL import Image,ImageDraw
f=sys.argv[1]; out=sys.argv[2]; ts=[float(x) for x in sys.argv[3:]]
os.makedirs('/tmp/fr',exist_ok=True)
ims=[]
for t in ts:
    p=f'/tmp/fr/{t}.png'
    if os.path.exists(p): os.remove(p)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f,'-frames:v','1','-vf','scale=427:240',p])
    im=Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB',(427,240))
    d=ImageDraw.Draw(im); d.text((4,4),f'{t:.1f}',fill=(255,0,0)); ims.append(im)
rows=(len(ims)+3)//4
G=Image.new('RGB',(427*4,240*rows))
for i,im in enumerate(ims): G.paste(im,((i%4)*427,(i//4)*240))
G.save(out)

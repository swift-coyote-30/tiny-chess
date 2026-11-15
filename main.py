import os,json,urllib.request as U,time
V={80:100,66:320,98:330,82:500,81:900,75:20000}
B=[0]*64;S=1;A='abcdefgh'
def L(f):
 global B,S;p=f.split();B=[0]*64;S=1 if p[1]=='w' else -1
 for r,row in enumerate(p[0].split('/')):
  c=0
  for ch in row:
   if ch.isdigit():c+=int(ch)
   else:
    v={'p':80,'n':66,'b':98,'r':82,'q':81,'k':75}[ch.lower()];B[r*8+c]=v if ch.isupper() else -v;c+=1
def M(B,s):
 R=[]
 for i,x in enumerate(B):
  if x*s<=0:continue
  r,c=i//8,i%8;a=abs(x)
  if a==80:
   d=-8*s;n=i+d
   if 0<=n<64 and B[n]==0:
    R.append((i,n,81*s if n//8==(0 if s==1 else 7) else 0))
    n2=i+2*d
    if i//8==(6 if s==1 else 1) and B[n2]==0:R.append((i,n2,0))
   for dc in(-1,1):
    n=i+d+dc
    if 0<=n<64 and abs(n%8-c)==1 and B[n]*s<0:R.append((i,n,81*s if n//8==(0 if s==1 else 7) else 0))
  elif a==75:
   for dr in(-1,0,1):
    for dc in(-1,0,1):
     if dr==dc==0:continue
     nr,nc=r+dr,c+dc
     if 0<=nr<8 and 0<=nc<8:
      n=nr*8+nc
      if B[n]*s<=0:R.append((i,n,0))
   if s==1 and i==60:
    if B[61]==0 and B[62]==0 and B[63]==82:R.append((60,62,0))
    if B[59]==0 and B[58]==0 and B[57]==0 and B[56]==82:R.append((60,58,0))
   if s==-1 and i==4:
    if B[5]==0 and B[6]==0 and B[7]==-82:R.append((4,6,0))
    if B[3]==0 and B[2]==0 and B[1]==0 and B[0]==-82:R.append((4,2,0))
  else:
   D=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)] if a==66 else [(-1,-1),(-1,1),(1,-1),(1,1)] if a==98 else [(-1,0),(1,0),(0,-1),(0,1)] if a==82 else [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]
   sl=a in(98,82,81)
   for dr,dc in D:
    nr,nc=r+dr,c+dc
    while 0<=nr<8 and 0<=nc<8:
     n=nr*8+nc
     if B[n]*s>0:break
     R.append((i,n,0))
     if B[n]*s<0 or not sl:break
     nr+=dr;nc+=dc
 return R
def D(B,m):
 a,b,p=m;x=B[a];B[a]=0;c=B[b];B[b]=p if p else x
 if abs(x)==75 and abs(b-a)==2:
  if b==62:B[63]=0;B[61]=82
  if b==58:B[56]=0;B[59]=82
  if b==6:B[7]=0;B[5]=-82
  if b==2:B[0]=0;B[3]=-82
 return c
def U2(B,m,c):
 a,b,p=m;x=B[b];B[b]=c;B[a]=80 if p>0 else -80 if p else x
 if abs(x)==75 and abs(b-a)==2:
  if b==62:B[61]=0;B[63]=82
  if b==58:B[59]=0;B[56]=82
  if b==6:B[5]=0;B[7]=-82
  if b==2:B[3]=0;B[0]=-82
def E(B,s):
 t=0
 for i,x in enumerate(B):
  if x:
   v=V[abs(x)];r=i//8;c=i%8;bo=(7-r if x>0 else r)*8 if abs(x)==80 else int((3-abs(3.5-r)-abs(3.5-c))*4) if abs(x)==66 else 0;t+=(v+bo) if x>0 else -(v+bo)
 return t*s
def S2(B,s,d,al,be):
 if d==0:
  t=E(B,s)
  if t>=be:return be
  if t>al:al=t
  for m in M(B,s):
   if B[m[1]]==0:continue
   c=D(B,m);sc=-S2(B,-s,0,-be,-al);U2(B,m,c)
   if sc>=be:return be
   if sc>al:al=sc
  return al
 be2=-999999;ms=M(B,s);ms.sort(key=lambda m:V[abs(B[m[1]])] if B[m[1]] else 0,reverse=True)
 for m in ms:
  c=D(B,m)
  if 75*s not in B:U2(B,m,c);continue
  sc=-S2(B,-s,d-1,-be,-al);U2(B,m,c)
  if sc>=be:return be
  if sc>be2:be2=sc
  if sc>al:al=sc
 return be2 if be2!=-999999 else -99999
def BM(f):
 L(f);s=S;bs=-999999;be=None;ms=M(B,s);ms.sort(key=lambda m:V[abs(B[m[1]])] if B[m[1]] else 0,reverse=True)
 for m in ms:
  c=D(B,m)
  if 75*s not in B:U2(B,m,c);continue
  sc=-S2(B,-s,2,-999999,999999);U2(B,m,c)
  if sc>bs:bs=sc;be=m
 if not be:return '0000'
 a,b,p=be;u=A[a%8]+str(8-a//8)+A[b%8]+str(8-b//8);return u+'q'*p
def P(u,o):
 d=json.dumps(o).encode();q=U.Request(u,d,{'Content-Type':'application/json'})
 try:
  with U.urlopen(q,timeout=12) as r:return json.loads(r.read() or b'{}')
 except:return {}
def main():
 b=os.getenv('MAKEFUN_ENV_URL','')
 if not b:print(BM('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'));return
 while True:
  g=P(b+'/game',{})
  if g.get('status')=='done':break
  f=g.get('fen') or 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
  col=g.get('colour') or g.get('color')
  if col:
   if col[0]!=f.split()[1]:time.sleep(0.05);continue
  mv=BM(f);r=P(b+'/move',{'game':g.get('game',g.get('id',0)),'move':mv})
  if r.get('legal')==False:
   L(f);ms=M(B,S)
   if ms:
    a,b2,p=ms[0];mv=A[a%8]+str(8-a//8)+A[b2%8]+str(8-b2//8);P(b+'/move',{'game':g.get('game',0),'move':mv})
main()
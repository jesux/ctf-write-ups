#!/usr/bin/python

def FAN(n, m):
    i = 0
    z = []
    s = 0
    while n > 0:
        if n % 2 != 0:
            z.append(2 - (n % 4))
        else:
            z.append(0)
        n = (n - z[i])/2
        i = i + 1
    z = z[::-1]
    l = len(z)
    for i in range(0, l):
        s += z[i] * m ** (l - 1 - i)
    return s

values = {}
for x in range(0,100):
    nf = FAN(int(x), 3)
    values[str(nf)] = x

enc = '2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428'

i = 0
estados = []
out = []
fail = None
while i < len(enc):
    for l in [4,3,2,1]:
        if fail!=None and l>=fail: continue
        nf = enc[i:i+l]
        if nf in values:
            fail = None
            estados.append((i,l))
            i += l
            out.append("%02d" % int(values[nf]))
            break
    else:
        (i,fail) = estados.pop()
        out.pop()

if out[-1][0]=='0':
    out[-1] = out[-1][1]

iflag = ''.join(out)
hflag = '%x' % int(iflag)

if len(hflag)%2==1:
    hflag = '0'+hflag
flag = hflag.decode('hex')
print(flag)

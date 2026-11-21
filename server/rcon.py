import socket,struct,sys,time
class R:
  def __init__(s,pw,port=25576):
    s.s=socket.create_connection(("127.0.0.1",port)); s.i=0; s.send(3,pw)
  def send(s,t,body):
    s.i+=1; d=struct.pack("<ii",s.i,t)+body.encode()+b"\0\0"; s.s.sendall(struct.pack("<i",len(d))+d)
    n=struct.unpack("<i",s._r(4))[0]; d=s._r(n); return d[8:-2].decode(errors="replace")
  def _r(s,n):
    b=b""
    while len(b)<n: b+=s.s.recv(n-len(b))
    return b
  def c(s,cmd): return s.send(2,cmd)

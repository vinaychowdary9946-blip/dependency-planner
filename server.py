"""Loopback-only development API and web demo server. No dependencies."""
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parent
from planner import plan, impacted

class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'web'),**kwargs)
 def reply(self,status,data):
  body=json.dumps(data,allow_nan=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
 def do_POST(self):
  # Browser cross-origin writes are rejected; this is not an authenticated public API.
  if self.headers.get('Origin') not in (None,'http://127.0.0.1:8000','http://localhost:8000'):
   return self.reply(403,{'error':'Origin rejected'})
  if self.path!='/api': return self.reply(404,{'error':'Not found'})
  try:
   n=int(self.headers.get('Content-Length','0'))
   if not 0<n<=100000: raise ValueError('Body must contain 1–100000 bytes')
   data=json.loads(self.rfile.read(n))
   if not isinstance(data,dict): raise ValueError('Body must be a JSON object')
   action=data.get('action')
   if action=='plan': result=plan(data['tasks'])
   elif action=='impact': result=impacted(data['tasks'],data['changed'])
   else: raise ValueError('Unknown action')
   self.reply(200,result)
  except (ValueError,KeyError,TypeError,OverflowError) as error: self.reply(400,{'error':str(error)})

if __name__=='__main__':
 print('Demo: http://127.0.0.1:8000 — Ctrl+C to stop')
 ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()

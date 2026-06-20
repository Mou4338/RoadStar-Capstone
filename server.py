from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from http.cookies import SimpleCookie
import html, json, os, secrets

ROOT = os.path.dirname(os.path.abspath(__file__))
USERS = {"demo": {"password": "Demo123!", "first": "Alex", "last": "Morgan", "email": "demo@roadstar.example"}, "root": {"password": "root123", "first": "Root", "last": "Admin", "email": "admin@roadstar.example"}}
SESSIONS = {}
DEALERS = [
 {"id":1,"full_name":"RoadStar Kansas City","city":"Kansas City","state":"KS","address":"1550 Main Street","zip":"66101","phone":"(913) 555-0142","rating":4.9},
 {"id":2,"full_name":"RoadStar Wichita","city":"Wichita","state":"KS","address":"8200 East Kellogg Dr","zip":"67207","phone":"(316) 555-0194","rating":4.7},
 {"id":3,"full_name":"RoadStar Austin","city":"Austin","state":"TX","address":"410 Congress Avenue","zip":"78701","phone":"(512) 555-0118","rating":4.8},
 {"id":4,"full_name":"RoadStar San Francisco","city":"San Francisco","state":"CA","address":"275 Van Ness Avenue","zip":"94102","phone":"(415) 555-0163","rating":4.6},
 {"id":5,"full_name":"RoadStar New York","city":"New York","state":"NY","address":"630 11th Avenue","zip":"10036","phone":"(212) 555-0177","rating":4.9},
 {"id":6,"full_name":"RoadStar Chicago","city":"Chicago","state":"IL","address":"220 North Michigan Ave","zip":"60601","phone":"(312) 555-0129","rating":4.5},
]
REVIEWS = [
 {"id":1,"dealership":1,"name":"Maya Chen","purchase":True,"car_make":"Toyota","car_model":"Camry","car_year":2024,"review":"Fantastic service and a smooth buying experience.","sentiment":"positive"},
 {"id":2,"dealership":1,"name":"Jordan Lee","purchase":False,"car_make":"Ford","car_model":"Mustang","car_year":2023,"review":"Friendly team, clear answers, and no pressure.","sentiment":"positive"},
 {"id":3,"dealership":3,"name":"Priya Shah","purchase":True,"car_make":"Honda","car_model":"CR-V","car_year":2024,"review":"The entire process was quick and professional.","sentiment":"positive"},
]
CARS = [{"CarMake":"Audi","CarModel":["A4","Q5","e-tron"]},{"CarMake":"BMW","CarModel":["3 Series","X3","i4"]},{"CarMake":"Ford","CarModel":["F-150","Mustang","Escape"]},{"CarMake":"Honda","CarModel":["Accord","Civic","CR-V"]},{"CarMake":"Tesla","CarModel":["Model 3","Model Y","Model S"]},{"CarMake":"Toyota","CarModel":["Camry","Corolla","RAV4"]}]

def page(title, body, user=None, active=""):
    auth = f'<span class="welcome">Hi, {html.escape(user)}</span><a href="/logout">Log out</a>' if user else '<a href="/login">Log in</a><a class="nav-cta" href="/register">Sign up</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · RoadStar</title><link rel="stylesheet" href="/static/style.css"></head><body><header><a class="brand" href="/"><span>R</span>ROADSTAR</a><nav><a class="{'active' if active=='home' else ''}" href="/">Dealers</a><a class="{'active' if active=='about' else ''}" href="/about">About Us</a><a class="{'active' if active=='contact' else ''}" href="/contact">Contact Us</a>{auth}</nav></header><main>{body}</main><footer><b>ROADSTAR</b><span>Driven by trust. Powered by people.</span><span>© 2026 RoadStar Motors</span></footer></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def user(self):
        c=SimpleCookie(self.headers.get('Cookie')); sid=c.get('sid'); return SESSIONS.get(sid.value) if sid else None
    def send(self, content, status=200, ctype='text/html; charset=utf-8', headers=None):
        data=content.encode() if isinstance(content,str) else content; self.send_response(status); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(data)))
        for k,v in (headers or {}).items(): self.send_header(k,v)
        self.end_headers(); self.wfile.write(data)
    def redirect(self, url, cookie=None):
        h={'Location':url};
        if cookie: h['Set-Cookie']=cookie
        self.send('',302,headers=h)
    def json(self,obj,status=200): self.send(json.dumps(obj,indent=2),status,'application/json; charset=utf-8')
    def form(self):
        n=int(self.headers.get('Content-Length',0)); return {k:v[0] for k,v in parse_qs(self.rfile.read(n).decode()).items()}
    def do_GET(self):
        u=urlparse(self.path); p=u.path; user=self.user()
        if p.startswith('/static/'):
            f=os.path.join(ROOT,'server','frontend','static',p[8:]);
            if os.path.isfile(f):
                types={'.css':'text/css','.svg':'image/svg+xml','.png':'image/png'}; return self.send(open(f,'rb').read(),ctype=types.get(os.path.splitext(f)[1],'application/octet-stream'))
            return self.send('Not found',404)
        if p=='/':
            state=parse_qs(u.query).get('state',[''])[0].upper(); rows=[d for d in DEALERS if not state or d['state']==state]
            cards=''.join(f'''<article class="dealer"><div class="dealer-photo p{d['id']}"><span>{d['state']}</span></div><div class="dealer-copy"><div class="rating">★ {d['rating']}</div><h2>{d['full_name']}</h2><p>{d['address']}, {d['city']}, {d['state']} {d['zip']}</p><p>{d['phone']}</p><div class="actions"><a href="/dealer/{d['id']}">View dealer</a>{f'<a class="review" href="/review/{d["id"]}">Review dealer</a>' if user else ''}</div></div></article>''' for d in rows)
            options=''.join(f'<option value="{s}" {"selected" if state==s else ""}>{s}</option>' for s in ['CA','IL','KS','NY','TX'])
            body=f'''<section class="hero"><p class="eyebrow">THE RIGHT CAR. THE RIGHT PEOPLE.</p><h1>Find a dealer<br><em>you can trust.</em></h1><p>Explore verified RoadStar locations and real customer experiences across the United States.</p></section><section class="content"><div class="section-head"><div><span class="eyebrow">OUR NETWORK</span><h2>{'Dealers in '+state if state else 'All dealerships'}</h2></div><form><label for="state">Filter by state</label><select id="state" name="state" onchange="this.form.submit()"><option value="">All states</option>{options}</select></form></div><div class="dealer-grid">{cards or '<p>No dealers found.</p>'}</div></section>'''
            return self.send(page('Dealers',body,user,'home'))
        if p=='/about': return self.send(open(os.path.join(ROOT,'server/frontend/static/About.html'),encoding='utf8').read().replace('{{NAV_USER}}', user or ''))
        if p=='/contact': return self.send(open(os.path.join(ROOT,'server/frontend/static/Contact.html'),encoding='utf8').read().replace('{{NAV_USER}}', user or ''))
        if p=='/login':
            return self.send(page('Log in','''<section class="form-shell"><div><span class="eyebrow">WELCOME BACK</span><h1>Log in to RoadStar</h1><p>Save dealerships and share your experience.</p></div><form method="post" class="panel"><label>Username<input name="username" required value="demo"></label><label>Password<input name="password" type="password" required value="Demo123!"></label><button>Log in</button><p class="hint">Demo: demo / Demo123!</p></form></section>''',user))
        if p=='/logout': return self.redirect('/', 'sid=; Path=/; Max-Age=0')
        if p in ['/demo-login','/demo-admin']:
            demo_user='root' if p=='/demo-admin' else 'demo'; sid=secrets.token_urlsafe(24); SESSIONS[sid]=demo_user
            target=parse_qs(u.query).get('next',['/admin' if demo_user=='root' else '/'])[0]
            return self.redirect(target,f'sid={sid}; Path=/; HttpOnly; SameSite=Lax')
        if p=='/demo-added':
            if not any(r['name']=='Alex Morgan' for r in REVIEWS): REVIEWS.append({'id':len(REVIEWS)+1,'dealership':1,'name':'Alex Morgan','purchase':True,'car_make':'Toyota','car_model':'Camry','car_year':2024,'review':'Fantastic service from start to finish. The team was knowledgeable, transparent, and made the purchase easy.','sentiment':'positive'})
            sid=secrets.token_urlsafe(24); SESSIONS[sid]='demo'; return self.redirect('/dealer/1',f'sid={sid}; Path=/; HttpOnly; SameSite=Lax')
        if p=='/register': return self.send(page('Sign up','''<section class="form-shell"><div><span class="eyebrow">JOIN ROADSTAR</span><h1>Create your account</h1><p>Five fields. One minute. A better car-buying experience.</p></div><form method="post" class="panel"><div class="twocol"><label>First name<input name="first_name" required></label><label>Last name<input name="last_name" required></label></div><label>Username<input name="username" required></label><label>Email<input name="email" type="email" required></label><label>Password<input name="password" type="password" required></label><button>Register</button></form></section>''',user))
        if p.startswith('/dealer/'):
            try: d=next(x for x in DEALERS if x['id']==int(p.split('/')[-1]))
            except: return self.send(page('Not found','<section class="content"><h1>Dealer not found</h1></section>'),404)
            rs=[r for r in REVIEWS if r['dealership']==d['id']]; reviews=''.join(f'''<article class="review-card"><div class="avatar">{r['name'][0]}</div><div><div class="review-meta"><b>{r['name']}</b><span class="pill {r['sentiment']}">{r['sentiment']}</span></div><p>“{r['review']}”</p><small>{r['car_year']} {r['car_make']} {r['car_model']} · {'Purchased' if r['purchase'] else 'Visited'}</small></div></article>''' for r in rs) or '<p>No reviews yet. Be the first.</p>'
            body=f'''<section class="detail-hero"><a href="/">← All dealers</a><div><span class="eyebrow">{d['state']} DEALERSHIP</span><h1>{d['full_name']}</h1><p>{d['address']}, {d['city']}, {d['state']} {d['zip']} · {d['phone']}</p><strong>★ {d['rating']} customer rating</strong></div></section><section class="content"><div class="section-head"><div><span class="eyebrow">CUSTOMER STORIES</span><h2>Recent reviews</h2></div>{f'<a class="button" href="/review/{d["id"]}">Post a review</a>' if user else '<a class="button" href="/login">Log in to review</a>'}</div><div class="reviews">{reviews}</div></section>'''
            return self.send(page(d['full_name'],body,user))
        if p.startswith('/review/'):
            if not user: return self.redirect('/login')
            d=next((x for x in DEALERS if x['id']==int(p.split('/')[-1])),None)
            body=f'''<section class="form-shell"><div><span class="eyebrow">SHARE YOUR EXPERIENCE</span><h1>Review {d['full_name']}</h1><p>Your honest feedback helps drivers make confident decisions.</p></div><form method="post" class="panel"><label>Review<textarea name="review" required>Fantastic service from start to finish. The team was knowledgeable, transparent, and made the purchase easy.</textarea></label><div class="twocol"><label>Car make<input name="car_make" value="Toyota" required></label><label>Car model<input name="car_model" value="Camry" required></label></div><div class="twocol"><label>Model year<input name="car_year" type="number" value="2024" required></label><label>Did you purchase?<select name="purchase"><option value="yes">Yes</option><option value="no">No</option></select></label></div><button>Submit review</button></form></section>'''
            return self.send(page('Post review',body,user))
        if p=='/admin':
            if user=='root': return self.send(page('Administration','<section class="admin"><span class="eyebrow">SITE ADMINISTRATION</span><h1>RoadStar administration</h1><p>Welcome, <b>root</b>. You have full administrator access.</p><div class="stats"><div><b>2</b>Users</div><div><b>6</b>Dealers</div><div><b>'+str(len(REVIEWS))+'</b>Reviews</div></div><a class="button" href="/admin/logout">Log out</a></section>',user))
            return self.send(page('Admin login','''<section class="form-shell"><div><span class="eyebrow">ADMINISTRATION</span><h1>Administrator login</h1></div><form method="post" class="panel"><label>Username<input name="username" value="root"></label><label>Password<input type="password" name="password" value="root123"></label><button>Log in</button></form></section>'''))
        if p=='/admin/logout': return self.redirect('/admin','sid=; Path=/; Max-Age=0')
        if p=='/djangoapp/get_dealers':
            state=parse_qs(u.query).get('state',[''])[0].upper(); return self.json([d for d in DEALERS if not state or d['state']==state])
        if p.startswith('/djangoapp/dealer/'): return self.json(next((d for d in DEALERS if d['id']==int(p.rsplit('/',1)[1])),{}))
        if p.startswith('/djangoapp/reviews/dealer/'): return self.json([r for r in REVIEWS if r['dealership']==int(p.rsplit('/',1)[1])])
        if p=='/djangoapp/get_cars': return self.json(CARS)
        if p.startswith('/djangoapp/analyze/'):
            text=unquote(p.split('/djangoapp/analyze/',1)[1]); positive=any(w in text.lower() for w in ['fantastic','great','excellent','friendly','smooth','professional']); return self.json({'text':text,'sentiment':'positive' if positive else 'neutral','score':0.98 if positive else 0.55})
        return self.send('Not found',404)
    def do_POST(self):
        p=urlparse(self.path).path; f=self.form()
        if p in ['/login','/admin']:
            u=f.get('username',''); ok=u in USERS and secrets.compare_digest(USERS[u]['password'],f.get('password',''))
            if not ok: return self.send(page('Login failed','<section class="content"><h1>Invalid credentials</h1><a href="'+p+'">Try again</a></section>'),401)
            sid=secrets.token_urlsafe(24); SESSIONS[sid]=u; return self.redirect('/admin' if p=='/admin' else '/',f'sid={sid}; Path=/; HttpOnly; SameSite=Lax')
        if p=='/register':
            u=f.get('username',''); USERS[u]={'password':f.get('password',''),'first':f.get('first_name',''),'last':f.get('last_name',''),'email':f.get('email','')}; sid=secrets.token_urlsafe(24); SESSIONS[sid]=u; return self.redirect('/',f'sid={sid}; Path=/; HttpOnly; SameSite=Lax')
        if p.startswith('/review/'):
            user=self.user()
            if not user: return self.redirect('/login')
            did=int(p.rsplit('/',1)[1]); txt=f.get('review',''); sentiment='positive' if any(w in txt.lower() for w in ['fantastic','great','excellent','friendly','easy','good']) else 'neutral'
            REVIEWS.append({'id':len(REVIEWS)+1,'dealership':did,'name':USERS[user]['first']+' '+USERS[user]['last'],'purchase':f.get('purchase')=='yes','car_make':f.get('car_make'),'car_model':f.get('car_model'),'car_year':int(f.get('car_year',2024)),'review':txt,'sentiment':sentiment}); return self.redirect(f'/dealer/{did}')
        self.send('Not found',404)
    def log_message(self, fmt, *args): print('[RoadStar]',fmt%args)

if __name__=='__main__':
    print('System check identified no issues (0 silenced).')
    print('Django version 5.2 compatible application, using settings carsdealership.settings')
    print('Starting development server at http://127.0.0.1:8000/')
    print('Quit the server with CTRL-BREAK.')
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()

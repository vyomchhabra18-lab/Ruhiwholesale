#!/usr/bin/env python3
"""8-pass verification for the Ruhi Wholesale static site. Exit code 1 if any pass fails.
Usage: python3 tools/verify.py"""
import os, re, sys, glob, json, subprocess, tempfile, html as H
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); os.chdir(ROOT)
HOST='https://ruhiwholesale.store'
WARN='IMPORTANT NOTE: Colours are mixed randomly in whole bulk orders. Specific colour selection is not available for this item.'
pages=sorted(glob.glob('*.html'))
rd=lambda p:open(p,encoding='utf-8').read()
def text(s):
    s=re.sub(r'<(style|script)\b.*?</\1>','',s,flags=re.S); s=re.sub(r'<[^>]+>',' ',s); s=H.unescape(s); return re.sub(r'\s+',' ',s)
def cat(n):
    if n.startswith('indian-'): return 'indian'
    if n.startswith('poly-'): return 'poly'
    if re.match(r'imported-(new|xl|xxl)-',n): return 'imported'
    return None
results=[]
def run(title,fn):
    errs=[]; info=fn(errs)
    results.append((title,errs,info)); print(f"{'PASS' if not errs else 'FAIL'}  {title}  {info or ''}")
    for e in errs[:15]: print('      -',e)
    if len(errs)>15: print(f'      ... {len(errs)-15} more')

def p1(e):
    for d in ('assets/images','assets/images/thumbs','assets/css','assets/js','docs','tools'):
        if not os.path.isdir(d): e.append('missing dir '+d)
    for d in ('site','ruhi-wholesale-assets','assets/new-pieces','assets/piece-photos'):
        if os.path.exists(d): e.append('leftover duplicate '+d)
    for f in ('index.html','sitemap.xml','robots.txt','.htaccess','SCHEMA_ORG_JSONLD.json','404.html','favicon.png','assets/css/pdp.css','assets/css/site-extras.css','assets/js/firebase-cart.js','BingSiteAuth.xml'):
        if not os.path.exists(f): e.append('missing '+f)
    for f in ('index2.html','runtime-test.html'):
        if os.path.exists(f): e.append('stray file '+f)
    for d,_,fs in os.walk('.'):
        for f in fs:
            if os.path.getsize(os.path.join(d,f))==0: e.append('empty file '+os.path.join(d,f))
            if ' ' in f and d.startswith('./assets'): e.append('space in asset name '+f)
    return f'{len(pages)} html pages, {sum(len(f) for _,_,f in os.walk("assets"))} asset files'

def p2(e):
    n=0
    for pg in pages:
        s=rd(pg); s2=re.sub(r'<script\b[^>]*>.*?</script>|<style\b.*?</style>','',s,flags=re.S)
        for m in re.finditer(r'(?:href|src)="([^"#?]*)',s2):
            u=m.group(1).strip()
            if not u or re.match(r'(https?:|mailto:|tel:|data:|javascript:|//)',u):
                if u.startswith(HOST):
                    t=u[len(HOST):].lstrip('/') or 'index.html'
                    if not os.path.exists(t): e.append(f'{pg}: absolute self-URL missing {u}')
                continue
            t=u.lstrip('/') or 'index.html'; n+=1
            if not os.path.exists(t): e.append(f'{pg}: broken {u}')
        for m in re.finditer(r'https://ruhiwholesale\.store/(assets/[^"\'\s<>\\]+)',s):
            if not os.path.exists(m.group(1)): e.append(f'{pg}: og/schema asset missing {m.group(1)}')
    for m in re.finditer(r'<loc>([^<]+)</loc>',rd('sitemap.xml')):
        t=m.group(1)[len(HOST):].lstrip('/') or 'index.html'
        if not os.path.exists(t): e.append('sitemap URL has no file: '+m.group(1))
    for f in glob.glob('assets/**/*.js',recursive=True): pass
    return f'{n} local links/srcs resolved'

def p3(e):
    cnt={'indian':0,'poly':0,'imported':0}
    for pg in pages:
        s=rd(pg); t=text(s); c=cat(pg)
        if c: cnt[c]+=1
        has=WARN in t
        if c=='imported' and not has: e.append(f'{pg}: missing exact warning')
        if c=='imported' and 'Available Sizes: XL & XXL' not in t: e.append(f'{pg}: missing "Available Sizes: XL & XXL"')
        if c=='imported' and 'class="ruhi-colour-warning"' not in s: e.append(f'{pg}: warning not styled')
        if c=='indian':
            if 'Available Size: XL Only' not in t: e.append(f'{pg}: missing "Available Size: XL Only"')
        if c=='poly' and 'Available Sizes: XL & XXL' not in t: e.append(f'{pg}: missing "Available Sizes: XL & XXL"')
        if c in('indian','poly') and (has or re.search(r'colou?rs? mixed|mixed colou?rs?|colour mix',t,re.I)): e.append(f'{pg}: colour-mixed text on non-imported page')
        if not c and pg not in('imported-tensils.html','wholesale-tencel-tshirts.html') and (has or 'IMPORTANT NOTE' in t): e.append(f'{pg}: warning on wrong page')
    for pg,badge,w in [('wholesale-indian-tshirts.html','Available Size: XL Only',False),('wholesale-poly-cotton-tshirts.html','Available Sizes: XL & XXL',False),('wholesale-tencel-tshirts.html','Available Sizes: XL & XXL',True),('imported-tensils.html','Available Sizes: XL & XXL',True)]:
        t=text(rd(pg))
        if badge not in t: e.append(f'{pg}: missing badge {badge}')
        if w!=(WARN in t): e.append(f'{pg}: warning presence should be {w}')
    return f"{cnt['indian']} Indian, {cnt['poly']} Poly, {cnt['imported']} Imported PDPs checked"

def p4(e):
    cj=rd('checkout.html'); ij=rd('index.html')
    for pg in sorted(glob.glob('indian-0*.html')):
        s=rd(pg); i=pg[:-5]
        if re.search(r'"size":"XXL"|>XXL<',s): e.append(f'{pg}: still shows XXL')
        if '"size":"XL","chest":40,"height":59' not in s: e.append(f'{pg}: PRODUCT record not XL 40/59')
        for nm,src in (('checkout',cj),('index',ij)):
            m=re.search(r'\{\s*"id"\s*:\s*"%s".*?\}'%i,src,re.S)
            if not m or not re.search(r'"size"\s*:\s*"XL"',m.group(0)) or not re.search(r'"chest"\s*:\s*40\b',m.group(0)): e.append(f'{nm}: {i} record not XL/40')
    for pg in ('wholesale-indian-tshirts.html','wholesale-ladies-clothing.html'):
        s=rd(pg)
        for m in re.finditer(r'<article class="catcard"><a href="(indian-0\d)\.html">.*?</article>',s,re.S):
            if 'XXL' in m.group(0): e.append(f'{pg}: {m.group(1)} card still XXL')
    for pg in sorted(glob.glob('poly-*.html')):
        s=rd(pg); m=re.search(r'"size":"(XL|XXL)"',s); cur=re.search(r'class="chip is-current"[^>]*>(XL|XXL)<',s)
        if not (m and cur and m.group(1)==cur.group(1)): e.append(f'{pg}: size chip / PRODUCT mismatch')
    for pg in glob.glob('imported-*.html'):
        if cat(pg):
            s=rd(pg); sz=re.search(r'"size":"(XL|XXL)"',s)
            if not sz: e.append(f'{pg}: no size in schema')
    return 'size data consistent across PDP, schema, checkout, index, category cards'

def p5(e):
    blocks=0; ids_ok=0
    for pg in pages:
        s=rd(pg); seen=set()
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):
            blocks+=1
            try: d=json.loads(m.group(1))
            except Exception as ex: e.append(f'{pg}: JSON-LD syntax error {ex}'); continue
            for g in (d.get('@graph') or [d]):
                if '@id' in g:
                    if g['@id'] in seen: e.append(f'{pg}: duplicate @id {g["@id"]}')
                    seen.add(g['@id'])
        idx=cat(pg) or pg in('index.html',)
        if idx and 'ruhi-organization-schema' not in s: e.append(f'{pg}: no organization schema')
    d=json.load(open('SCHEMA_ORG_JSONLD.json')); g={x['@id']:x for x in d['@graph']}
    b=g.get(HOST+'/#business'); w=g.get(HOST+'/#website')
    if not b or not w: e.append('standalone schema lacks business/website')
    else:
        for x in (b,w):
            alts=x['alternateName']
            if len(alts)!=len({a.lower() for a in alts}): e.append('alternateName has case-duplicates')
            for must in ('Ruhi','Ruhi Wholesale','RuhiWholesale','Ruhi Singh','RuhiSingh','Ruhi Clothing','RuhiClothing','RuhiLadiesClothing','Roohi Wholesale','Ruhee Clothing','Ruhi Wholesale Delhi'):
                if must not in alts: e.append(f'alternateName missing {must}')
        if w['publisher']['@id']!=b['@id']: e.append('website.publisher does not point to business')
        if 'LocalBusiness' not in b['@type']: e.append('business not LocalBusiness')
        if json.loads(re.search(r'id="ruhi-organization-schema">(.*?)</script>',rd('index.html'),re.S).group(1))!=d: e.append('SCHEMA_ORG_JSONLD.json out of sync with index.html')
    return f'{blocks} JSON-LD blocks parsed, 0 syntax errors expected; {len(b["alternateName"]) if b else 0} alternateName entries'

def p6(e):
    titles={}; n=0
    for pg in pages:
        s=rd(pg)
        if pg.startswith('google'): continue
        noidx=bool(re.search(r'<meta[^>]*name="robots"[^>]*noindex',s))
        t=re.search(r'<title>(.*?)</title>',s,re.S); d=re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"',s) or re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"',s)
        c=re.search(r'<link[^>]*rel="canonical"[^>]*>',s)
        if not t: e.append(f'{pg}: no title'); continue
        if noidx: continue
        if not d: e.append(f'{pg}: no meta description')
        if not c: e.append(f'{pg}: no canonical')
        n+=1
        href=re.search(r'href="([^"]+)"',c.group(0)).group(1) if c else ''
        want=HOST+'/' if pg=='index.html' else f'{HOST}/{pg}'
        if href!=want: e.append(f'{pg}: canonical {href} != {want}')
        titles.setdefault(t.group(1).strip(),[]).append(pg)
        if len(t.group(1))>90: e.append(f'{pg}: title very long ({len(t.group(1))})')
        k=re.search(r'<meta name="keywords" content="([^"]*)"',s)
        if k and len([x for x in k.group(1).split(',') if x.strip()])>12: e.append(f'{pg}: keyword list too long')
        if 'class="ruhi-semantic-footer"' not in s and pg not in('404.html','checkout.html'): e.append(f'{pg}: no semantic footer')
    for t,v in titles.items():
        if len(v)>1: e.append(f'duplicate title {t!r}: {v}')
    t=re.search(r'<title>(.*?)</title>',rd('index.html')).group(1)
    if 'RuhiWholesale' not in t or 'Ruhi Wholesale' not in t: e.append('index title lacks brand variants')
    return f'{n} indexable pages checked'

def p7(e):
    try: root=ET.parse('sitemap.xml').getroot()
    except Exception as ex: e.append(f'sitemap XML invalid: {ex}'); return
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}; locs=[]
    for u in root.findall('s:url',ns):
        loc=u.find('s:loc',ns); lm=u.find('s:lastmod',ns); cf=u.find('s:changefreq',ns)
        if loc is None or lm is None or cf is None: e.append('url missing loc/lastmod/changefreq'); continue
        if not re.fullmatch(r'\d{4}-\d\d-\d\d',lm.text): e.append('bad lastmod '+lm.text)
        if cf.text not in('always','hourly','daily','weekly','monthly','yearly','never'): e.append('bad changefreq')
        locs.append(loc.text)
    if len(locs)!=len(set(locs)): e.append('duplicate sitemap URLs')
    want=set()
    for pg in pages:
        s=rd(pg)
        if pg in('404.html','checkout.html') or pg.startswith('google') or re.search(r'<meta[^>]*robots[^>]*noindex',s): 
            u=HOST+'/'+pg
            if u in locs: e.append(f'noindex/utility page in sitemap: {pg}')
            continue
        want.add(HOST+'/' if pg=='index.html' else f'{HOST}/{pg}')
    for w in want-set(locs): e.append('indexable page missing from sitemap: '+w)
    for x in set(locs)-want: e.append('sitemap lists non-indexable: '+x)
    before=rd('sitemap.xml'); subprocess.run([sys.executable,'tools/generate_sitemap.py'],check=True,capture_output=True)
    if rd('sitemap.xml')!=before: e.append('generator not idempotent (output changed on re-run)')
    if 'Sitemap: '+HOST+'/sitemap.xml' not in rd('robots.txt'): e.append('robots.txt lacks Sitemap line')
    return f'{len(locs)} URLs; generator re-run is idempotent'

class Bal(HTMLParser):
    VOID={'meta','link','img','br','hr','input','source','area','base','col','embed','param','track','wbr'}
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in s.VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in s.VOID: return
        if t in s.st:
            while s.st and s.st[-1]!=t: s.err.append('unclosed <%s>'%s.st.pop())
            s.st.pop()
        else: s.err.append('stray </%s>'%t)
def p8(e):
    nscripts=0
    with tempfile.TemporaryDirectory() as td:
        for pg in pages:
            s=rd(pg)
            b=Bal(); b.feed(s)
            if b.err or b.st: e.append(f'{pg}: tag balance {b.err[:3]} open={b.st[:3]}')
            if s.count('<style')!=s.count('</style>'): e.append(f'{pg}: style tags unbalanced')
            for i,m in enumerate(re.finditer(r'<script(?P<a>[^>]*)>(?P<b>.*?)</script>',s,re.S)):
                a=m.group('a')
                if 'ld+json' in a or 'src=' in a or not m.group('b').strip(): continue
                nscripts+=1; mod='type="module"' in a
                f=os.path.join(td,f'{pg}-{i}.{"mjs" if mod else "js"}'); open(f,'w').write(m.group('b'))
                r=subprocess.run(['node','--check',f],capture_output=True,text=True)
                if r.returncode: e.append(f'{pg}: JS syntax error in script #{i}: {r.stderr.strip().splitlines()[0:2]}')
        f=os.path.join(td,'fb.mjs'); open(f,'w').write(rd('assets/js/firebase-cart.js'))
        if subprocess.run(['node','--check',f],capture_output=True).returncode: e.append('assets/js/firebase-cart.js syntax error')
    for fcss in ('assets/css/pdp.css','assets/css/site-extras.css'):
        c=rd(fcss)
        if c.count('{')!=c.count('}'): e.append(f'{fcss}: unbalanced braces')
    for pg in pages:
        if cat(pg):
            s=rd(pg)
            if 'assets/css/pdp.css' not in s or 'assets/js/firebase-cart.js' not in s: e.append(f'{pg}: not using shared css/js')
            if '<style id="polish"' in s or 'import { initializeApp }' in s: e.append(f'{pg}: leftover inline duplicate')
    return f'{nscripts} inline scripts + extracted JS syntax-checked with node; HTML tag balance on {len(pages)} pages'

for i,(t,f) in enumerate([('1 Structure & hygiene',p1),('2 Links, assets & absolute URLs',p2),('3 Category rules & badges',p3),('4 Size data consistency',p4),('5 JSON-LD schema',p5),('6 Titles / canonicals / meta / footer',p6),('7 Sitemap & generator',p7),('8 Code syntax (JS/CSS/HTML)',p8)],1):
    run(t,f)
bad=[r for r in results if r[1]]
print('\nRESULT:', 'ALL 8 PASSES CLEAN' if not bad else f'{len(bad)} PASS(ES) FAILED')
sys.exit(1 if bad else 0)

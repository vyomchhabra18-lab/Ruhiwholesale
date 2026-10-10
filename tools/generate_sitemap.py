#!/usr/bin/env python3
"""Regenerate sitemap.xml from the real, indexable pages in the site root.

Run from anywhere:  python3 tools/generate_sitemap.py
- Lists only pages that exist, are indexable (no noindex) and are their own canonical.
- <lastmod> only changes when a page's content changes (tracked in tools/.sitemap-state.json).
- <changefreq> is set by page type.
Deliberately does NOT invent URLs for keyword/typo aliases: doorway/alias pages that
do not exist (or that duplicate real pages) violate Google and Bing spam policies.
"""
import os, re, glob, json, hashlib, datetime, html
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
HOST='https://ruhiwholesale.store'
STATE=os.path.join(ROOT,'tools','.sitemap-state.json')
SKIP={'404.html','checkout.html','BingSiteAuth.xml'}
def freq(n):
    if n=='index.html': return 'daily'
    if n.startswith('wholesale-') or n=='imported-tensils.html': return 'weekly'
    if re.match(r'(indian|poly|imported)-',n): return 'monthly'
    if n in('privacy-policy.html','terms.html'): return 'yearly'
    return 'monthly'
def url_for(n): return HOST+'/' if n=='index.html' else f'{HOST}/{n}'
def main(today=None):
    today=today or datetime.date.today().isoformat()
    state=json.load(open(STATE)) if os.path.exists(STATE) else {}
    rows=[]; skipped=[]
    for p in sorted(glob.glob(os.path.join(ROOT,'*.html'))):
        n=os.path.basename(p)
        s=open(p,encoding='utf-8').read()
        if n in SKIP or n.startswith('google') or re.search(r'<meta name="robots" content="[^"]*noindex',s):
            skipped.append(n); continue
        m=re.search(r'<link[^>]*rel="canonical"[^>]*>',s); m=re.search(r'href="([^"]+)"',m.group(0)) if m else None
        if not m or m.group(1)!=url_for(n):
            skipped.append(n+' (canonical mismatch)'); continue
        h=hashlib.sha256(s.encode()).hexdigest()
        if state.get(n,{}).get('hash')!=h: state[n]={'hash':h,'lastmod':today}
        rows.append((n,state[n]['lastmod']))
    # index first, then categories, then products
    order=lambda r:(0 if r[0]=='index.html' else 1 if r[0].startswith('wholesale-') else 2 if r[0] in('about.html','services.html','contact.html','imported-tensils.html') else 3 if re.match(r'(indian|poly|imported)-',r[0]) else 4, r[0])
    rows.sort(key=order)
    out=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for n,lm in rows:
        out+=['  <url>',f'    <loc>{html.escape(url_for(n))}</loc>',f'    <lastmod>{lm}</lastmod>',f'    <changefreq>{freq(n)}</changefreq>','  </url>']
    out.append('</urlset>')
    open(os.path.join(ROOT,'sitemap.xml'),'w',encoding='utf-8',newline='\n').write('\n'.join(out)+'\n')
    json.dump(state,open(STATE,'w'),indent=1,sort_keys=True)
    print(f'sitemap.xml: {len(rows)} URLs written; skipped: {skipped}')
if __name__=='__main__': main()

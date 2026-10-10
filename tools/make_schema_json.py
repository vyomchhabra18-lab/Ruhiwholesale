#!/usr/bin/env python3
"""Rewrite SCHEMA_ORG_JSONLD.json from the same graph embedded in the pages (single source of truth: index.html)."""
import re, json, os
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
s=open(os.path.join(ROOT,'index.html'),encoding='utf-8').read()
m=re.search(r'<script type="application/ld\+json" id="ruhi-organization-schema">(.*?)</script>',s,re.S)
d=json.loads(m.group(1))
open(os.path.join(ROOT,'SCHEMA_ORG_JSONLD.json'),'w',encoding='utf-8').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('SCHEMA_ORG_JSONLD.json updated;',len(d['@graph'][0]['alternateName']),'alternateName entries')

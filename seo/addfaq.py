#!/usr/bin/env python3
"""Append FAQ items to a page's meta: python3 seo/addfaq.py file.html 'Q?' 'A.' ['Q2?' 'A2.']"""
import json, re, sys
f = sys.argv[1]; s = open(f).read(); m = re.match(r'<!--meta\s*([\s\S]*?)-->', s); meta = json.loads(m.group(1))
it = sys.argv[2:]
for q, a in zip(it[::2], it[1::2]): meta.setdefault('faq', []).append({"q": q, "a": a})
open(f, 'w').write('<!--meta ' + json.dumps(meta, indent=2, ensure_ascii=False) + ' -->' + s[m.end():])

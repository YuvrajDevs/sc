#!/usr/bin/env python3
"""Inserts the shared 'Everything Sealcloak does' capabilities block before {{cta}} in compare pages that lack it."""
import re, sys, glob
src = open('content/compare/sealcloak-vs-keepsafe.html').read()
blk = re.search(r'        <!--shared-->[\s\S]*?<!--/shared-->\n', src).group(0)
for f in sys.argv[1:] or glob.glob('content/compare/sealcloak-vs-*.html'):
    s = open(f).read()
    if '<!--shared-->' in s: continue
    k = s.index('        {{cta}}'); open(f, 'w').write(s[:k] + blk + '\n' + s[k:]); print('added', f)

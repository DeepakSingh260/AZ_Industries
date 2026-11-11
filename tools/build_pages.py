#!/usr/bin/env python3
"""
Build the static product pages and sitemap.xml from catalogue/data.js.

    python3 tools/build_pages.py

Writes
  products/index.html                      the catalogue index
  products/<group>/index.html              one page per product group
  products/<group>/<product>/index.html    one page per product
  sitemap.xml                              every page above plus the home page

Everything under products/ is generated. Do not edit those files by hand:
edit catalogue/data.js and run this script again. The page URLs are derived
from the group and product names (lower-case, words joined by hyphens), and
index.html uses the same rule to link to them, so renaming a product changes
its URL.

catalogue/data.js is read with the system JavaScript engine (osascript), so
this runs on macOS without Node.
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.azindustrialsolutions.com'
BRAND = 'AZ Industrial Solutions'
SITE_NAME = 'AZ Industrial Solutions & Automation'
DATA = os.path.join(ROOT, 'catalogue', 'data.js')
OUT = os.path.join(ROOT, 'products')
CSS_VER = '1'
TODAY = datetime.date.today().isoformat()
RATINGS = ['6 kg/cm² (PN 6)', '10 kg/cm² (PN 10)', 'Not sure']
RATING_TEXT = '6 kg/cm² (PN 6) and 10 kg/cm² (PN 10)'


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(s):
    # Must match slugify() in index.html.
    return re.sub(r'[^a-z0-9]+', '-', str(s).lower()).strip('-')


def pad(n):
    return '%02d' % int(n)


def load_catalogue():
    js = ('ObjC.import("Foundation");'
          'var s=$.NSString.stringWithContentsOfFileEncodingError(%s,4,null).js;'
          'var window={};eval(s);JSON.stringify(window.AZ_CATALOGUE)') % json.dumps(DATA)
    r = subprocess.run(['osascript', '-l', 'JavaScript', '-e', js], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('Could not read catalogue/data.js: ' + r.stderr.strip())
    return json.loads(r.stdout)


# ---------- data helpers ----------

def inch_label(cat, v):
    for x in cat['sizesIN']:
        if x['v'] == v:
            return x['l']
    return str(v) + '"'


def size_values(cat, p):
    s = p.get('size')
    if not s:
        return []
    if s['unit'] == 'mm':
        return ['%d mm OD' % v for v in cat['sizesMM'] if s['min'] <= v <= s['max']]
    return [x['l'] for x in cat['sizesIN'] if s['min'] <= x['v'] <= s['max']]


def size_text(cat, p):
    s = p.get('size')
    if not s:
        return ''
    if s['unit'] == 'mm':
        return '%d to %d mm OD' % (s['min'], s['max'])
    return '%s to %s' % (inch_label(cat, s['min']), inch_label(cat, s['max']))


def size_list_text(cat, p):
    vals = size_values(cat, p)
    if not vals:
        return ''
    if p['size']['unit'] == 'mm':
        return ', '.join(v.replace(' mm OD', '') for v in vals) + ' mm OD'
    return ', '.join(vals)


def base_name(name):
    return re.sub(r'^(HDPE|PPH|PPRC|PP|PVDF)\s+', '', name).strip().lower()


# One paragraph per fitting type, matched against the product name (first match wins).
# A product can override this with its own `about` field in data.js.
TYPE_NOTES = [
    (r'tapping tee', 'A tapping tee is electrofusion-welded onto a live main and has a built-in cutter, so a branch can be added under pressure without shutting the line down.'),
    (r'saddle', 'A branch saddle is electrofusion-welded onto the side of a pipe to add a branch without cutting the main.'),
    (r'short neck stub end', 'A short neck stub end is butt-fused to the end of the pipe and carries a loose backing flange, giving a bolted, demountable joint to valves, pumps, tanks and metal flanges. The short neck suits standard butt-fusion machines and keeps the overall length down.'),
    (r'long neck stub end|stub end \(180|^long neck$', 'A long neck stub end is butt-fused to the pipe and used with a loose backing flange to make a bolted joint. The longer neck gives room for the clamps of a butt-fusion machine and suits larger diameters.'),
    (r'slip-on flange', 'A slip-on (backing) flange slides over the pipe behind a stub end or core flange and takes the bolt load, so the plastic part is never under bolt stress. It is drilled to standard flange patterns for bolting to valves, pumps and steel pipework.'),
    (r'blind flange', 'A blind flange closes the end of a flanged line or an unused branch. It can be removed later to extend the line or for inspection.'),
    (r'threaded flange', 'A threaded flange has an internal thread for connecting threaded pipe or fittings on one side and a flange face on the other.'),
    (r'sandwich flange', 'A sandwich flange is bolted between two mating flanges to make a branch or an instrument take-off without cutting a tee into the line.'),
    (r'paddle flange', 'A paddle (puddle) flange is fused onto the pipe where it passes through a concrete wall, tank floor or chamber. The paddle acts as a water stop and anchors the pipe in the concrete.'),
    (r'weld neck flange', 'A weld neck flange is fused directly onto the pipe. It gives a stiffer joint than a stub end with backing ring, for lines with higher loads or vibration.'),
    (r'core flange', 'A core flange is fused to the pipe and used with a loose backing ring, in the same way as a stub end, to make a bolted joint to valves and equipment.'),
    (r'ms powder coated flange', 'A mild-steel backing flange, powder coated against corrosion, used behind a stub end or core flange to take the bolt load.'),
    (r'tail piece with flange|tail piece, flanged', 'A flanged tail piece (flange adaptor) is fused into the plastic line and bolts directly to a flanged metal fitting or valve.'),
    (r'tail piece', 'A tail piece (flange adaptor) connects plastic pipe to a flanged metal fitting or valve, with a plain end for fusion on one side and a flange face on the other.'),
    (r'reducing tee', 'A reducing tee makes a branch of a smaller size off the main line in one fitting, instead of a tee plus a reducer.'),
    (r'thread tee', 'A threaded tee makes a branch with a threaded outlet, for connecting valves, instruments or metal pipework directly into a plastic line.'),
    (r'thread elbow', 'A threaded elbow turns the line through 90 degrees and ends in a thread, for connecting to taps, valves or metal pipework.'),
    (r'thread adaptor', 'A threaded adaptor joins plastic pipe to threaded metal fittings, valves and equipment. Male and female versions are available.'),
    (r'socket \(threaded\)', 'A threaded socket joins socket-fusion pipe to a threaded metal fitting or valve.'),
    (r'socket bend \(threaded\)', 'A threaded socket bend turns the line through 90 degrees and ends in a thread for connecting to metal pipework or a valve.'),
    (r'socket tee \(threaded\)', 'A threaded socket tee makes a branch with a threaded outlet for a valve, instrument or metal connection.'),
    (r'socket tee', 'A socket tee makes a same-size branch in a socket-fusion line.'),
    (r'socket bend', 'A socket bend turns a socket-fusion line through 90 degrees.'),
    (r'^socket', 'A plain socket (coupler) joins two lengths of pipe of the same size in a socket-fusion line.'),
    (r'ball valve', 'A ball valve isolates a section of the line with a quarter turn. This one is fused directly into the pipe, with no threaded joints to leak.'),
    (r'welding machine die', 'Heating dies (bushes) for a socket-fusion welding machine, sized to the pipe outside diameter. One pair is needed for each pipe size.'),
    (r'\btee\b', 'A tee makes a branch of the same size off a main line and carries full line pressure. Choose the pressure class to match the pipe.'),
    (r'elbow 45|bend 45', 'A 45 degree bend changes the direction of the line by 45 degrees, for gentle offsets and where two 45 degree bends are preferred to one 90 degree bend for lower pressure loss.'),
    (r'\bbend\b|\belbow\b', 'A 90 degree bend (elbow) changes the direction of the line. The pressure class should match the pipe, usually PN 6 or PN 10.'),
    (r'reducer', 'A reducer joins two pipe sizes in line, for example 110 mm down to 90 mm, where the flow or the equipment connection changes size.'),
    (r'end cap', 'An end cap seals the end of a line, either permanently or for pressure testing before the line is extended.'),
    (r'union', 'A union is a three-piece joint that can be unscrewed, so a section of pipe, a valve or a piece of equipment can be removed without cutting the line.'),
    (r'coupler', 'A coupler joins two lengths of pipe of the same size in line.'),
]


def type_note(p):
    if p.get('about'):
        return p['about']
    n = p['name'].lower()
    for pat, text in TYPE_NOTES:
        if re.search(pat, n):
            return text
    sys.stderr.write('No type note for: %s\n' % p['name'])
    return ''


def seo_name(f, p):
    """Product name with the material in front, so titles and headings say what it is made of."""
    name, fid = p['name'], f['id']
    if fid == 'ef':
        return name if 'Electrofusion' in name else 'Electrofusion ' + name
    if fid == 'spigot':
        return 'HDPE ' + name if 'Spigot' in name else 'HDPE Spigot ' + name
    mat = material_short(f)
    return name if name.startswith(mat + ' ') else mat + ' ' + name


def material_short(f):
    return re.sub(r'\s*\(.*$', '', f.get('material', f['name'])).split(',')[0].strip()


def prepare(cat):
    live = next(c for c in cat['categories'] if c.get('status') == 'live')
    fams = live['families']
    seen = set()
    for f in fams:
        f['slug'] = slugify(f['name'])
        f['url'] = '/products/%s/' % f['slug']
        if f['slug'] in seen:
            sys.exit('Duplicate group URL: ' + f['url'])
        seen.add(f['slug'])
        f['thumb'] = '/catalogue/img/%s-%s.jpg' % (f['id'], pad(f['products'][0]['n']))
        f['about'] = f.get('about') or f['desc']
        f['material'] = f.get('material') or f['name']
        pseen = set()
        for p in f['products']:
            p['slug'] = slugify(p['name'])
            if p['slug'] in pseen:
                sys.exit('Duplicate product URL in %s: %s (give one of them a different name)' % (f['name'], p['slug']))
            pseen.add(p['slug'])
            p['url'] = f['url'] + p['slug'] + '/'
            p['pkey'] = '%s-%s' % (f['id'], p['n'])
            p['img'] = '/catalogue/img/%s-%s.jpg' % (f['id'], pad(p['n']))
            p['fam'] = f
            if not os.path.exists(os.path.join(ROOT, p['img'].lstrip('/'))):
                sys.exit('Missing image: ' + p['img'])
        mins = [p['size']['min'] for p in f['products'] if p.get('size') and p['size']['unit'] == 'mm']
        maxs = [p['size']['max'] for p in f['products'] if p.get('size') and p['size']['unit'] == 'mm']
        f['range'] = '%d to %d mm OD' % (min(mins), max(maxs)) if mins else ''
    return live, fams


# ---------- page chrome ----------

CHEVRON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>'
BURGER = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'
LINKEDIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'


def nav_html(fams, total):
    items = ['<a href="/products/"><strong>All pipe fittings</strong><small>%d products</small></a>' % total]
    for f in fams:
        items.append('<a href="%s"><strong>%s</strong><small>%d products</small></a>' % (f['url'], esc(f['name']), len(f['products'])))
    return '''<nav class="site-nav">
  <div class="nav-inner">
    <a class="nav-logo" href="/">
      <img src="/logo/az-logo-mark.png" alt="AZ Industrial Solutions &amp; Automation logo">
      <div><div class="nav-logo-name">AZ Industrial</div><div class="nav-logo-sub">Solutions &amp; Automation</div></div>
    </a>
    <ul class="nav-links" id="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/#services">Services</a></li>
      <li class="nav-dd">
        <a href="/products/" class="nav-active" aria-haspopup="true">Industrial Products %s</a>
        <div class="nav-dd-menu"><div class="nav-dd-inner">%s</div></div>
      </li>
      <li><a href="/#industries">Industries</a></li>
      <li><a href="/#about">About</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li><a href="/#quote" class="nav-quote" id="nav-quote" hidden>Quote list <b id="nav-quote-n">0</b></a></li>
      <li><a href="/#contact" class="nav-btn">Get a Quote</a></li>
    </ul>
    <button class="nav-burger" id="nav-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">%s</button>
  </div>
</nav>''' % (CHEVRON, ''.join(items), BURGER)


def footer_html(fams):
    groups = ''.join('<li><a href="%s">%s</a></li>' % (f['url'], esc(f['name'])) for f in fams)
    return '''<footer>
  <div class="footer-inner">
    <div class="footer-top">
      <div>
        <img src="/logo/az-logo-mark.png" alt="AZ Industrial Solutions &amp; Automation logo" style="height:48px;width:auto;filter:invert(1) brightness(10);display:block;margin-bottom:1rem;">
        <div class="footer-logo-name">AZ Industrial Solutions &amp; Automation</div>
        <p class="footer-tagline">Customized industrial consulting solutions driving efficiency and growth across industries.</p>
        <div class="footer-contact"><a href="mailto:info@azindustrialsolutions.com">info@azindustrialsolutions.com</a></div>
      </div>
      <div>
        <div class="footer-col-head">Quick Links</div>
        <ul class="footer-links">
          <li><a href="/#services">Services</a></li>
          <li><a href="/products/">Industrial Products</a></li>
          <li><a href="/#industries">Industries</a></li>
          <li><a href="/#about">About Us</a></li>
          <li><a href="/#contact">Contact</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-head">Product Groups</div>
        <ul class="footer-links">%s</ul>
      </div>
      <div>
        <div class="footer-col-head">Contact</div>
        <ul class="footer-links">
          <li><a href="mailto:info@azindustrialsolutions.com">info@azindustrialsolutions.com</a></li>
          <li><a href="https://www.linkedin.com/company/smart-iwos/" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;gap:.4rem;">%sLinkedIn</a></li>
          <li><a href="/#contact">Request a Quote</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 AZ Industrial Solutions &amp; Automation. All rights reserved.</span>
      <span>Privacy Policy &middot; Terms of Service</span>
    </div>
  </div>
</footer>
<div class="qbar" id="qbar" hidden><div class="qbar-inner container"><span class="qbar-text"><b id="qbar-n">0</b> <span id="qbar-w">items</span> in your quote list</span><a class="qbar-view" href="/#quote">View list</a><a class="btn btn-brand" href="/#contact">Send quote request</a></div></div>
<div class="toast" id="toast" role="status" aria-live="polite"><span id="toast-msg"></span><a href="/#quote">View list</a></div>
<script src="/catalogue/pages.js?v=%s"></script>''' % (groups, LINKEDIN, CSS_VER)


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace('</', '<\\/')


def layout(title, desc, path, og_type, og_image, ld, body, fams, total, img_alt=''):
    url = SITE + path
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Generated by tools/build_pages.py from catalogue/data.js. Do not edit by hand. -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="%(og_type)s">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(og_image)s">
<meta property="og:image:width" content="720">
<meta property="og:image:height" content="346">
<meta property="og:image:alt" content="%(img_alt)s">
<meta property="og:site_name" content="%(site_name)s">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og_image)s">
<link rel="icon" type="image/png" href="/logo/az-icon-64.png">
<link rel="apple-touch-icon" href="/logo/az-icon-180.png">
<meta name="theme-color" content="#1a3a6b">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/catalogue/pages.css?v=%(css_ver)s">
<script type="application/ld+json">
%(ld)s
</script>
</head>
<body>
%(nav)s
<main>
%(body)s
</main>
%(footer)s
</body>
</html>
''' % dict(title=esc(title), desc=esc(desc), url=url, og_type=og_type, og_image=SITE + og_image,
           site_name=esc(SITE_NAME), css_ver=CSS_VER, ld=ld, nav=nav_html(fams, total), body=body, footer=footer_html(fams), img_alt=esc(img_alt))


def crumbs_html(items):
    # items: list of (name, path or None for current)
    out = []
    for name, path in items:
        if path is None:
            out.append('<span class="cur" aria-current="page">%s</span>' % esc(name))
        else:
            out.append('<a href="%s">%s</a>' % (path, esc(name)))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">&rsaquo;</span>'.join(out) + '</nav>'


def crumbs_ld(items):
    return {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': name, 'item': SITE + (path if path else '')}
            for i, (name, path) in enumerate(items)
        ]
    }


def rel_card(p, by_group=False):
    top, sub = (p['fam']['name'], p['name'] + ' \u00b7 ' + p['spec']) if by_group else (p['name'], p['spec'])
    return ('<a class="rel" href="%s"><img src="%s" alt="" loading="lazy" width="88" height="42"><div><b>%s</b><small>%s</small></div></a>'
            % (p['url'], p['img'], esc(top), esc(sub)))


def cta_html(h, p):
    return ('<div class="cta-banner"><div class="container"><h2>%s</h2><p>%s</p>'
            '<a class="btn btn-white btn-lg" href="/#contact">Request a Quotation</a></div></div>' % (esc(h), esc(p)))


# ---------- pages ----------

def product_page(cat, live, fams, total, f, p):
    mat = f['material']
    mat_s = material_short(f)
    sizes = size_values(cat, p)
    stext = size_text(cat, p)
    sname = seo_name(f, p)
    srange = stext.replace(' to ', '\u2013').replace(' mm OD', ' mm')
    title = '%s%s | %s' % (sname, (', ' + srange) if srange else '', BRAND)
    lead = '%s%s, made of %s. Supplied across Canada by %s. Choose the size and quantity you need, add it to your quote list, and we reply with pricing, availability and lead time.' % (
        sname, (' in sizes from ' + stext) if stext else '', mat, BRAND)
    desc = '%s%s, supplied across Canada by %s. Request a quote online for pricing, availability and lead time.' % (
        sname, (', ' + stext) if stext else '', BRAND)
    note = type_note(p)

    crumbs = [('Home', '/'), ('Industrial Products', '/products/'), (f['name'], f['url']), (p['name'], None)]

    if sizes:
        opts = ''.join('<option value="%s">%s</option>' % (esc(v), esc(v)) for v in sizes)
        opts += '<option value="Other / not sure">Other / not sure (describe in notes)</option>'
    else:
        opts = '<option value="Standard">Standard</option>'
    rating = ''
    if p.get('rated'):
        rating = ('<div class="form-group"><label class="form-label" for="rating">Pressure rating</label>'
                  '<select class="form-select sel" id="rating" name="rating">%s</select></div>'
                  % ''.join('<option>%s</option>' % esc(r) for r in RATINGS))

    facts = [('Material', mat), ('Size range', p['spec'])]
    if sizes:
        facts.append(('Sizes', size_list_text(cat, p) + '. Other sizes on request.'))
    if p.get('rated'):
        facts.append(('Pressure class', RATING_TEXT))
    facts.append(('Catalogue ref.', '%s-%s' % (f['num'], pad(p['n']))))
    facts.append(('Supply', 'Quoted per size and quantity. Delivered across Canada.'))
    facts_html = ''.join('<dt>%s</dt><dd>%s</dd>' % (esc(k), esc(v)) for k, v in facts)

    siblings = [q for q in f['products'] if q is not p]
    others = [q for g in fams if g is not f for q in g['products'] if base_name(q['name']) == base_name(p['name'])]

    body = '''<div class="container">
%(crumbs)s
<article class="pd">
  <div class="pd-media"><img src="%(img)s" alt="%(alt)s" width="720" height="346" fetchpriority="high" decoding="async"></div>
  <div class="pd-info">
    <a class="pd-fam" href="%(furl)s">%(fnum)s &middot; %(fname)s</a>
    <h1>%(sname)s</h1>
    <p class="pd-lead">%(lead)s</p>
    <dl class="facts">%(facts)s</dl>
    <form class="pd-add" id="add-form" data-pkey="%(pkey)s" data-name="%(name)s" data-fam="%(fname)s" data-img="%(img)s">
      <div class="pd-add-h">Add to your quote list</div>
      <div class="pd-row">
        <div class="form-group"><label class="form-label" for="size">Size</label><select class="form-select sel" id="size" name="size">%(opts)s</select></div>
        %(rating)s
        <div class="form-group"><label class="form-label" for="qty">Quantity</label><div class="qty"><button type="button" data-d="-1" aria-label="Decrease quantity">&minus;</button><input id="qty" name="qty" type="number" min="1" value="1"><button type="button" data-d="1" aria-label="Increase quantity">+</button></div></div>
      </div>
      <div class="form-group"><label class="form-label" for="note">Notes <span>(optional)</span></label><input class="form-input" id="note" name="note" placeholder="e.g. SDR 11, needed by March, drawing to follow"></div>
      <button class="btn btn-brand btn-lg" type="submit" id="add-btn">Add to quote list</button>
      <p class="m-help">No payment is taken on this site. We email you a quotation with pricing, availability and delivery time.</p>
    </form>
  </div>
</article>
</div>
<section class="sec" style="border-top:1px solid var(--bdr);"><div class="container narrow">
  <h2>About the %(sname)s</h2>
  %(note)s
  <h3 class="sub-h">About %(fname_l)s</h3>
  <p class="sub">%(about)s</p>
</div></section>
<section class="sec"><div class="container">
  <div class="sec-head"><div><h2>Other %(fname_l)s</h2><p class="sub">%(nsib)d more products in this group.</p></div><a class="sec-link" href="%(furl)s">See the whole group</a></div>
  <div class="rel-grid">%(sibs)s</div>
</div></section>
%(others)s
%(cta)s''' % dict(
        crumbs=crumbs_html(crumbs), img=p['img'], alt=esc('%s, %s' % (sname, p['spec'])), furl=f['url'], fnum=f['num'], sname=esc(sname),
        note=('<p class="sub">%s</p>' % esc(note)) if note else '',
        fname=esc(f['name']), fname_l=esc(f['name'][0].upper() + f['name'][1:]) if False else esc(f['name']),
        name=esc(p['name']), lead=esc(lead), facts=facts_html, pkey=p['pkey'], opts=opts, rating=rating,
        about=esc(f['about']), nsib=len(siblings), sibs=''.join(rel_card(q) for q in siblings),
        others=('<section class="sec"><div class="container"><div class="sec-head"><div><h2>%s in other materials</h2><p class="sub">The same fitting from our other product groups.</p></div></div><div class="rel-grid">%s</div></div></section>'
                % (esc(p['name']), ''.join(rel_card(q, True) for q in others))) if others else '',
        cta=cta_html('Need a size that is not listed?', 'Tell us the material, size and quantity, or send a drawing, and we will quote it.'))

    product = {
        '@type': 'Product',
        '@id': SITE + p['url'] + '#product',
        'name': sname,
        'sku': 'AZ-%s-%s' % (f['id'].upper(), pad(p['n'])),
        'url': SITE + p['url'],
        'image': [SITE + p['img']],
        'description': desc,
        'category': 'Industrial Pipe Fittings > ' + f['name'],
        'material': mat,
        'additionalProperty': [{'@type': 'PropertyValue', 'name': 'Size range', 'value': p['spec']}] +
                              ([{'@type': 'PropertyValue', 'name': 'Pressure class', 'value': 'PN 6 / PN 10'}] if p.get('rated') else []),
    }
    ld = jsonld({'@context': 'https://schema.org', '@graph': [crumbs_ld(crumbs), product]})
    return layout(title, desc, p['url'], 'product', p['img'], ld, body, fams, total, img_alt=sname)


def family_page(cat, live, fams, total, f):
    n = len(f['products'])
    title = '%s Supplier in Canada, %d Products | %s' % (f['name'], n, BRAND)
    desc = '%s in %s, %s. %d products supplied across Canada by %s. See sizes and request a quote online.' % (
        f['name'], f['material'], f['range'] or 'a range of sizes', n, BRAND)
    crumbs = [('Home', '/'), ('Industrial Products', '/products/'), (f['name'], None)]
    cards = ''.join('''<a class="pc" href="%s">
    <div class="pc-img"><img loading="lazy" src="%s" alt="%s" width="720" height="346"></div>
    <div class="pc-body"><div class="pc-n">%s</div><div class="pc-name">%s</div><div class="pc-spec">%s</div><div class="pc-go">View product</div></div></a>'''
                    % (p['url'], p['img'], esc(p['name']), pad(p['n']), esc(p['name']), esc(p['spec'])) for p in f['products'])
    others = ''.join('<a class="rel" href="%s"><img src="%s" alt="" loading="lazy" width="88" height="42"><div><b>%s</b><small>%d products</small></div></a>'
                     % (g['url'], g['thumb'], esc(g['name']), len(g['products'])) for g in fams if g is not f)
    body = '''<div class="page-hero"><div class="container">
  <div class="eyebrow eyebrow-blue" style="justify-content:center;">Industrial Products &middot; %(num)s</div>
  <h1>%(name)s</h1>
  <p>%(about)s</p>
  <div class="hero-meta"><span><b>%(n)d</b> products</span>%(range)s<span>Delivered <b>across Canada</b></span></div>
</div></div>
<div class="container">
%(crumbs)s
<div class="sec" style="padding-top:.75rem;"><div class="prod-grid">%(cards)s</div></div>
</div>
<section class="sec" style="border-top:1px solid var(--bdr);"><div class="container">
  <div class="sec-head"><div><h2>Other product groups</h2><p class="sub">%(total)d products in %(nf)d groups.</p></div><a class="sec-link" href="/products/">All industrial products</a></div>
  <div class="rel-grid">%(others)s</div>
</div></section>
%(cta)s''' % dict(num=f['num'], name=esc(f['name']), about=esc(f['about']), n=n,
                   range=('<span><b>%s</b></span>' % esc(f['range'])) if f['range'] else '',
                   crumbs=crumbs_html(crumbs), cards=cards, total=total, nf=len(fams), others=others,
                   cta=cta_html('Have a product list already?', 'Send us the fitting types, sizes and quantities, or attach your bill of materials, and we will come back with a quotation.'))
    coll = {
        '@type': 'CollectionPage',
        'name': f['name'],
        'url': SITE + f['url'],
        'description': desc,
        'mainEntity': {
            '@type': 'ItemList',
            'numberOfItems': n,
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': p['name'], 'url': SITE + p['url']} for i, p in enumerate(f['products'])]
        }
    }
    ld = jsonld({'@context': 'https://schema.org', '@graph': [crumbs_ld(crumbs), coll]})
    return layout(title, desc, f['url'], 'website', f['thumb'], ld, body, fams, total, img_alt=f['name'])


def index_page(cat, live, fams, total):
    title = 'Industrial Pipe Fittings Supplier in Canada | %s' % BRAND
    desc = '%d industrial pipe fittings in %d product groups: HDPE, electrofusion, spigot, PPH, PPRC, PP and PVDF. Supplied across Canada by %s. Build a quote list online.' % (total, len(fams), BRAND)
    crumbs = [('Home', '/'), ('Industrial Products', None)]
    cards = ''.join('''<a class="fam-card" href="%s">
    <div class="thumb"><img src="%s" alt="" loading="lazy" width="720" height="346"></div>
    <div class="num">%s</div><div class="name">%s</div><div class="count">%d products%s</div>
    <div class="desc">%s</div><div class="more">View products</div></a>''' % (
        f['url'], f['thumb'], f['num'], esc(f['name']), len(f['products']), (' &middot; ' + esc(f['range'])) if f['range'] else '', esc(f['desc'])) for f in fams)
    rows = ''.join('<tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (f['url'], esc(f['name']), esc(f['material']), esc(f['about'])) for f in fams)
    body = '''<div class="page-hero" style="padding-bottom:6.5rem;"><div class="container">
  <div class="eyebrow eyebrow-blue" style="justify-content:center;">Industrial Products</div>
  <h1>%(title)s</h1>
  <p>%(intro)s</p>
  <div class="hero-meta"><span><b>%(total)d</b> products</span><span><b>%(nf)d</b> product groups</span><span>Delivered <b>across Canada</b></span></div>
</div></div>
<div class="container"><div class="fam-cards">%(cards)s</div></div>
<div class="container">%(crumbs)s</div>
<section class="sec"><div class="container narrow">
  <h2>How to order</h2>
  <p class="sub">Open a product, choose the size and quantity, and add it to your quote list. The list follows you around the site. When you are done, send it from the contact page and we reply with a written quotation. No payment is taken on this site.</p>
  <p style="margin-top:1.25rem;"><a class="btn btn-brand" href="/#products">Browse all %(total)d products on one page</a></p>
</div></section>
<section class="sec"><div class="container narrow">
  <h2>Choosing a material</h2>
  <p class="sub">Each group below is one material or joining method. Not sure which one your line needs? Add the closest product to your list and describe the service in the notes.</p>
  <div class="mat-wrap"><table class="mat-table"><thead><tr><th>Group</th><th>Material</th><th>Typical use</th></tr></thead><tbody>%(rows)s</tbody></table></div>
</div></section>
%(cta)s''' % dict(title=esc(live.get('title', 'Industrial Pipe Fittings')), intro=esc(live.get('intro', '')), total=total, nf=len(fams),
                   cards=cards, crumbs=crumbs_html(crumbs), rows=rows,
                   cta=cta_html('Have a product list already?', 'Send us the fitting types, sizes and quantities, or attach your bill of materials, and we will come back with a quotation.'))
    coll = {
        '@type': 'CollectionPage',
        'name': live.get('title', 'Industrial Pipe Fittings'),
        'url': SITE + '/products/',
        'description': desc,
        'mainEntity': {
            '@type': 'ItemList',
            'numberOfItems': len(fams),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': f['name'], 'url': SITE + f['url']} for i, f in enumerate(fams)]
        }
    }
    ld = jsonld({'@context': 'https://schema.org', '@graph': [crumbs_ld(crumbs), coll]})
    return layout(title, desc, '/products/', 'website', fams[0]['thumb'], ld, body, fams, total, img_alt='Industrial pipe fittings')


def write(path, text):
    full = os.path.join(ROOT, path.lstrip('/'), 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    cat = load_catalogue()
    live, fams = prepare(cat)
    total = sum(len(f['products']) for f in fams)
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    urls = [('/', None, None)]
    write('/products/', index_page(cat, live, fams, total))
    urls.append(('/products/', None, None))
    for f in fams:
        write(f['url'], family_page(cat, live, fams, total, f))
        urls.append((f['url'], f['thumb'], f['name']))
        for p in f['products']:
            write(p['url'], product_page(cat, live, fams, total, f, p))
            urls.append((p['url'], p['img'], seo_name(f, p)))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')
        for u, img, name in urls:
            fh.write('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n' % (SITE, u, TODAY))
            if img:
                fh.write('    <image:image>\n      <image:loc>%s%s</image:loc>\n      <image:title>%s</image:title>\n    </image:image>\n' % (SITE, img, esc(name)))
            fh.write('  </url>\n')
        fh.write('</urlset>\n')
    print('Wrote %d pages (%d groups, %d products) and sitemap.xml with %d URLs.' % (len(urls) - 1, len(fams), total, len(urls)))


if __name__ == '__main__':
    main()

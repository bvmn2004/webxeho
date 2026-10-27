"""Render the 29 editorial pages from content/pages.json using their existing shells.

Python standard library only. Does not touch index.html, booking code or styling.
Run without arguments to render; use --check to detect stale generated pages.
"""
from pathlib import Path
import argparse,html,json,re,sys,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
BASE='https://laixehodanang.me/'
REGIONS={
    'lai-xe-ho-hai-chau-da-nang.html':'Hải Châu',
    'lai-xe-ho-son-tra-da-nang.html':'Sơn Trà',
    'lai-xe-ho-cam-le-da-nang.html':'Cẩm Lệ – Hòa Xuân',
    'lai-xe-ho-thanh-khe-da-nang.html':'Thanh Khê',
    'lai-xe-ho-ngu-hanh-son-da-nang.html':'Ngũ Hành Sơn',
    'lai-xe-ho-lien-chieu-da-nang.html':'Liên Chiểu',
}
SERVICES={
    'lai-xe-ho-o-to-da-nang.html','lai-xe-ho-xe-may-da-nang.html',
    'lai-xe-ho-sau-tiec-da-nang.html','dat-tai-xe-lai-ho-ban-dem-da-nang.html',
    'thue-tai-xe-theo-gio-da-nang.html','thue-tai-xe-theo-ngay-da-nang.html',
    'thue-tai-xe-di-tinh-da-nang.html','thue-tai-xe-da-nang-di-hoi-an.html',
    'thue-tai-xe-da-nang-di-hue.html','thue-tai-xe-dua-don-doi-tac-da-nang.html',
    'tai-xe-phuc-vu-tiec-cuoi-su-kien-da-nang.html',
}

def set_meta(source,selector,value):
    pattern=r'(<meta\b[^>]*'+re.escape(selector)+r'[^>]*\bcontent=")[^"]*("[^>]*>)'
    result,count=re.subn(pattern,lambda m:m[1]+html.escape(value,quote=True)+m[2],source,count=1)
    if count!=1:raise ValueError('Missing metadata: '+selector)
    return result

def render_page(source,page):
    source=re.sub(r'<title>.*?</title>',lambda m:'<title>'+html.escape(page['title'])+'</title>',source,count=1,flags=re.S)
    source=set_meta(source,'name="description"',page['description'])
    source=set_meta(source,'property="og:title"',page['h1'])
    source=set_meta(source,'property="og:description"',page['description'])
    source=set_meta(source,'property="og:url"',BASE+page['file'])
    source=set_meta(source,'property="og:image"',BASE+page['hero_src'])
    source=re.sub(r'<link rel="canonical" href="[^"]+">',lambda m:'<link rel="canonical" href="'+BASE+page['file']+'">',source,count=1)
    source=re.sub(r'<h1>.*?</h1>',lambda m:'<h1>'+html.escape(page['h1'])+'</h1>',source,count=1,flags=re.S)
    source=re.sub(r'<p class="lead">.*?</p>',lambda m:'<p class="lead">'+html.escape(page['intro'])+'</p>',source,count=1,flags=re.S)
    source=re.sub(r'(<img\b[^>]*src="'+re.escape(page['hero_src'])+r'"[^>]*alt=")[^"]*',lambda m:m[1]+html.escape(page['hero_alt'],quote=True),source,count=1)
    start=source.index('<div class="reading">')+len('<div class="reading">')
    end=source.rfind('</div>',start,source.index('</main>',start))
    if end<start:raise ValueError('Missing reading container')
    source=source[:start]+page['body_html']+source[end:]
    def schema(match):
        data=json.loads(match[1])
        if data.get('@type')=='Article':
            data['headline']=page['h1'];data['description']=page['description']
            data['dateModified']=page['modified'];data['image']=[BASE+page['hero_src']]
            data['mainEntityOfPage']={'@type':'WebPage','@id':BASE+page['file']}
        elif data.get('@type')=='BreadcrumbList':
            data['itemListElement'][-1]['name']=page['h1']
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,source,flags=re.S)

def render_hub(source,pages):
    by_file={p['file']:p for p in pages}
    def update(match):
        card=match[0];target=re.search(r'class="card-image-link" href="([^"]+)"',card)
        if not target or target[1] not in by_file:raise ValueError('Unknown news-card target')
        p=by_file[target[1]]
        topics=re.search(r'data-topics="([^"]*)"',card)[1]
        category=('bang-gia' if p['file']=='bang-gia-lai-xe-ho-da-nang.html' else
                  'khu-vuc' if p['file'] in REGIONS or p['file']=='khu-vuc-phuc-vu.html' else
                  'dich-vu' if p['file'] in SERVICES else 'bai-viet')
        card=re.sub(r' data-(?:category|region)="[^"]*"','',card)
        card=card.replace('<article class="card"','<article class="card" data-category="'+category+'" data-region="'+html.escape(REGIONS.get(p['file'],''),quote=True)+'"',1)
        body_text=html.unescape(re.sub(r'<[^>]+>',' ',p['body_html']))
        search=' '.join((p['h1']+' '+p['intro']+' '+html.unescape(topics).replace('|',' ')+' '+body_text).split())
        card=re.sub(r'data-search="[^"]*"',lambda m:'data-search="'+html.escape(search,quote=True)+'"',card,count=1)
        card=re.sub(r'(<h3><a href="[^"]+">).*?(</a></h3>)',lambda m:m[1]+html.escape(p['h1'])+m[2],card,count=1,flags=re.S)
        card=re.sub(r'<p>.*?</p>',lambda m:'<p>'+html.escape(p['intro'])+'</p>',card,count=1,flags=re.S)
        card=re.sub(r'(<img\b[^>]*alt=")[^"]*',lambda m:m[1]+html.escape(p['hero_alt'],quote=True),card,count=1)
        return card
    source=re.sub(r'<article class="card"[^>]*>.*?</article>',update,source,flags=re.S)
    # Keep the visible section headings consistent with the main filters.
    cards=re.findall(r'<article class="card"[^>]*>.*?</article>',source,re.S)
    for section,categories in [('dich-vu',{'bang-gia','dich-vu'}),('khu-vuc',{'khu-vuc'}),('bai-viet',{'bai-viet'})]:
        selected=''.join(card for card in cards if re.search(r'data-category="([^"]+)"',card)[1] in categories)
        pattern=r'(<section id="'+section+r'"[^>]*>.*?<div class="cards">).*?(</div></section>)'
        source,count=re.subn(pattern,lambda m:m[1]+selected+m[2],source,count=1,flags=re.S)
        if count!=1:raise ValueError('Missing news category section: '+section)
    source=re.sub(r'<title>.*?</title>','<title>Tin tức, dịch vụ và khu vực | Như Ý Driver</title>',source,count=1,flags=re.S)
    source=set_meta(source,'name="description"','Tìm bảng giá, dịch vụ lái hộ ô tô, xe máy, hướng dẫn đặt tài xế và khu vực nhận yêu cầu của Như Ý Driver tại Đà Nẵng.')
    source=set_meta(source,'property="og:description"','Bảng giá, dịch vụ, hướng dẫn đặt tài xế và các khu vực nhận yêu cầu của Như Ý Driver tại Đà Nẵng.')
    return source

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    pages=json.loads((ROOT/'content/pages.json').read_text(encoding='utf-8'))['pages']
    if len(pages)!=29:raise ValueError('Expected the 29 existing detail pages')
    results={}
    for p in pages:
        path=ROOT/p['file']
        if path.parent!=ROOT or p['file']=='index.html' or not path.is_file():raise ValueError('Invalid existing page')
        old=path.read_text(encoding='utf-8');new=render_page(old,p)
        if new!=old:results[path]=new
    hub=ROOT/'tin-tuc.html';old=hub.read_text(encoding='utf-8');new=render_hub(old,pages)
    if new!=old:results[hub]=new
    # Only content that was actually edited gets a current lastmod, never the protected homepage.
    site=ROOT/'sitemap.xml';old=site.read_text(encoding='utf-8');tree=ET.fromstring(old);ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    dates={BASE+p['file']:p['modified'] for p in pages};dates[BASE+'tin-tuc.html']='2026-10-28'
    for node in tree.findall(ns+'url'):
        loc=node.find(ns+'loc')
        if loc.text in dates:
            last=node.find(ns+'lastmod')
            if last is None:last=ET.SubElement(node,ns+'lastmod')
            last.text=dates[loc.text]
    ET.register_namespace('',ns[1:-1])
    new='<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(tree,encoding='unicode')+'\n'
    if new!=old:results[site]=new
    if args.check:
        if results:
            print('Stale outputs: '+', '.join(p.name for p in results));return 1
        print('PASS: all 29 detail pages, news previews and sitemap match the content source.');return 0
    for path,new in results.items():path.write_text(new,encoding='utf-8')
    print('Rendered '+str(len(results))+' changed files from content/pages.json.');return 0

if __name__=='__main__':sys.exit(main())

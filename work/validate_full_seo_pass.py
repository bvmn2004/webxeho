from pathlib import Path
from lxml import html
from PIL import Image
from urllib.parse import urlsplit,unquote
import hashlib,json,re,xml.etree.ElementTree as ET

source=json.loads(Path('content/pages.json').read_text(encoding='utf-8'))['pages']
baseline=json.loads(Path('work/seo-pass-2026-10-28-baseline.json').read_text(encoding='utf-8'))
before={r['file']:r for r in json.loads(Path('work/seo-pass-2026-10-28-before.json').read_text(encoding='utf-8'))}
files={p['file'] for p in source};assert len(files)==29
edited=files|{'tin-tuc.html','sitemap.xml'}
for name,digest in baseline.items():
 if name not in edited:assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,('Protected file changed',name)
home=Path('index.html').read_text(encoding='utf-8')
expected_header=re.search(r'<header\b.*?</header>\s*<!-- Mobile menu -->\s*<nav\b.*?</nav>',home,re.S).group()
expected_header=re.sub(r'href="#([^\"]+)"',r'href="index.html#\1"',expected_header)
expected_footer=re.search(r'<footer\b.*?</footer>',home,re.S).group()
protected_scripts=[s for s in re.findall(r'<script\b.*?</script>',home,re.S) if 'window.dataLayer' in s or 'function gtag_report_conversion' in s or 'googletagmanager.com/gtag/' in s]
titles=set();descriptions=set();out=[]
for file in sorted(files|{'tin-tuc.html'}):
 raw=Path(file).read_text(encoding='utf-8');doc=html.fromstring(raw)
 assert len(doc.xpath('//h1'))==1,file
 title=doc.xpath('//title/text()')[0];desc=doc.xpath('//meta[@name="description"]/@content')[0]
 assert title not in titles,file;assert desc not in descriptions,file;titles.add(title);descriptions.add(desc)
 assert doc.xpath('//link[@rel="canonical"]/@href')==['https://laixehodanang.me/'+file],file
 assert doc.xpath('//meta[@property="og:url"]/@content')==['https://laixehodanang.me/'+file],file
 assert re.search(r'<header\b.*?(?=<main\b)',raw,re.S).group().strip()==expected_header.strip(),file
 assert re.search(r'<footer\b.*?</footer>',raw,re.S).group()==expected_footer,file
 for script in protected_scripts:assert script in raw,('Tracking changed',file)
 ids=doc.xpath('//*[@id]/@id');assert len(ids)==len(set(ids)),('Duplicate ID',file)
 links=0
 for el in doc.xpath('//a[@href]|//img[@src]|//script[@src]|//link[@href]'):
  v=el.get('href') or el.get('src');u=urlsplit(v)
  if u.scheme or u.netloc:continue
  target=Path(unquote(u.path).lstrip('/')) if u.path else Path(file)
  assert target.is_file(),(file,v)
  if u.fragment:assert html.parse(str(target)).xpath('//*[@id=$v]',v=u.fragment),(file,v)
  links+=1
 for el in doc.xpath('//main//img'):
  assert el.get('alt') and el.get('width') and el.get('height'),file
  im=Image.open(el.get('src'));assert im.size==(int(el.get('width')),int(el.get('height'))),file
 for script in doc.xpath('//script[@type="application/ld+json"]'):
  data=json.loads(script.text)
  if data.get('@type')=='Article':
   assert data['headline']==doc.xpath('//h1')[0].text_content()
   assert data['description']==desc
   assert data['dateModified']=='2026-10-28'
   assert doc.xpath('//time[@datetime="2026-10-28"]'),file
 if file in files:
  current=' '.join(doc.xpath('//div[@class="reading"]')[0].itertext())
  assert current!=before[file]['text'],('Body not edited',file)
  assert doc.xpath('//nav[@class="toc"]//a'),file
  if file!='bang-gia-lai-xe-ho-da-nang.html':assert doc.xpath('//main//a[@href="bang-gia-lai-xe-ho-da-nang.html"]'),file
  assert doc.xpath('//main//a[@href="tel:0985666044"]') and doc.xpath('//main//a[@href="https://zalo.me/0985666044"]'),file
  assert not doc.xpath('//div[@class="related"]/a[@href=$v]',v=file),('Self-related link',file)
 out.append({'file':file,'h1':doc.xpath('//h1')[0].text_content(),'local_links_checked':links})
news=html.parse('tin-tuc.html');cards=news.xpath('//article[@data-search]');assert len(cards)==29
assert {c.xpath('./a[@class="card-image-link"]/@href')[0] for c in cards}==files
for card in cards:
 target=card.xpath('./a[@class="card-image-link"]/@href')[0]
 assert target==card.xpath('.//h3/a/@href')[0]
 target_doc=html.parse(target)
 assert card.xpath('.//h3')[0].text_content()==target_doc.xpath('//h1')[0].text_content()
assert len(ET.parse('sitemap.xml').findall('.//{*}loc'))==31
urls=[e.text for e in ET.parse('sitemap.xml').findall('.//{*}loc')];assert len(urls)==len(set(urls))
assert 'Disallow: /' not in Path('robots.txt').read_text(encoding='utf-8')
assert 'Đúng 5 km' not in Path('bang-gia-lai-xe-ho-da-nang.html').read_text(encoding='utf-8')
result={'detail_pages_reviewed_and_body_edited':29,'news_hub_checked':1,'protected_homepage_checked':1,'total_pages_reviewed':31,'cards':29,'sitemap_urls':31,'protected_files_unchanged':True,'checks':'PASS','pages':out}
Path('work/seo-pass-2026-10-28-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 29 edited detail pages + news + protected homepage. Metadata, content sources, links, images, anchors, tracking and sitemap verified.')

from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
from PIL import Image
import hashlib,json,re,xml.etree.ElementTree as ET

baseline=json.loads(Path('work/current-task-baseline.json').read_text(encoding='utf-8'))
for name,digest in baseline.items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,('Protected file changed',name)
manifest=json.loads(Path('work/new-content-manifest.json').read_text(encoding='utf-8'))
new={d['slug']+'.html' for d in manifest['areas']+manifest['articles']}
index=Path('index.html').read_text(encoding='utf-8')
header=re.search(r'<header\b.*?</header>\s*<!-- Mobile menu -->\s*<nav\b.*?</nav>',index,re.S).group()
header=re.sub(r'href="#([^\"]+)"',r'href="index.html#\1"',header)
footer=re.search(r'<footer\b.*?</footer>',index,re.S).group()
titles=set();descs=set();content=[]
for file in Path('.').glob('*.html'):
 s=file.read_text(encoding='utf-8')
 if '<main' not in s:continue
 content.append(file.name);d=html.fromstring(s)
 assert len(d.xpath('//h1'))==1,file
 title=d.xpath('//title/text()')[0];desc=d.xpath('//meta[@name="description"]/@content')[0]
 assert title not in titles,('duplicate title',file);titles.add(title)
 assert desc not in descs,('duplicate description',file);descs.add(desc)
 assert d.xpath('//link[@rel="canonical"]/@href')==['https://laixehodanang.me/'+file.name],file
 ids=d.xpath('//*[@id]/@id');assert len(ids)==len(set(ids)),('duplicate id',file)
 assert re.search(r'<footer\b.*?</footer>',s,re.S).group()==footer,file
 assert re.search(r'<header\b.*?(?=<main\b)',s,re.S).group().strip()==header.strip(),file
 for el in d.xpath('//a[@href]|//img[@src]|//script[@src]|//link[@href]'):
  value=el.get('href') or el.get('src');u=urlsplit(value)
  if u.scheme or u.netloc:continue
  target=Path(unquote(u.path).lstrip('/')) if u.path else file
  assert target.is_file(),('missing target',file,value)
  if u.fragment and target.suffix=='.html':assert html.parse(str(target)).xpath('//*[@id=$v]',v=u.fragment),('missing anchor',file,value)
 for node in d.xpath('//script[@type="application/ld+json"]'):json.loads(node.text)
 for el in d.xpath('//main//img'):
  assert el.get('alt') and el.get('width') and el.get('height'),('image metadata',file)
  im=Image.open(unquote(el.get('src')));assert im.width==int(el.get('width')) and im.height==int(el.get('height')),file
 if file.name in new:
  assert len(d.xpath('//details'))>=3,file
  assert len(d.xpath('//nav[@class="toc"]//a'))==len(d.xpath('//div[@class="reading"]/section/h2[@id]')),file
  assert 'C:\\Users' not in s
  assert 'tel:0985666044' in s and 'https://zalo.me/0985666044' in s
  assert 'G-K5J958F2D4' in s and 'AW-18148925849' in s and 'AW-17783643653' in s
  assert len(' '.join(d.xpath('//div[@class="reading"]//text()')).split())>450,file
news=html.parse('tin-tuc.html');cards=news.xpath('//article[@data-search]');assert len(cards)==29
for card in cards:assert card.xpath('./a[@class="card-image-link"]/@href')[0]==card.xpath('.//h3/a/@href')[0]
buttons=set(news.xpath('//button[@data-topic]/@data-topic'))
for card in cards:
 for topic in card.get('data-topics').split('|'):assert topic in buttons,('unknown topic',topic)
tree=ET.parse('sitemap.xml');urls=[x.text for x in tree.findall('.//{*}loc')]
assert len(urls)==31 and len(set(urls))==31
assert set(urls)=={'https://laixehodanang.me/'}|{'https://laixehodanang.me/'+name for name in content}
assert 'Disallow: /' not in Path('robots.txt').read_text(encoding='utf-8')
result={'content_pages':len(content),'new_pages':len(new),'hub_cards':len(cards),'sitemap_urls':len(urls),'protected_files_unchanged':list(baseline),'checks':'PASS: title, description, canonical, H1, links, anchors, images, JSON-LD, shared header/footer, topics and sitemap'}
Path('work/qa-new-content.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))

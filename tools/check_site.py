"""Check both generated pages and local asset/anchor references."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'dist'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.html = {}
        self.feed(source)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'html':
            self.html = attrs
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate id: {attrs['id']}"
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'data-photo'):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if tag == 'img':
            assert 'alt' in attrs, 'Missing image alternative text'


for name, language in [('index.html', 'fr'), ('ar.html', 'ar')]:
    page = Page((ROOT / name).read_text())
    assert page.html['lang'] == language
    if language == 'ar':
        assert page.html['dir'] == 'rtl'
    assert 'avis' in page.ids
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if url.path:
            path = (ROOT / unquote(url.path)).resolve()
            assert path.is_relative_to(ROOT) and path.is_file(), f'{name}: missing {ref}'
        elif url.fragment:
            assert url.fragment in page.ids, f'{name}: missing anchor {ref}'
print('FR/AR: assets, anchors, image labels and language attributes checked.')

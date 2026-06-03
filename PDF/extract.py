import fitz, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\roxrl\OneDrive\Documents\GitHub\oxford\PDF'

def extract_topics(text):
    lines = text.split('\n')
    topics = []
    current = None
    buf = []
    header_re = re.compile(r'^[A-Z][A-Z\s\-/&()0-9#]{4,}$')
    for line in lines:
        l = line.strip()
        if not l:
            if buf and current:
                buf.append('')
            continue
        if header_re.match(l) and len(l) > 4:
            if current and buf:
                topics.append({'title': current, 'content': '\n'.join(buf).strip()})
            current = l
            buf = []
        else:
            if current:
                buf.append(l)
    if current and buf:
        topics.append({'title': current, 'content': '\n'.join(buf).strip()})
    return topics

all_data = []

# MK Weeks
for w in range(1, 8):
    fname = f'{base}\\MK-Week-0{w}.pdf'
    doc = fitz.open(fname)
    full_text = '\n'.join(page.get_text() for page in doc)
    topics = extract_topics(full_text)
    all_data.append({'source': f'MK-Week-{w:02d}', 'type': 'mark_klimek', 'week': w, 'topics': topics})
    print(f'MK-Week-{w}: {len(topics)} topics')

# Other files
others = [
    ('Lab Values and Therapeutic Drug Levels', 'lab_values'),
    ('nurseslabs-cram-sheet', 'cram_sheet'),
    ('แหกโค้ง 1 เมษา', 'thai_review_1'),
    ('แหกโค้ง 2 พค', 'thai_review_2'),
    ('แหกโค้ง 3 พค', 'thai_review_3'),
    ('Mark K Notes', 'mk_notes'),
    ('2026_RN_Test Plan_English-F', 'test_plan_2026'),
]

for fname, ftype in others:
    try:
        doc = fitz.open(f'{base}\\{fname}.pdf')
        full_text = '\n'.join(page.get_text() for page in doc)
        topics = extract_topics(full_text)
        all_data.append({'source': fname, 'type': ftype, 'topics': topics})
        print(f'{fname}: {len(topics)} topics')
    except Exception as e:
        print(f'ERROR {fname}: {e}')

out = f'{base}\\nclex_content.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

size_mb = round(__import__('os').path.getsize(out) / 1024 / 1024, 2)
print(f'\nSaved: nclex_content.json ({size_mb} MB)')
print(f'Total files: {len(all_data)}')
print(f'Total topics: {sum(len(d["topics"]) for d in all_data)}')

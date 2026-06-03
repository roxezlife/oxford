import fitz, json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\roxrl\OneDrive\Documents\GitHub\oxford\PDF'

def extract_topics(text):
    """Parse content into topics by detecting ALL-CAPS headers."""
    lines = text.split('\n')
    topics = []
    current = None
    buf = []
    header_re = re.compile(r'^[A-Z][A-Z\s\-/&()0-9#:\']{4,}$')

    for line in lines:
        l = line.strip()
        if not l:
            if buf:
                buf.append('')
            continue
        if header_re.match(l) and len(l) > 4:
            if current is not None and buf:
                topics.append({'title': current, 'content': '\n'.join(buf).strip()})
            current = l
            buf = []
        else:
            if current is not None:
                buf.append(l)
            # if no header yet, collect as intro
            elif l:
                if not topics:
                    current = 'INTRODUCTION'
                    buf = [l]

    if current and buf:
        topics.append({'title': current, 'content': '\n'.join(buf).strip()})
    return [t for t in topics if len(t['content']) > 20]

def extract_raw(text, source):
    """Fallback: return raw text as single topic block."""
    text = text.strip()
    if not text:
        return []
    # Split by double newline into chunks
    chunks = [c.strip() for c in re.split(r'\n{2,}', text) if len(c.strip()) > 30]
    return [{'title': f'Section {i+1}', 'content': c} for i, c in enumerate(chunks[:200])]

all_data = []

files = [
    ('MK-Week-01', 'mark_klimek', 1),
    ('MK-Week-02', 'mark_klimek', 2),
    ('MK-Week-03', 'mark_klimek', 3),
    ('MK-Week-04', 'mark_klimek', 4),
    ('MK-Week-05', 'mark_klimek', 5),
    ('MK-Week-06', 'mark_klimek', 6),
    ('MK-Week-07', 'mark_klimek', 7),
    ('Lab Values and Therapeutic Drug Levels', 'lab_values', None),
    ('nurseslabs-cram-sheet', 'cram_sheet', None),
    ('แหกโค้ง 1 เมษา', 'thai_review', None),
    ('แหกโค้ง 2 พค', 'thai_review', None),
    ('แหกโค้ง 3 พค', 'thai_review', None),
    ('Mark K Notes', 'mk_notes', None),
    ('2026_RN_Test Plan_English-F', 'test_plan', None),
]

for entry in files:
    fname, ftype = entry[0], entry[1]
    week = entry[2] if len(entry) > 2 else None
    path = f'{base}\\{fname}.pdf'
    if not os.path.exists(path):
        print(f'SKIP (not found): {fname}')
        continue
    try:
        doc = fitz.open(path)
        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())
        full_text = '\n'.join(pages_text)

        topics = extract_topics(full_text)
        if not topics:
            topics = extract_raw(full_text, fname)

        record = {
            'source': fname,
            'type': ftype,
            'pages': len(doc),
            'topics': topics
        }
        if week:
            record['week'] = week

        all_data.append(record)
        print(f'{fname}: {len(topics)} topics, {len(doc)} pages')
    except Exception as e:
        print(f'ERROR {fname}: {e}')

out = f'{base}\\nclex_content.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

size_kb = round(os.path.getsize(out) / 1024)
print(f'\nSaved: nclex_content.json ({size_kb} KB)')
print(f'Total files: {len(all_data)}')
print(f'Total topics: {sum(len(d["topics"]) for d in all_data)}')

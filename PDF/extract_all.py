import fitz, json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\roxrl\OneDrive\Documents\GitHub\oxford\PDF'
out_path = f'{base}\\nclex_content.json'

# Load existing data
with open(out_path, encoding='utf-8') as f:
    all_data = json.load(f)
done_sources = {d['source'] for d in all_data}

def extract_topics(text):
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
    if current and buf:
        topics.append({'title': current, 'content': '\n'.join(buf).strip()})
    return [t for t in topics if len(t['content']) > 20]

def extract_chunks(text):
    chunks = [c.strip() for c in re.split(r'\n{2,}', text) if len(c.strip()) > 40]
    return [{'title': f'Section {i+1}', 'content': c} for i, c in enumerate(chunks[:300])]

missing = [
    ('008a161a-72b6-4f8a-a293-3c7f865a9741', 'unknown'),
    ('1 เนื้อหาหลัก กย-ตค', 'thai_main'),
    ('2 เนื้อหาหลัก ตค', 'thai_main'),
    ('2019_RN_TestPlan-English', 'test_plan'),
    ('3 เนื้อหาหลัก Law เมษา', 'thai_main'),
    ('33', 'unknown'),
    ('4 เนื้อหาหลัก Culture เมษา', 'thai_main'),
    ('COMPLETENursingSchoolBundle_NurseInTheMaking_DIGITAL DOWNLOAD', 'nursing_bundle'),
    ('mosbys-comprehensive-review-of-nursing-for-the-nclex-rnc2ae-examination- (1)', 'mosbys'),
    ('mosbys-comprehensive-review-of-nursing-for-the-nclex-rnc2ae-examination-', 'mosbys'),
    ('NCLEX-RN-Exam-Cram-Practice-Questions', 'practice_questions'),
    ('Plan Exam', 'study_plan'),
    ('saunders-qa-review-for-the-nclex-rn-examination-7th-ed', 'saunders_qa'),
    ('Saunders', 'saunders_main'),
    ('สรุป UwolrdNotes (1)', 'uworld_notes'),
]

for fname, ftype in missing:
    if fname in done_sources:
        print(f'SKIP (already done): {fname}')
        continue
    path = f'{base}\\{fname}.pdf'
    if not os.path.exists(path):
        print(f'SKIP (not found): {fname}')
        continue
    try:
        size_mb = os.path.getsize(path) / 1024 / 1024
        print(f'Processing: {fname} ({size_mb:.1f} MB)...', flush=True)
        doc = fitz.open(path)
        pages = len(doc)

        # For very large files, sample pages to avoid memory issues
        if pages > 200:
            step = max(1, pages // 200)
            page_indices = list(range(0, pages, step))
            note = f'[sampled {len(page_indices)}/{pages} pages]'
        else:
            page_indices = list(range(pages))
            note = f'[{pages} pages]'

        texts = []
        for i in page_indices:
            texts.append(doc[i].get_text())
        full_text = '\n'.join(texts)

        topics = extract_topics(full_text)
        if not topics:
            topics = extract_chunks(full_text)

        record = {
            'source': fname,
            'type': ftype,
            'pages': pages,
            'note': note,
            'topics': topics
        }
        all_data.append(record)
        print(f'  → {len(topics)} topics {note}')

    except Exception as e:
        print(f'  ERROR: {e}')

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

size_mb = round(os.path.getsize(out_path) / 1024 / 1024, 2)
print(f'\nDone! nclex_content.json = {size_mb} MB')
print(f'Total files: {len(all_data)}')
print(f'Total topics: {sum(len(d["topics"]) for d in all_data)}')

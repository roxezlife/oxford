import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\roxrl\OneDrive\Documents\GitHub\oxford\PDF\nclex_content.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total files: {len(data)}")
print(f"Total topics: {sum(len(d['topics']) for d in data)}\n")

for d in data:
    topics = d['topics']
    titles = [t['title'] for t in topics[:6]]
    print(f"[{d['source']}] → {len(topics)} topics")
    for t in titles:
        print(f"   • {t}")
    print()

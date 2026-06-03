# แผนเพิ่มโหมด English ก.พ. ใน EN LEARN

## สัดส่วนข้อสอบ ก.พ. ภาษาอังกฤษ
| โหมด | สัดส่วน | ข้อ (จาก 25) |
|------|---------|-------------|
| Reading Comprehension | ~40-60% | 10+ ข้อ |
| Vocabulary | 20% | 5 ข้อ |
| Structure (Grammar) | 20% | 5 ข้อ |
| Conversation | 20% | 5 ข้อ |

## โหมดที่ต้องเพิ่ม (เรียงตามความสำคัญ)

### 1. Reading Comprehension (สำคัญที่สุด)
- แสดง passage (ย่อหน้า 1-3 ย่อหน้า)
- ตามด้วย 2-5 คำถาม multiple choice
- ข้อมูล: ดึงจาก PDF ผ่าน build_quiz.py

### 2. Conversation (บทสนทนา)
- แสดง situation/dialogue context
- เลือกว่าควรพูดอะไรต่อ (4 ตัวเลือก)
- ข้อมูล: ดึงจาก "แนวข้อสอบ วิชาภาษาอังกฤษ เรื่อง บทสนทนา (Conversation).pdf"

### 3. Structure (Grammar)
- เติมคำ/เลือก tense ที่ถูกต้อง
- ข้อมูล: ดึงจาก "แนวข้อสอบ วิชาภาษาอังกฤษ ไวยากรณ์ (Grammar).pdf"

### 4. Vocabulary (มีอยู่แล้ว แต่ปรับเพิ่ม)
- ปัจจุบัน: flash card คำศัพท์ Oxford 3000
- เพิ่ม: เติมคำในประโยค แบบ ก.พ. (fill-in-the-blank)

## แหล่งข้อมูล
- โฟลเดอร์: `C:\Users\roxrl\OneDrive\Desktop\กพ`
- Script: `build_quiz.py` (มี parser พร้อมแล้วสำหรับทุก PDF)
- PDF หลัก:
  - `แนวข้อสอบ วิชาภาษาอังกฤษ เรื่อง บทสนทนา (Conversation).pdf`
  - `แนวข้อสอบ วิชาภาษาอังกฤษ คำศัพท์ (Vocabulary).pdf`
  - `แนวข้อสอบ วิชาภาษาอังกฤษ ไวยากรณ์ (Grammar).pdf`
  - `แนวข้อสอบ วิชาภาษาอังกฤษ การอ่านจับใจความ (Reading Comprehension).pdf`
  - iTest ชุดต่างๆ (English ข้อ 51-75)

## แนวทาง Implementation

### ขั้นตอนที่ 1: Extract ข้อสอบ
- รัน/แก้ `build_quiz.py` ให้ export เฉพาะ English questions เป็น `gkh_english.json`
- Format: `{ topic, text, choices:{1,2,3,4}, answer, context? }`

### ขั้นตอนที่ 2: เพิ่มใน EN LEARN (index.html)
- เพิ่ม nav tab "ก.พ." หรือ "ข้อสอบ"
- Screen ใหม่มี 3 sub-mode: Conversation / Structure / Reading
- ใช้ UI เดิม (quiz style ที่มีอยู่แล้ว)
- โหลด `gkh_english.json` จาก GitHub Pages เหมือน words.json

### ขั้นตอนที่ 3: Speaking Practice (optional)
- ปุ่ม "ฝึกพูด" ในโหมด Conversation
- ใช้ Web Speech API (SpeechRecognition) — Chrome/Edge เท่านั้น
- ฟัง TTS → พูดตาม → ตรวจ % match

## หมายเหตุ
- `build_quiz.py` มี parser ครบแล้ว: `parse_english_pdf`, `parse_eng_inline`, `parse_eng_abcd_inline`
- Reading questions มี "Situation:" context ที่ต้องแสดงก่อนคำถาม
- Conversation questions มี dialogue context ที่ต้องแสดงพร้อมคำถาม

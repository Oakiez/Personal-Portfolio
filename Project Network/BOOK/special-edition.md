# Special Edition Notes — UCCN Simulator
**Simulator Design Decisions & Non-Obvious Choices**
**Version:** 1.0 | **Date:** 2026-03-19

---

## วัตถุประสงค์ของเอกสาร

เอกสารนี้บันทึก design decisions ที่ไม่ชัดเจน, trade-offs ที่เลือกไป, และ "lessons learned" ระหว่างการพัฒนา UCCN Simulator สำหรับผู้ที่จะสานต่อหรือ fork โปรเจกต์นี้

---

## 1. ทำไมถึงเลือก Vanilla JavaScript แทน Framework

### การตัดสินใจ
ใช้ HTML/CSS/JS ล้วนๆ โดยไม่ใช้ React, Vue, หรือ framework ใดๆ

### เหตุผล
1. **Portability:** ไฟล์เดียว เปิดได้ทุกเบราว์เซอร์โดยไม่ต้อง build
2. **Research tool:** เน้น concept demonstration ไม่ใช่ production app
3. **Canvas control:** HTML5 Canvas ต้องการ direct DOM access ที่ framework อาจซับซ้อนขึ้น
4. **Zero dependency:** ไม่มี npm, ไม่มี node_modules, ไฟล์เดียวส่งได้เลย

### Trade-off
State management ซับซ้อนขึ้นเมื่อ codebase ใหญ่ — แต่สำหรับ research prototype ขนาดนี้ยังรับได้

---

## 2. การออกแบบ DAFT O₆ Floor

### ปัญหา
ถ้า O₆ = 0 (ไม่มี link ในเครือข่าย) → DARS = O₄/0 = Infinity → crash

### วิธีแก้
กำหนด O₆ floor = 1.0 เมื่อไม่มี link, และ floor = 0.01 เมื่อมี link แต่ระยะห่าง → 0

### ผลกระทบ
เมื่อ T-Offset ทุกโหนด = 0 (ระยะเดียวกัน):
```
O₆ = 0.01  →  DARS = O₄/0.01 = O₄ × 100
```
ทำให้ DARS พุ่งสูงมากแม้ O₄ ต่ำ — **นี่คือ by design** เพื่อส่งสัญญาณว่า "nodes อยู่ที่เดียวกัน = ไม่ใช่ interstellar network จริง"

---

## 3. updateHeader() Patching Pattern

### ปัญหา
Sprint 4 ต้องการให้ `computeDAFT()` ทำงานทุกครั้งที่ `updateHeader()` ถูกเรียก แต่การ override function ตรงๆ ทำให้เกิด infinite recursion:

```javascript
// BAD - recursion!
const updateHeader = function(){
  updateHeader();  // calls itself forever
  computeDAFT();
};
```

### วิธีแก้
ใช้ aliasing pattern:
```javascript
const _baseUpdateHeader = updateHeader;
updateHeader = function(){
  _baseUpdateHeader();  // call original
  computeDAFT();        // then add new behavior
};
```

### หลักการ
นี่คือ **Decorator Pattern** — wraps existing function โดยไม่แก้ต้นฉบับ ใช้ได้กับ JavaScript เพราะ functions เป็น first-class citizens

---

## 4. DTN Auto-Send และ DARS Oscillation

### พฤติกรรมที่อาจดูเหมือน bug
เมื่อ simulation running และมี DTN mode active, DARS จะกระโดดขึ้นลงอย่างต่อเนื่อง:
```
PURE → CONSTRUCTIVE → PURE → CONSTRUCTIVE → ...
```

### ทำไมนี่คือ by design
1. DTN auto-send ส่ง packet ทุก ~5 วินาที (probability 5% per sim step)
2. แต่ละ packet ทำให้ TX++ ก่อน, RX++ ทีหลัง (latency)
3. ช่วง "รอ" นั้น O₄ > 0 → DARS > 0 → state เปลี่ยน
4. พอ RX มาถึง O₄ กลับ 0 → PURE

**นี่คือพฤติกรรมที่ถูกต้องของเครือข่ายที่มี propagation delay จริง**

---

## 5. Causal Hash Design

### ทำไมใช้ CRC32 แทน UUID หรือ SHA-256

| Criterion | CRC32 | UUID | SHA-256 |
|-----------|-------|------|---------|
| Display-friendly | ✅ 8 chars | ❌ 36 chars | ❌ 64 chars |
| Collision resistance | Medium | High | Very High |
| Research purposes | ✅ เพียงพอ | Over-engineered | Over-engineered |
| Multi-layer composability | ✅ ง่าย | ❌ | Medium |

สำหรับ research simulator ที่ไม่ได้เกี่ยวข้องกับ security จริง CRC32 ให้ human-readable ID ที่สั้นพอดู ใน log

### Multi-layer node ID
```
CH-{CRC32(s)}-{CRC32(s+'B')}-{CRC32(s+'C')[0:4]}-{CRC32(s+'D')[0:6]}
```
ให้ ID ในรูป `CH-XXXXXXXX-XXXXXXXX-XXXX-XXXXXX` ซึ่งอ่านออกว่าเป็น causal ID ได้ทันที

---

## 6. Theme System

### 4 Themes และ Rationale

| Theme | Palette | เหมาะกับ |
|-------|---------|---------|
| Stellar (default) | Blue/Cyan dark | งาน night mode ทั่วไป |
| Pulsar | Amber/Orange dark | สภาพแวดล้อมที่มีแสงน้อย |
| Nova | Green dark | Terminal / hacker aesthetic |
| Quasar | Light mode | การ present ในห้องสว่าง |

ทุก theme ใช้ CSS variables เดียวกัน (`--accent`, `--bg`, `--text` ฯลฯ) ทำให้สลับ theme ไม่ต้องเปลี่ยน logic

---

## 7. Simulator Limitations ที่ผู้ใช้ควรทราบ

1. **Graviton ไม่มีจริงในแง่ engineering** — เป็น theoretical particle ยังไม่เคยถูก generate ได้
2. **Neutrino bandwidth** ในโลกจริงปัจจุบันคือ ~0.1 bps ไม่ใช่ 100 MHz ตามที่จำลอง
3. **Temporal Offset** ใน simulator เป็น conceptual proxy ไม่ใช่ relativity calculation จริง
4. **DARS thresholds** (0.10, 0.30, 0.60) เป็นค่าที่เลือกเพื่อ demo — ยังไม่มี empirical basis
5. **Simulation clock** วิ่ง 1:1 กับเวลาจริง ไม่ได้ compress เวลาจักรวาล

---

*© UCCN Research Project — Special Edition Notes v1.0*

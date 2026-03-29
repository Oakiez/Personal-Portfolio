# Edition Comparison — UCCN Simulator
**Version History & Feature Matrix**
**Date:** 2026-03-19

---

## ภาพรวม / Overview

เอกสารนี้เปรียบเทียบความแตกต่างระหว่าง Sprint/Edition ต่างๆ ของ UCCN Simulator เพื่อช่วยให้ผู้วิจัยและนักพัฒนาเข้าใจวิวัฒนาการของระบบ

---

## Feature Matrix by Sprint

| Feature | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|---------|----------|----------|----------|----------|
| Node Registry | ✅ | ✅ | ✅ | ✅ |
| Causal Hash (CRC32) | ✅ | ✅ | ✅ | ✅ |
| Photon Mode | ✅ | ✅ | ✅ | ✅ |
| Neutrino Mode | ❌ | ✅ | ✅ | ✅ |
| Graviton Mode | ❌ | ✅ | ✅ | ✅ |
| DTN Mode | ❌ | ✅ | ✅ | ✅ |
| Multi-modal TX | ❌ | ✅ | ✅ | ✅ |
| Paradox Prevention | Basic | Full | Full | Full |
| Physics Engine | Basic | Full | Full | Full |
| DAFT Engine | ❌ | ❌ | ✅ | ✅ |
| Domain Mapping | ❌ | ❌ | ✅ | ✅ |
| Quality Metrics | ❌ | ❌ | ✅ | ✅ |
| Causal Graph Tab | ❌ | ❌ | ✅ | ✅ |
| Ethics / HITL | ❌ | ❌ | ❌ | ✅ |
| EU AI Act Compliance | ❌ | ❌ | ❌ | ✅ |
| Thai PDPA §26 | ❌ | ❌ | ❌ | ✅ |
| Roadmap Timeline | ❌ | ❌ | ✅ | ✅ |
| Log Resizer | ❌ | ❌ | ❌ | ✅ |
| Theme System (4 themes) | ❌ | Partial | ✅ | ✅ |

---

## Sprint Highlights

### Sprint 1 — Foundation
- สร้าง Node Registry พื้นฐาน
- Photon-only transmission
- Causal Hash (CRC32) สำหรับ node ID
- Canvas rendering เบื้องต้น
- Paradox prevention: Grandfather only

### Sprint 2 — Multi-Modal
- เพิ่ม Neutrino, Graviton, DTN modes
- Multi-modal simultaneous transmission
- Physics Engine ครบ (Shannon, Lorentz γ, DTN Bundle)
- Paradox: เพิ่ม Causal Loop + Bootstrap
- Vector Clock (Lamport Timestamp)
- Link Mode สำหรับเชื่อมโหนดด้วย GUI

### Sprint 3 — Intelligence Layer
- **DAFT Engine:** O₄, O₆, DARS, State Machine
- **Domain Interface Mapping:** Bio, Physics, Neuro, Quantum
- **Quality Metrics Dashboard** (7 metrics)
- **Causal Graph Tab:** visualize event sequence
- **Roadmap Timeline:** Phase 0–5 (2024–3000+)
- Theme system สมบูรณ์ (Stellar, Pulsar, Nova, Quasar)

### Sprint 4 — Ethics & HITL
- **Ethics Tab:** EU AI Act Art.13/14 compliance
- **HITL Architecture:** 3 levels
- **Thai PDPA §26** integration
- Human Override button พร้อม audit log
- DAFT → Ethics trigger map
- Log resizer (VS Code style)
- Topbar แสดง DAFT state + DARS แบบ real-time

---

## Breaking Changes

| Version | Breaking Change |
|---------|----------------|
| Sprint 2 → 3 | DAFT state computation เพิ่มใน `updateHeader()` — ต้อง patch ไม่ override |
| Sprint 3 → 4 | `updateHeader` ถูก wrap ด้วย `_baseUpdateHeader` pattern |

---

## Known Issues by Version

| Issue | Affected Version | Status |
|-------|-----------------|--------|
| Lorentz γ = Infinity เมื่อ v=c | Sprint 1-2 | Fixed in Sprint 2 (clamp at 0.9999999) |
| DARS oscillation เมื่อ DTN auto-send | Sprint 3+ | By design — ไม่ใช่ bug |
| O₆ = 0 ทำให้ DARS = Infinity | Sprint 3 | Fixed: O₆ floor = 0.01 |

---

*© UCCN Research Project — Edition Comparison v1.0*

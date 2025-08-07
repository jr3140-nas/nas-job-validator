# 🛠️ NAS Job Packet Quality Validator

This Streamlit web app allows planners at North American Stainless to automatically score corrective maintenance job packets against a standard 8-point checklist.

## ✅ Features
- Upload one or multiple PDF job packets
- Auto-extract and evaluate content (text-based)
- Score each packet against quality criteria
- Detailed feedback for each job plan

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Checklist Criteria
1. Work Request conversion
2. Job scope (site visit, notes)
3. 3-stage planning (Before/During/After)
4. Technician instructions
5. Labor estimate (crew, duration)
6. Parts & tools listed
7. Safety planning (LOTO, PPE, hazards)
8. Job packet completeness

---
Built for NAS Mechanical Maintenance Team • August 2025

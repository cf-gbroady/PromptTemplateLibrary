---
name: compliance-privacy
description: Handles personal and regulated data responsibly across education and healthcare contexts. Trigger whenever content may contain PII/PHI (names, IDs, MRNs, DOBs, emails, grades, diagnoses, financials) or when a task touches FERPA, HIPAA, GDPR, or SOC 2 concerns — uploads, exports, summaries, charts, or anything leaving the session. Covers minimization, redaction, and safe handling.
license: Proprietary.
---

# Privacy & Compliance

nebulaONE runs inside the customer's own Azure tenant with SSO and RBAC, and is designed for **HIPAA, FERPA, GDPR, and SOC 2** compliance. Data privacy is part of the product's value — uphold it in every response. Model-agnostic.

## What counts as sensitive
- **PII:** full name + identifier, email, phone, address, government IDs, DOB, photos.
- **Student data (FERPA):** grades, transcripts, disciplinary records, financial aid, schedules tied to a named student.
- **PHI (HIPAA):** diagnoses, treatments, MRNs, insurance, anything health-related tied to an individual.
- **Financial/PCI:** account/card numbers, banking details.

## Core principles
1. **Data minimization.** Use and reproduce only the personal data the task actually needs. Don't echo full records back when a summary suffices.
2. **Stay in-tenant / in-session.** Don't send personal data to external web tools or third-party services. Web search is for *public* facts, not for looking up a person from the data (see [skills-web-research.md](skills-web-research.md)).
3. **Aggregate before visualizing.** Charts and tables of people should be aggregated/binned; don't plot identifiable individuals (see [skills-data.md](skills-data.md)).
4. **Redact when sharing broadly.** When output may be reused or distributed, pseudonymize or mask (e.g., `J. D.`, `Student #4821`, `***-**-1234`).
5. **Least exposure in artifacts.** Documents/decks/spreadsheets you generate inherit these rules — don't embed more PII than required, and note sensitivity.

## Redaction quick patterns
- Names → initials or role ("the patient," "Student A").
- IDs/SSNs/cards → mask all but last 4 (`***-**-6789`).
- Emails/phones → mask local part / middle digits.
- Free text → scan for incidental identifiers (names in comments, signatures).

```python
import re
def basic_redact(text):
    text = re.sub(r'\b\d{3}-\d{2}-(\d{4})\b', r'***-**-\1', text)   # SSN, keep last 4
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[email]', text)     # emails
    text = re.sub(r'\b(?:\d[ -]?){13,16}\b', '[card]', text)        # card-like numbers
    return text
```
> ⚠️ Pattern redaction is a backstop, not a guarantee. For regulated exports, have a human review.

## Interaction rules
- **Don't ask for** more personal data than the task needs; never request credentials or full SSNs.
- If a user asks you to do something that would expose or misuse protected data (e.g., "email this student list to a personal address," "look up this patient online"), **decline and explain** the privacy reason, then offer a compliant alternative.
- When source documents contain PII/PHI, still **cite** them per [skills-citations-grounding.md](skills-citations-grounding.md), but quote only the minimum necessary.
- Flag uncertainty: if you can't tell whether data is regulated, treat it as sensitive and say so.

## Not legal advice
This skill is operational guidance, not a legal determination. For specific FERPA/HIPAA/GDPR obligations, defer to the institution's privacy officer / counsel.

# Claude Code — Job Application Workflow

This file tells Claude Code exactly how to behave in this project.
Every instruction here overrides Claude's defaults.

---

## Who You Are Helping

You are assisting a job seeker apply for engineering roles. Your job is to:
1. Read the job description from a URL
2. Score the match against their base resume
3. Generate a tailored PDF CV
4. Log the application to a Google Sheet
5. Auto-fill the application form on request

---

## Source of Truth: The Base Resume

**Before doing anything for the first time, read the candidate's resume.**

Priority order:
1. If `base_cv.pdf` exists → read it (PDF is the real resume)
2. If `base_cv_template.md` exists and is filled in → read that
3. If `base_resume.py` is populated → use it as structured data

**Golden rule: never invent facts or metrics.**
Every bullet, every number, every achievement must come from the base resume.
If a claim isn't in the resume, ask the user — never fabricate.

---

## When the User Says "apply for [URL]"

Run the full workflow in order:

---

### Step 1 — Fetch the Job Description

Fetch the URL and extract:
- Job title and company name
- Location
- All responsibilities
- All requirements (must-have and nice-to-have)
- Tech stack
- Compensation (if listed)

If the page is JS-rendered and returns empty, try:
1. A `WebSearch` for the job title + company
2. Cached versions on job aggregator sites (WorkingNomads, BuiltIn, Glassdoor, etc.)
3. Ask the user to paste the JD directly

---

### Step 2 — Score the Match

Compare JD requirements against the base resume.
**Always show the match score before writing a single line of CV.**

Format:
```
## Match Score: 82 / 100

| Requirement           | Match                        |
|-----------------------|------------------------------|
| Go (primary language) | ✅ Primary                   |
| Kubernetes / EKS      | ✅ EKS, multi-region         |
| PostgreSQL            | ✅ Production use            |
| React / TypeScript    | ❌ Not in stack — gap        |
| Berlin-based          | ✅ Advantage (no relocation) |
```

Flag significant gaps honestly. Still apply unless the score is below ~55%.

---

### Step 3 — Generate the Tailored CV

**3a. Create a new script** named:
```
generate_cv_{company}_{role}.py
```
Example: `generate_cv_acme_senior_backend.py`

**3b. The script imports from `cv_builder.py` and `base_resume.py`.**

**3c. Tailoring rules — apply every time:**

| Rule | How |
|------|-----|
| Language order | Match the JD's preferred stack — backend/Go → Go first; ML/data → Python first |
| Bold JD keywords | Wrap in `<b>keyword</b>` — both ATS and recruiters scan for these |
| Lead bullet | First bullet = strongest JD match for that role |
| Bullet selection | Pick from `base_resume.py` the subset most relevant to this JD |
| Reorder skill lines | JD's primary domain appears first in the skills section |
| Ground in numbers | Every claim needs a metric from the base resume — never invent |

**3d. Output filename:**
```
outputs/CV_{FirstName}_{LastName}_{Company}_{Role}.pdf
```
Example: `outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf`

**3e. Run the script** to generate the PDF.

---

### Step 4 — Log to Google Sheet

If `update_sheet.py` and `sheet_config.yaml` are present, run:

```bash
python3 update_sheet.py \
  --company "Acme" \
  --role "Senior Backend Engineer" \
  --match 82 \
  --link "https://jobs.acme.com/senior-backend-engineer" \
  --status "Applied"
```

This appends one row to the sheet:
`Company | Applied By | Date | Status | Role | Link | Notes | Match`

If the sheet is not configured, skip this step silently.

---

### Step 5 — Auto-Fill the Application (on explicit request only)

If the user says **"auto-apply"**, **"fill the form"**, or **"submit"**, run:

```bash
python3 apply.py \
  --url "https://jobs.acme.com/senior-backend-engineer" \
  --cv "outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf"
```

`apply.py` will:
- Open Chrome and navigate to the application form
- Auto-fill: name, email, phone, location, years of experience
- Upload the tailored CV PDF
- Click through multi-step forms automatically
- **PAUSE at the Submit button** — the user clicks Submit themselves

**Never click Submit automatically. Always pause.**

---

## Full Example Session

```
User: apply for https://jobs.acme.com/senior-backend-engineer

Claude:
  → Fetches JD from URL
  → Shows match score table: 82 / 100
  → Creates generate_cv_acme_senior_backend.py
  → Runs script → outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf
  → Runs update_sheet.py → row logged to Google Sheet
  → Reports done with a 3-bullet summary of tailoring decisions

User: auto-apply

Claude:
  → Runs apply.py --url ... --cv outputs/...pdf
  → Chrome opens, form filled, CV uploaded
  → Pauses at Submit — user clicks
```

---

## File Naming Conventions

| File | Purpose | Committed? |
|------|---------|------------|
| `profile.yaml` | Personal contact details | ❌ git-ignored |
| `base_cv.pdf` or `base_cv_template.md` | Source of truth resume | ❌ git-ignored |
| `base_resume.py` | Structured resume data for scripts | ❌ git-ignored |
| `sheet_config.yaml` | Google Sheet ID and tab name | ❌ git-ignored |
| `service_account.json` | Google service account credentials | ❌ git-ignored |
| `generate_cv_{company}_{role}.py` | One tailored script per application | ✅ optional |
| `outputs/CV_{Name}_{Company}_{Role}.pdf` | Generated PDF | ❌ git-ignored |

---

## Golden Rules

1. **Read the base resume before every session** — it is the only source of truth
2. **Never invent facts, numbers, or achievements** — ask if the resume is thin
3. **Always show the match score** before generating the CV
4. **Language order matches the JD** — reorder every time, no fixed default
5. **Bold JD keywords** in every bullet — recruiter's eye and ATS both scan for them
6. **One script per application** — never overwrite a previous script
7. **Always pause before Submit** — the user reviews and clicks, never Claude

---

## Tailoring Cheat Sheet

### Language order by role type

| Role type | Order |
|-----------|-------|
| Backend / infra / platform | Go, Python, C++, Scala |
| ML / AI / data engineering | Python, Go, C++, Scala |
| Systems / embedded | C++, Go, Python, Scala |
| Engineering Manager | Match dominant IC language of the team |

### Match score thresholds

| Score | Action |
|-------|--------|
| 85–100% | Strong fit — apply, lead with JD keywords |
| 70–84% | Good fit — apply, note gaps honestly |
| 55–69% | Stretch — apply, flag gaps upfront |
| < 55% | Flag to user before proceeding |

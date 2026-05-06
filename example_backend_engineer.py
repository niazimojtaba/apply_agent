"""
Example: tailor a CV for a Senior Backend Engineer role at Acme Corp.

Workflow:
  1. base_resume.py  — your complete history (fill in once)
  2. profile.yaml    — your personal details (fill in once)
  3. This script     — select, reorder, and bold what fits this specific JD

Copy this file, rename it (e.g. generate_cv_mycompany.py), edit each section,
then run:  python generate_cv_mycompany.py
"""

from cv_builder import CVBuilder
import base_resume as base

OUTPUT = "outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf"

cv = CVBuilder(OUTPUT)

# ── 1. Header ─────────────────────────────────────────────────────────────────
# Tailor the role title to the JD. Bold the most important keywords.
cv.header("Senior Backend Engineer — Go, Kubernetes &amp; Distributed Systems")

# ── 2. Summary ────────────────────────────────────────────────────────────────
# 3–4 sentences. Bold JD keywords. End with location + notice period.
cv.summary(
    "Senior backend engineer with <b>8+ years</b> building scalable, reliable "
    "distributed systems in <b>Go</b> and Python. Deep experience with "
    "<b>Kubernetes</b>, <b>Kafka</b>, and <b>AWS</b> — delivering microservices "
    "at <b>10M+ user scale</b> with <b>99.9% uptime</b>. Proven track record of "
    "owning systems end-to-end: design, delivery, observability, and on-call. "
    "Berlin-based, 1-month notice."
)

# ── 3. Skills ─────────────────────────────────────────────────────────────────
# Pull from base_resume.SKILLS and reorder to match the JD's stack.
# Bold keywords that appear verbatim in the JD.
cv.skills([
    ("Languages",     f"<b>Go</b> (primary), Python, C++"),
    ("Cloud & Infra", f"<b>AWS</b> (EKS, S3, IAM, multi-region), <b>Kubernetes</b>, Docker, Helm, Terraform"),
    ("Messaging",     f"<b>Kafka</b>, Temporal — event-driven architecture at production scale"),
    ("Databases",     base.SKILLS["databases"]),
    ("Observability", f"<b>SLO/SLI</b>/error budgets, distributed tracing, ELK stack, blameless postmortems"),
    ("Practices",     "Microservices, <b>gRPC</b>, REST, TDD, CI/CD"),
])

# ── 4. Work Experience ────────────────────────────────────────────────────────
# Import job entries from base_resume.JOBS.
# Pick only the bullets that are most relevant to this JD — fewer strong
# bullets beat many weak ones.

acme = base.JOBS["acme_senior"]
cv.job(
    acme["header"],
    acme["period"],
    acme["desc"],
    [
        acme["bullets"][1],  # Kafka pipeline  ← JD asks for event-driven
        acme["bullets"][0],  # Kubernetes migration  ← JD asks for K8s
        acme["bullets"][2],  # SLO/uptime  ← JD asks for SRE
        acme["bullets"][3],  # PostgreSQL perf  ← JD asks for DB experience
    ],
)

beta = base.JOBS["beta_mid"]
cv.job(
    beta["header"],
    beta["period"],
    beta["desc"],
    [
        beta["bullets"][0],  # Go APIs + observability
        beta["bullets"][1],  # TDD + CI/CD
    ],
)

# ── 5. Publications (optional) ────────────────────────────────────────────────
# cv.publications(base.PUBLICATIONS)   # uncomment if relevant to the role

# ── 6. Education ──────────────────────────────────────────────────────────────
cv.education(base.EDUCATION)

# ── 7. Awards (optional) ──────────────────────────────────────────────────────
cv.awards(base.AWARDS)

# ── 8. Render ─────────────────────────────────────────────────────────────────
cv.build()

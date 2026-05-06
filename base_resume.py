"""
base_resume.py — your complete professional history in one place.

Fill this in once with everything you've ever done.
Your per-role scripts import from here and cherry-pick / reorder
what's most relevant for each application.

Nothing here is printed automatically — you control what appears
in each CV by choosing which entries to include.
"""

# ── Personal headline (default; override per script) ─────────────────────────
DEFAULT_TITLE = "Senior Software Engineer"

# ── Skills ────────────────────────────────────────────────────────────────────
# Store the full list here. In each script, reorder lines and bold keywords
# that match the JD.

SKILLS = {
    "languages":    "Go, Python, C++, Scala",
    "cloud":        "AWS (EKS, Batch, S3, IAM, multi-region), Kubernetes, Docker, Helm, Terraform",
    "messaging":    "Kafka, Temporal, Airflow — event-driven architecture and workflow orchestration",
    "databases":    "PostgreSQL, Elasticsearch, Redis, Apache Druid",
    "observability":"ELK stack, distributed tracing, SLO/SLI/error budgets, blameless postmortem culture",
    "practices":    "Microservices, gRPC, REST, TDD, CI/CD, System Design, Agile/Scrum, OKR planning",
}

# ── Work experience ───────────────────────────────────────────────────────────
# Each job is a dict with all the bullets you've ever written about that role.
# In your per-role script, pass only the subset that fits the JD.

JOBS = {
    "acme_senior": {
        "header":  "Acme Corp — Senior Backend Engineer",
        "period":  "Jan 2022 – Present | Berlin, Germany",
        "desc":    "B2B SaaS platform — real-time data processing for 500+ enterprise customers.",
        "bullets": [
            # Infrastructure / Kubernetes
            "Migrated a monolith to <b>Kubernetes (EKS)</b>-based microservices using "
            "<b>Terraform</b> and Helm — cut release cycle from 2 weeks to <b>2 days</b>.",

            # Event-driven / Kafka
            "Designed <b>Kafka</b> ingestion pipeline processing <b>2M events/day</b> "
            "with guaranteed delivery, reducing data latency from 5 min to <b>under 10 s</b>.",

            # Observability / SRE
            "Defined <b>SLOs/SLIs</b> and error budgets; built burn-rate alerting — "
            "achieving <b>99.9% uptime</b> across all production services.",

            # Database / performance
            "Led <b>PostgreSQL</b> zero-downtime schema migrations on a 200M-row table; "
            "optimised slow queries — reduced p99 from <b>800 ms to 60 ms</b>.",

            # Leadership
            "Mentored 4 engineers through weekly 1:1s and architecture reviews; "
            "two promoted to senior within 18 months.",
        ],
    },

    "beta_mid": {
        "header":  "Beta Startup — Backend Engineer",
        "period":  "Jun 2018 – Dec 2021 | Remote",
        "desc":    "Developer tooling SaaS — 50K active users.",
        "bullets": [
            "Built core <b>Go</b> REST and <b>gRPC</b> APIs from scratch; "
            "introduced structured logging and distributed tracing — cut mean time "
            "to debug from hours to <b>under 15 minutes</b>.",

            "Introduced <b>TDD</b> and automated CI/CD: unit + integration test "
            "coverage from 20% to <b>85%</b>, eliminating a class of recurring bugs.",

            "Designed multi-tenant data model supporting <b>500+ isolated customer "
            "workspaces</b> with row-level security in PostgreSQL.",
        ],
    },
}

# ── Education ─────────────────────────────────────────────────────────────────
# List of (degree, institution + years, extra detail lines).

EDUCATION = [
    (
        "MSc Computer Science",
        "Technical University of Berlin &nbsp;(2016–2018)",
        "Thesis: Distributed Consensus in Edge Networks<br/>"
        "Teaching Assistant: Distributed Systems, Algorithms (2 terms)",
    ),
    (
        "BSc Computer Engineering",
        "University of Example &nbsp;(2012–2016)",
        "Teaching Assistant: Data Structures (3 terms)",
    ),
]

# ── Publications ──────────────────────────────────────────────────────────────

PUBLICATIONS = [
    'Smith, J. "Efficient consensus under partial failures." '
    '<i>IEEE Transactions on Distributed Systems</i>, Vol. 12, 2020.',
]

# ── Awards ────────────────────────────────────────────────────────────────────

AWARDS = [
    "1st place — Internal Hackathon, Acme Corp 2023",
    "Top 10% — Advent of Code 2022",
    "Best Paper Award — University Symposium 2018",
]

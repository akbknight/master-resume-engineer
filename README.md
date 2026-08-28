# Master Resume Engineer

Master Resume Engineer is an evidence-led framework for building, auditing, and tailoring professional resumes. It combines conservative fact reconciliation, standard applicant-tracking-system structure, direct human editing, and deterministic document checks.

The framework does not promise secret keywords or guaranteed screening outcomes. Its purpose is simpler: make a candidate's real qualifications easy to parse, easy to verify, and easy to understand.

## What It Does

- Reads and deduplicates resume, CV, portfolio, project, and supporting files.
- Separates candidate evidence from templates, job postings, and third-party examples.
- Reconciles conflicting dates, titles, metrics, employers, and credentials.
- Creates master, targeted, or audit-only resume outputs.
- Uses one-column structure, standard headings, conventional dates, and searchable text.
- Rewrites vague or inflated language into concise, evidence-based bullets.
- Checks metrics, ownership, units, causation, and institutional consistency.
- Removes hidden-text tricks, keyword stuffing, generic filler, and irrelevant personal details.
- Validates Markdown or plain-text resumes before document export.

## Research Foundation

The operating rules are grounded in seven prominent publications selected for their coverage of automated screening, hiring bias, recruiter trust, and model-mediated evaluation:

1. [Stanford HAI — AI Hiring Tools Can Yield Racial Bias and Systemic Rejection](https://hai.stanford.edu/news/ai-hiring-tools-can-yield-racial-bias-and-systemic-rejection)
2. [The New York Times — Recruiters Use A.I. to Scan Résumés. Applicants Are Trying to Trick It](https://www.nytimes.com/2025/10/07/business/ai-chatbot-prompts-resumes.html)
3. [Associated Press — Finding a Job Is Tough. Here's How AI Can and Can't Help](https://apnews.com/article/job-search-ai-resume-screening-interview-a535a7932ff291a1998158d40cd82c4c)
4. [Forbes — AI Resumes Are Sabotaging the Hiring Process, 67% of Managers Reveal](https://www.forbes.com/sites/rachelwells/2026/03/18/ai-resumes-are-sabotaging-the-hiring-process-67-of-managers-reveal/)
5. [BBC Worklife — AI Hiring Tools May Be Filtering Out the Best Job Applicants](https://www.bbc.com/worklife/article/20240214-ai-recruiting-hiring-software-bias-discrimination)
6. [New York Post — AI Job Screeners Prefer AI-Written Resumes](https://nypost.com/2026/05/16/us-news/artificial-intelligence-job-screeners-prefer-ai-written-resumes-over-human-ones-researchers-find/)
7. [Forbes — The AI Recruitment Takeover](https://www.forbes.com/sites/keithferrazzi/2025/03/27/the-ai-recruitment-takeover-redefining-hiring-in-the-digital-age/)

Primary and corroborating material is documented in [Research Basis](references/research-basis.md), including the underlying model self-preference paper, Robert Half's hiring-manager survey, and reporting on hidden resume prompts.

## Package Contents

- [`SKILL.md`](SKILL.md) — operating rules and workflow
- [`references/research-basis.md`](references/research-basis.md) — source synthesis, deductions, and limitations
- [`scripts/validate_resume.py`](scripts/validate_resume.py) — structural and language validator
- [`assets/ats-resume-template.md`](assets/ats-resume-template.md) — clean, single-column starting template

## Use

1. Load [`SKILL.md`](SKILL.md) as the governing instruction set.
2. Provide the candidate's source files.
3. Add a target job description when a tailored resume is required.
4. Run the validator against the completed Markdown draft.
5. If exporting DOCX or PDF, inspect both extracted text and the rendered pages.

Example request:

```text
Build a master resume from my source files. Reconcile conflicting claims conservatively, preserve only supported evidence, and run every verification gate before delivering the result.
```

Targeted example:

```text
Tailor my resume to this job description. Classify each requirement as a direct match, transferable match, unsupported gap, or unclear. Use employer terminology only where my evidence supports it.
```

## Validate a Resume

```bash
python scripts/validate_resume.py path/to/resume.md
```

Use `--json` for machine-readable results:

```bash
python scripts/validate_resume.py path/to/resume.md --json
```

The validator checks prohibited filler, screening manipulation, invisible or corrupted characters, hidden-text markup, Markdown images, core-content tables, required sections, contact fields, summary length, bullet length, repeated openings, weak phrasing, date formats, and quantified evidence.

## Design Principles

- Evidence outranks polish.
- Clear structure outranks visual decoration.
- Contextual proof outranks keyword repetition.
- Narrow, defensible claims outrank impressive but uncertain claims.
- International and non-standard experience should be explained, not erased.
- Every bullet should survive an interview follow-up question.

## Limitations

No resume can guarantee an interview or neutralize an undisclosed screening model. The framework improves clarity, parsing, factual consistency, and human verification; it does not manufacture qualifications or claim to defeat systemic bias.

## License

Released under the [MIT License](LICENSE).

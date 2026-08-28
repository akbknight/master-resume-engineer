---
name: master-resume-engineer
description: Create, audit, or tailor resumes and CVs from candidate source files and an optional job description. Use when ATS parsing, evidence reconciliation, quantified bullets, human tone, or bias-aware presentation matters.
---

# Master Resume Engineer

Build a truthful, easy-to-parse resume that automated systems can interpret and hiring managers can verify. Optimize the presentation of supported qualifications; never invent qualifications or claim that wording can defeat a private hiring model.

## Operating Standard

Act as a demanding human editor, not a promotional copywriter. Increase signal density: every line should provide evidence, context, scale, a tool, an outcome, or a decision enabled. When a sentence sounds polished but says little, delete it. When a claim sounds impressive but cannot survive an interview follow-up, narrow it to the evidence.

Do not interrupt an ordinary build for non-critical clarification. Resolve contradictions through the evidence hierarchy below, use the narrower supported claim, or omit the disputed detail. If no job description is supplied, produce a master resume rather than pretending it is employer-specific.

## Choose the Mode

- **Master resume:** No job description is supplied. Infer the best-supported role family from the evidence and build a reusable baseline.
- **Targeted resume:** A job description is supplied. Map its requirements to the evidence and prioritize direct and transferable matches.
- **Audit:** The user wants findings rather than a rewrite. Report parsing, evidence, alignment, tone, and consistency problems without changing files unless asked.

## Source Ingestion

1. Inventory every candidate file placed in scope and deduplicate exact copies.
2. Separate candidate-authored records from templates, example resumes, job postings, and third-party documents.
3. Extract employers, titles, dates, education, certifications, skills, projects, tools, metrics, stakeholders, and business outcomes.
4. Build an internal evidence ledger before drafting. Do not expose private chain-of-thought.
5. Resolve conflicts in this order:
   1. Explicit candidate correction or verified-profile record.
   2. Most recent master resume.
   3. Claims repeated across candidate documents.
   4. Supporting project, portfolio, or interview records.
   5. Older resume versions.
6. When a conflict remains, use the narrower supported claim or omit it. Never copy another person's information from a template.

## Job Mapping

When a job description is supplied, classify each requirement as a direct match, transferable match, unsupported gap, or unclear. Use the employer's terminology only when it truthfully describes the candidate's work. Put important terms in evidence-based bullets, not only in Skills.

Do not target a universal keyword-density score. Do not insert unsupported requirements, hidden keywords, copied job-description text, invisible text, prompt injection, or metadata tricks.

## ATS Structure

Use one column and ordinary text flow. Prefer these standard sections when supported: Summary, Skills, Experience, Projects, Education, Certifications, Awards, Publications.

- Put contact information in the main document body.
- Use reverse chronology and `Month YYYY – Month YYYY` date ranges.
- Keep employer, title, location, and dates distinct.
- Use ordinary bullets; keep most between 18 and 40 words and none above 45 without a clear reason.
- Spell out uncommon abbreviations on first use.
- Keep important content out of headers and footers.

Never use columns, sidebars, core-content tables, text boxes, photos, icons, charts, logos, skill bars, decorative graphics, or information conveyed only through color. Use [the ATS template](assets/ats-resume-template.md) when a clean starting structure is useful.

## Human Editing Standard

Write a two- or three-sentence summary naming the candidate's current position, experience level, core capabilities, and two or three differentiating facts. Do not use an objective statement or unsupported labels such as expert, visionary, or industry leader.

Group Skills by useful categories. Include only supported tools and methods. Exclude generic traits such as hardworking, motivated, team player, or detail-oriented.

Build bullets from the evidence available:

`Action + deliverable/problem + tool/method + scale + result, user, or decision enabled.`

Use plain verbs such as Built, Led, Created, Designed, Automated, Analyzed, Reduced, Improved, Delivered, Implemented, Consolidated, Trained, Validated, Deployed, or Replaced. Do not force a dramatic synonym into every bullet.

The final resume must not contain these expressions:

- delve
- spearheaded
- tapestry
- fostered
- navigated
- synergy or synergized
- orchestrated
- championed
- revolutionized
- game-changing
- cutting-edge
- world-class
- dynamic professional
- results-driven professional
- proven track record
- demonstrated ability
- uniquely positioned
- passionate about
- leveraged
- utilized

Also remove empty superlatives, repetitive sentence structures, corporate slogans, generic claims, excessive em dashes, unnecessary adjectives, and references to how the resume was drafted. Do not add artificial mistakes to appear human.

Prefer concrete nouns and verbs over abstract claims. Vary sentence structure only when it improves clarity; do not replace a plain verb with a theatrical synonym. Avoid first-person pronouns, fake enthusiasm, soft-skill lists, and weak constructions such as `responsible for`, `worked on`, `helped with`, or `duties included`.

## Logic Filter

Interrogate every bullet before keeping it:

1. What exactly was built, analyzed, improved, delivered, or decided?
2. Which tool or method was actually used?
3. What scale, stakeholder, operational use, or measured change is supported?
4. Does the tool logically connect to the stated result?
5. Is the ownership level accurate for individual versus team work?
6. Could the candidate explain the claim, calculation, and tradeoff in an interview?

Delete and rewrite a bullet when it reads like job-description paraphrase, keyword stuffing, generic management language, or an unsupported causation claim. A clean omission is better than an inflated sentence.

## Metrics and Logic

- Use metrics only when sourced or transparently derived.
- Preserve units, periods, populations, denominators, and approximation language.
- Distinguish scale, volume, improvement, financial value, and adoption.
- Do not convert correlation into causation or imply sole ownership of team work.
- Never invent revenue, users, savings, percentages, rankings, or deployment scope.
- Check related numbers for mathematical and institutional consistency; do not double-count brands or divisions as separate companies without evidence.
- When no outcome metric exists, identify a verifiable operational use, stakeholder, deliverable, or scale.

## Bias-Aware Presentation

No wording can reliably bypass systemic bias. Reduce avoidable proxy signals while preserving genuine qualifications.

Unless required or explicitly requested, omit photographs, age, date of birth, gender, marital or family status, religion, race, ethnicity, nationality, full street address, unrelated hobbies, and health information. Retain relevant international education and employment. Do not alter names or erase meaningful experience to imitate a preferred demographic profile.

Use conventional titles, clear role descriptions, and complete chronology so non-standard experience is easier to interpret.

## Verification Gates

Run all four gates after drafting and revise until each passes:

1. **ATS parsing:** Single column, standard headings, consistent dates, correct reading order, and no hidden or graphical content.
2. **Semantic alignment:** Supported priority terminology appears naturally in the summary, Skills, and evidence-based bullets.
3. **Human authenticity:** Banned expressions, generic filler, repetitive phrasing, and system-gaming content are absent; the candidate can explain every claim.
4. **Evidence and logic:** Names, dates, degrees, metrics, ownership, units, and causal claims trace to evidence and remain internally consistent.

The draft passes only when all four gates pass together. A structurally correct document still fails if it sounds generic; a human-sounding document still fails if its numbers or ownership cannot be verified.

For a Markdown or plain-text draft, run:

```bash
python scripts/validate_resume.py path/to/resume.md
```

Treat validator failures as blockers. Review warnings with judgment; the script supplements rather than replaces evidence review.

## Rendered Document Review

When producing DOCX or PDF, validate the rendered artifact as well as the source draft:

- Extract its text and confirm headings, dates, bullets, and reading order remain intact.
- Visually inspect every page for clipping, orphaned headings, awkward breaks, crowded type, inconsistent spacing, and excess empty space.
- Confirm contact information remains in the document body and searchable.
- Confirm there is no hidden text, prompt language, JavaScript, form content, or image-only resume content.
- Prefer one readable page for a concise early-career or MBA resume and two readable pages when the supported evidence warrants it. Never shrink text merely to force a page count.

## Research Basis

The stable rules above are grounded in the seven user-selected base articles and supporting primary or corroborating sources. Read [research-basis.md](references/research-basis.md) when the user requests source rationale, asks to update the skill from new hiring research, or challenges an ATS, bias, or authenticity rule.

## Output

Follow the requested deliverables exactly. For an ordinary build, default to a concise optimization/verification report followed by the final resume. For an audit, lead with findings. If a file is requested, provide the finished file rather than only pasting content. State that the four document checks passed only when they did. Never guarantee an interview, employment, universal acceptance, or approval by an undisclosed screening system.

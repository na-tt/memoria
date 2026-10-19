---
name: research-scout
description: Explore and triage academic research using Semantic Scholar. Use when the user wants to discover relevant papers, investigate a research topic, find important or recent work, identify competing approaches, explore citations and related papers, or determine what literature is actually worth reading. Focus on saving the user time by iteratively searching, following promising research trails, discovering alternative terminology, and surfacing high-value or non-obvious papers rather than simply returning keyword-matched results. Do not treat citation count or semantic relevance as sufficient evidence of importance.
---

# Purpose

Use this skill when the user wants to discover, explore, or triage academic research on a topic.

The goal is **not** to produce a comprehensive literature review. The goal is to save the user time by exploring the scholarly literature, identifying papers that deserve attention, discovering useful terminology and research directions, and returning a small, high-value reading list.

Semantic Scholar is the primary scholarly discovery source available to this skill.

Optimize for:

> **"What papers would be worth my time if I were doing this search myself?"**

rather than:

> "What papers contain the most matching keywords?"

# When to use this skill

Use this skill when the user asks things such as:

* "Find papers about X."
* "What research exists on X?"
* "Help me explore the literature on X."
* "Find relevant research for my thesis."
* "What are the important papers on X?"
* "What should I read about X?"
* "Are there papers comparing X and Y?"
* "Find recent work on X."
* "Explore this research area for me."
* "What am I missing in the literature?"

Do **not** use this skill merely to answer a factual question that does not require scholarly literature.

If the user explicitly requests a comprehensive systematic literature review, this skill can perform discovery and triage, but should state that it is not by itself a systematic-review methodology.

# Core principles

## 1. Optimize for useful papers, not search relevance

Semantic similarity alone is insufficient.

A paper should be considered valuable when it is likely to:

* materially inform the user's research question;
* introduce an important concept or terminology;
* provide strong empirical evidence;
* establish or challenge an important result;
* present a competing methodology;
* provide a useful benchmark or dataset;
* represent influential foundational work;
* reveal a research gap;
* connect otherwise separate areas;
* or lead to a valuable citation/research trail.

Do not fill the final list with papers merely because their titles contain the user's keywords.

## 2. Search iteratively

Do not rely on a single query.

Start with the user's terminology, then use promising results to discover:

* alternative terminology;
* abbreviations;
* names of methods;
* names of datasets;
* competing approaches;
* important authors;
* important papers;
* neighboring research communities.

Use these discoveries to perform additional searches.

The search process should generally resemble:

```
user question
    ↓
initial queries
    ↓
promising papers
    ↓
terminology/method discovery
    ↓
refined queries
    ↓
citation exploration
    ↓
related-paper exploration
    ↓
candidate set
    ↓
ranking and triage
```


## 3. Follow the research graph

When a paper looks particularly promising, investigate its surrounding literature.

Where Semantic Scholar provides the relevant capabilities, examine:

* papers it cites;
* papers that cite it;
* related/recommended papers;
* papers by the same authors;
* papers using the same method;
* papers addressing the same problem with a different method.

Citation traversal is especially valuable for discovering papers that keyword search would miss.

Do not blindly traverse every citation. Follow citation paths selectively from high-value papers.

## 4. Look for disagreement and alternatives

Avoid constructing a literature set that merely confirms the first apparent approach.

Actively search for:

* competing methods;
* negative results;
* contradictory findings;
* alternative explanations;
* papers reporting limitations;
* benchmark studies comparing approaches;
* newer work that supersedes older methods.

If the literature appears to converge strongly on one conclusion, say so.

If the literature is divided, explicitly identify the disagreement.

## 5. Balance old and new research

Do not automatically prefer recent papers.

Look for a useful mixture of:

* foundational papers;
* highly influential papers;
* representative methodological papers;
* recent developments;
* recent surveys/reviews;
* recent papers challenging or extending established approaches.

A recent paper may be more relevant than a classic paper, but a classic paper may explain why the entire field uses a particular approach.

## 6. Do not equate citations with quality

Citation count is a useful signal, not a quality metric.

High citation counts can indicate:

* historical importance;
* popularity;
* age;
* broad applicability;
* controversy.

They do not prove methodological quality.

Likewise, a recent low-citation paper may be extremely valuable.

Treat citation influence as one ranking signal among several.

# Search strategy

## Phase 1 — Understand the question

Before searching, identify:

* the core research problem;
* the object/system being studied;
* the desired outcome;
* relevant constraints;
* domain/application;
* methods of interest;
* methods explicitly excluded;
* timeframe, if specified;
* whether the user wants foundational, recent, applied, theoretical, or empirical work.

Do not unnecessarily ask the user for clarification if a useful search can begin immediately.

Infer reasonable search dimensions when possible.

## Phase 2 — Generate query families

Create several conceptually different searches.

Useful query families include:

### Direct terminology

Search the user's wording directly.

### Synonyms

Replace important concepts with plausible alternatives.

### Method terminology

Search for known technical approaches to the problem.

### Problem terminology

Search for descriptions of the underlying problem rather than the user's proposed solution.

### Application terminology

Search within the relevant application/domain.

### Evaluation terminology

Search for benchmarking, evaluation, comparison, performance, limitations, robustness, etc.

### Alternative terminology

Use terminology discovered from promising papers.

Do not generate dozens of nearly identical searches. Prefer a small number of meaningfully different queries.

## Phase 3 — Build the candidate set

For each promising result, record mentally or internally:

* title;
* authors;
* year;
* abstract;
* citation/influence information when available;
* relevance to the user's question;
* methodological contribution;
* useful terminology;
* potential citation trails.

Do not immediately return every candidate.

The purpose of this phase is discovery.

## Phase 4 — Explore promising papers

For the strongest candidates, use available Semantic Scholar capabilities to investigate:

1. Related/recommended papers.
2. References.
3. Citations.
4. Author's other relevant work.
5. Papers using similar methods.
6. Newer work building on the paper.

Prioritize exploration that is likely to reveal something missed by keyword search.

## Phase 5 — Refine the search

After exploring the initial candidate set, ask:

* Did I discover terminology I wasn't searching for?
* Did I discover a method name?
* Did I discover a competing approach?
* Did I discover an important dataset or benchmark?
* Did I discover a research community using different terminology?
* Did I discover an important foundational paper?
* Did I discover an apparent disagreement?
* Did I discover an unexpected adjacent field?

Perform additional targeted searches when the answer is yes.

# Candidate ranking

Rank papers using a combination of:

### Relevance

How directly does the paper address the user's actual research problem?

### Specificity

Does it address the particular constraints or setting the user cares about?

### Research significance

Does it contribute something meaningful to the field?

### Empirical value

Does it contain experiments, measurements, benchmarks, datasets, or evaluations useful to the user's problem?

### Methodological value

Does it introduce or rigorously evaluate a method relevant to the user's work?

### Influence

Is there evidence that the work has substantially influenced subsequent research?

### Recency

Is it recent enough to represent the current state of the field?

### Discovery value

Could this paper lead to an important research trail?

### Surprise / non-obviousness

Would the user plausibly have missed this paper through a conventional keyword search?

Do not reduce these dimensions to a fake numerical score unless the user explicitly requests one.

Use qualitative judgment.

# Output format

Unless the user requests another format, return the result in the following structure.

## Research scout

Briefly state what was searched and what the main finding was.

### Papers worth reading

Return approximately **5–10 papers**, depending on the breadth of the topic.

For each paper provide:

**Title — Year**

* **Why it matters:** Explain specifically why this paper is worth the user's attention.
* **Contribution:** What the paper actually contributes.
* **Relevance:** How it connects to the user's research problem.
* **What to look at:** The experiment, method, result, figure, comparison, or section likely to be most useful.
* **Caveat:** Important limitation, uncertainty, or reason not to overinterpret it.
* **Research trail:** If useful, mention an especially promising citation, related paper, method, author, or terminology discovered from it.

Include a DOI, Semantic Scholar page, arXiv page, or other available scholarly identifier/link when available.

### What stood out

Summarize the most interesting patterns discovered during the search.

Examples:

* an unexpected terminology used by another research community;
* a method that appears much more established than expected;
* a surprisingly common limitation;
* a major methodological divide;
* an old paper that appears foundational;
* a newer paper that substantially changes the picture;
* an apparent research gap.

This section should contain **insight**, not merely another list of papers.

### Competing approaches

When applicable, identify the major competing approaches.

For each:

* what it does;
* why researchers use it;
* its principal advantage;
* its principal limitation;
* which papers represent it.

Do not manufacture a taxonomy when the literature does not support one.

### Rabbit holes

List **2–5 promising directions** that deserve further investigation but are not necessarily central enough for the main reading list.

Examples:

* unfamiliar terminology;
* adjacent research field;
* interesting author/research group;
* promising method;
* dataset;
* benchmark;
* citation cluster.

The purpose is to give the user places to continue exploring.

### Search limitations

Briefly mention important limitations of the search.

Examples:

* only abstracts/metadata were available;
* full text was not inspected;
* some papers may be inaccessible;
* terminology varies substantially between communities;
* publication/citation metadata may be incomplete;
* the search was exploratory rather than systematic.

Do not add this section when the limitation is trivial.

# Evidence discipline

## Never claim to have read what you have not read

If only metadata or an abstract is available, distinguish clearly between:

* what the paper's metadata indicates;
* what the abstract claims;
* what can be inferred from citation/context;
* what was actually inspected in the full text.

Use language such as:

> "The abstract reports..."

rather than:

> "The paper demonstrates..."

when the full paper was not inspected.

Never invent:

* experimental results;
* numerical results;
* datasets;
* methodology details;
* conclusions;
* limitations;
* publication venues;
* authors;
* citation relationships.

## Prefer primary sources

When possible, prioritize:

1. original research papers;
2. high-quality systematic reviews;
3. authoritative survey papers;
4. benchmark papers;
5. reputable preprints when appropriate.

Avoid treating blog posts, papers citing the work, or search-result snippets as substitutes for the original paper.

# Handling surveys and reviews

Reviews and surveys are especially valuable during exploration.

Use them to:

* learn field terminology;
* identify foundational papers;
* discover competing schools of thought;
* locate benchmark datasets;
* identify major unresolved problems.

However, do not let a survey replace the primary paper when the primary result matters to the user's research.

A useful pattern is:

```
survey/review
    ↓
identify important papers
    ↓
inspect primary papers
    ↓
compare current work
```

# Handling narrow research questions

For highly specific questions, prioritize **precision over breadth**.

It is acceptable to return fewer than five papers if the literature genuinely contains only a small number of directly relevant works.

Do not pad the answer with weakly related papers.

Clearly distinguish:

* directly relevant work;
* adjacent work;
* background work.


# Handling broad research questions

For broad topics, progressively narrow the search.

Start by identifying:

* terminology;
* major subfields;
* influential approaches;
* foundational work;
* recent developments.

Then focus the final output on the branches most relevant to the user's stated objective.

Do not attempt to summarize an entire field unless explicitly asked.

# "What sticks out" heuristic

The most valuable result is often not the highest-ranked search result.

Actively look for papers that are:

* surprisingly relevant;
* methodologically unusual;
* influential despite being old;
* recent and rapidly attracting attention;
* frequently cited by otherwise unrelated papers;
* associated with an unexpected terminology;
* representative of a competing approach;
* useful for explaining a limitation;
* capable of changing how the user frames the problem.

When such a paper is found, explicitly tell the user **why it stood out**.

# Stopping criteria

Do not search indefinitely.

Stop when additional searches are mostly returning:

* duplicate papers;
* papers already represented by the same methodology;
* weakly related work;
* papers with no new terminology or research direction;
* increasingly marginal variations of known results.

For a normal exploratory request, aim for a compact, high-quality candidate set rather than exhaustive coverage.

If new searches continue producing genuinely new research directions, continue exploring.

# User interaction

If the user gives feedback such as:

* "these are too theoretical";
* "I only care about computer vision";
* "find alternatives to ROS2";
* "I want papers from the last five years";
* "I'm interested in benchmarking";
* "focus on real-time systems";

then treat that feedback as a **search refinement constraint** and repeat the relevant discovery process.

Do not simply filter the previous results if doing so would miss better papers.

Re-search with the new constraint.

# Zotero handoff

If a Zotero integration is available, do not automatically save every discovered paper.

Only save papers when:

* the user explicitly asks to save them; or
* the user's established workflow explicitly authorizes automatic saving.

When saving papers, prefer the papers in the final "Papers worth reading" set rather than every intermediate search result.

# Final quality check

Before returning the result, verify:

* Did I search using more than one formulation where appropriate?
* Did I discover terminology beyond the user's original wording?
* Did I explore promising papers through citations/related work?
* Did I look for competing approaches?
* Did I balance foundational and recent work where appropriate?
* Did I avoid ranking solely by citation count?
* Did I avoid padding the result with weakly relevant papers?
* Did I clearly distinguish evidence from inference?
* Did I identify what genuinely stood out?
* Did I give the user useful next directions?
* Could the user plausibly save significant time by using this result instead of doing the search themselves?

If the answer to the final question is no, continue searching or improve the synthesis before responding.


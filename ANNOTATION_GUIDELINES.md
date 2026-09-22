# Annotation Guidelines

## 1. Goal

Evaluate each response consistently against the rubric, not against personal preference.

## 2. Scoring scale

### 5 — Excellent
Accurate, complete, relevant, clear and fully compliant. No material defect.

### 4 — Good
Strong response with a minor omission, wording issue or low-impact defect.

### 3 — Acceptable
Useful overall, but has a material weakness that does not completely invalidate the answer.

### 2 — Poor
Multiple material problems, significant omissions, weak instruction following or questionable claims.

### 1 — Very poor
Fundamentally incorrect, unsafe, irrelevant or non-responsive.

## 3. Accuracy

Check factual claims separately from writing quality.

- 5: claims are correct and appropriately supported.
- 4: minor imprecision with no material effect.
- 3: one material claim needs verification.
- 2: multiple unsupported or incorrect claims.
- 1: central answer is substantially false.

Do not reward confident wording when evidence is absent.

## 4. Factuality / hallucination handling

Mark a claim for review when it:

- states a specific fact without evidence where evidence is expected
- invents a citation, source, statistic or quotation
- presents uncertain information as certain
- introduces details not supported by the provided context
- contradicts reference material

A risk flag does not automatically prove hallucination.

## 5. Relevance

Ask: "Does this answer the user's actual request?"

Penalise unnecessary digressions, generic filler and answers that address a different question.

## 6. Completeness

Check every explicit requirement in the user prompt.

Use a checklist when the prompt contains multiple requested components.

## 7. Instruction following

Check constraints such as:

- requested format
- word/character limit
- tone
- required sections
- exclusions
- requested audience
- output structure

## 8. Safety

Escalate content involving meaningful risk. Do not use personal opinion as a substitute for the safety rubric.

## 9. Decision labels

**PASS**
- overall score >= configured pass threshold
- no blocking error
- no unresolved high-risk safety/factuality issue

**REVIEW**
- borderline score
- factuality requires verification
- evaluator disagreement is material
- evidence is incomplete
- ambiguity prevents confident classification

**FAIL**
- overall score < configured fail threshold
- central answer is materially wrong
- explicit requirements are substantially ignored
- blocking safety or policy issue is present

## 10. Calibration

Before production annotation:

1. independently score 10–20 shared examples
2. compare disagreements
3. discuss rubric interpretation
4. record edge cases
5. repeat until agreement stabilises
6. periodically re-calibrate

## 11. Annotation principles

- Evaluate the response, not the author.
- Apply the same rubric across models.
- Record evidence-based rationales.
- Avoid changing standards because a response "sounds good".
- Separate factuality from style.
- Use REVIEW when evidence is insufficient rather than guessing.

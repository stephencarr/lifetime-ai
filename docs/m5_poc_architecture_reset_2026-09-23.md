# M5 POC architecture reset — 23 September 2026

## Decision

The local rule-extractor, 128-claim scan, and finite answer grammar are diagnostic scaffolding. Their synthetic pass does not prove the intended Lifetime AI product. Do not present the current chat UI as a useful POC or invite participant UAT. A convincing M5 POC must run the same class of semantic technology intended for the product at all three points: construction, reconciliation, and use of persistent state. Replace diagnostic rules as the product path; retain them only as labeled baselines and regression controls.

## One real vertical slice

### 1. Construct claims from ordinary chat

Persist the untouched source event. A pinned local generative model proposes zero or more structured claims: subject/actor, relation, object, polarity, conditional and contextual scope, effective interval, assertion strength, and exact supporting source span. Quoted speech, third-party statements, questions, hypotheticals, and irrelevant messages may yield no first-party claim. Record model ID, weights hash, prompt/schema version, latency, and decision. The model has no direct write authority.

### 2. Check meaning and reconcile state

A separate semantic support check tests whether each proposed claim is entailed by its cited source span at the stated actor, scope, and time. Compare supported proposals with current candidate state for reinforcement, contradiction, narrower scope, supersession, or unrelatedness. Preserve equal-authority contradictions and uncertainty. The deterministic transition validator checks identity, source validity, authorization, schema, temporal consistency, and atomic provenance; it cannot by itself decide semantic truth. A model decision with missing weights, malformed output, unsupported source, or low calibrated confidence abstains and leaves state unchanged. Corrections and deletions remain provenance-linked operations.

### 3. Retrieve and use valid state

Index current state by tenant/user, actor, relation, scope, status, time, and source provenance. Use lexical and dense candidate retrieval, then a semantic reranker/support check against the question. The context compiler passes a bounded set of current claims, exact source spans, counterevidence, and inclusion reasons to the reply model. The reply may assert only what those sources support and must cite them. An incomplete search or unsupported answer abstains. Broad inventory questions require a current-state enumeration or a narrower request; an arbitrary top-k result cannot establish completeness. Deletion and expiry invalidate both state and search-index entries.

The first POC can use SQLite for canonical state and lexical search if measured capacity permits; an embedding index is a replaceable candidate source. Index technology is not the truth layer. The current full scan is removed from the product route once an indexed route meets the frozen retrieval and answer gates. There is no product claim at 128 claims.

## Technology choice and machine constraint

The target machine available to this work is an Apple M4 MacBook Air with 16 GB RAM. The first implementation now uses local llama.cpp with a pinned Qwen3-8B GGUF generator and a separate pinned BGE small embedding model. The generator proposes claims and checks source support and answer support; SQLite retains canonical state and FTS5 provides lexical candidates; USearch HNSW provides dense candidates. The model path is an explicit terminal entry point, separate from the diagnostic browser path. Availability, identity, and weight checks fail closed. This is an architectural first iteration, not a passed quality gate. The same generator currently performs proposal and verification, so its errors may correlate. A mock provider may test plumbing, but cannot count as POC evidence.

Four retained runs of the frozen integrated development set have not passed. The strongest run reached 13/14 clear captures and 8/10 supported answers but still promoted a one-off episode. The later typed-schema run regressed to 6/14 clear captures and promoted boilerplate gratitude as ongoing state. See [the measured development record](m5_model_development_2026-09-23.md). This local model configuration cannot be used for participant UAT or presented as concept proof.

## Evidence required before participant UAT

1. Freeze a product-shaped development instrument **before** implementation scoring, with original conversational messages and source-span labels. Include paraphrase, quoted and third-party text, negation, scope, temporal change, correction, contradiction, deletion, and irrelevant material. Keep every failed item and every repair attempt. The previous 18-case capture and 48-question answer sets remain historical diagnostic instruments.
2. Measure claim proposal recall, false durable capture, actor/scope/time accuracy, source-span entailment, reconciliation decisions, candidate recall at a fixed budget, supported-answer precision, citation correctness, deletion leakage, abstention, latency, memory, and total model work. Report both oracle-state retrieval and end-to-end results so construction errors are separated from use errors.
3. Run retrieval with growing realistic state and distractor counts, including 10,000, 100,000, and 1,000,000 claims in a synthetic scale test. Freeze the index configuration and thresholds before scoring. A tiny corpus with every claim scanned cannot establish scale.
4. Only after the integrated local model path passes development gates, run a newly selected participant-approved independent preflight. Do not tune on it and call the rerun independent. Resolve the current ledger-retention versus physical-erasure expectation before UAT. Formal G5 remains a separate paired comparison with the rolling-summary-and-retrieval baseline and total lifecycle cost.

## Immediate engineering order

Select and verify a local inference runtime and model on the target machine; define the structured claim/source-span schema; build the pinned-model extractor and semantic support checker; integrate their proposals through the existing validator; add indexed hybrid candidate retrieval and an evidence compiler; then freeze and run the integrated development instrument. Keep the diagnostic browser route explicitly labeled until that path works end to end. If a component cannot run or meet quality on this machine, report that as a POC failure or revise the hardware/model premise—do not replace it with keywords while claiming the concept works.

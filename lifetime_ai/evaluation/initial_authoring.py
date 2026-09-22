"""Original first-batch narratives and a deterministic draft-only renderer.

The three opportunities within each history concern distinct scoped items.  The
fourth probes the brief's hostile boundary. No pilot records or predictions are
read, and this module cannot mark a record reviewed or choose a final split.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from .canonical import sha256_value, strict_json_loads
from .frozen_g4 import _frozen_schema_validator
from .frozen_g4_pipeline import (
    BLUEPRINT_SCHEMA,
    _schema_validator,
    render_blueprint,
    validate_blueprints_against_authoring_matrix,
)
from .validation import validate_history


RELATIONS = ("supports", "contradicts", "narrows_scope", "supersedes", "unrelated", "uncertain")
MATRIX_PATH = Path(__file__).resolve().parents[2] / "evaluation/blueprints/frozen-g4-v0.1/authoring-matrix.json"
DEFAULTS = {
    "supports": ("accept", "reinforce", "none", None),
    "contradicts": ("abstain", "preserve_conflict", "clarify", "contradiction_without_repair"),
    "narrows_scope": ("accept", "add_scoped_item", "none", "scope_narrowing"),
    "supersedes": ("accept", "close_and_replace", "none", "temporal_supersession"),
    "unrelated": ("no_op", "none", "silence", "irrelevant_noise"),
    "uncertain": ("abstain", "none", "clarify", "genuine_ambiguity"),
}
RELATIONSHIP_FEATURE = {
    "supports": "preference_reinforcement",
    "contradicts": "contradiction_without_repair",
    "narrows_scope": "scope_narrowing",
    "supersedes": "temporal_supersession",
    "unrelated": "irrelevant_noise",
    "uncertain": "genuine_ambiguity",
}

# A variation changes the evidence boundary or its presentation, rather than
# merely renaming actors in a pilot example. All text here was authored anew.
NARRATIVES = {
    1: [
        ("Aster", ("profile", "contacts", "notifications"),
         "The Aster mobile client's {target} account-management requests currently target API v4.",
         "API owner Mina confirms from the live routing registry: Aster mobile still sends {target} account-management requests to v4. This confirmation concerns the same current release; the desktop route is tracked separately.",
         "The Aster desktop client sends profile account-management requests to v4. The mobile route was not inspected in this report."),
        ("Beacon", ("avatar", "security", "billing-address"),
         "Beacon's installed mobile release uses API v4 for account management in the {target} workflow.",
         "Approved release checklist, signed by API owner Noel: the mobile {target} account-management route has passed the v4 compatibility check and remains assigned to v4 for the current release. The next sprint's icon work has no route change.",
         "Beacon's browser release passed its v4 avatar account-management checklist; this entry covers the browser release only."),
        ("Cove", ("email", "devices", "recovery"),
         "For Cove mobile, API v4 serves the account-management {target} workflow during the September release.",
         "Signed compatibility report from API maintainer Inez: September Cove mobile {target} traffic continues on v4. The report corroborates the published routing entry. Release notes about search are attached for scheduling only.",
         "Cove's kiosk email workflow uses API v4 for account management during September. The kiosk has its own release and routing entry."),
    ],
    2: [
        ("Delta", ("card", "wallet", "voucher"),
         "Client telemetry says every Delta mobile {target} checkout request in rollout R7 during 09:00–09:05 used API v3.",
         "Gateway observer, with the same authority as client telemetry: every Delta mobile {target} checkout request in rollout R7 during 09:00–09:05 used API v4. Both observation sources are retained; neither has source precedence and no route-change event is known.",
         "A later gateway export again reports all Delta mobile card checkout requests in R7 at 09:00–09:05 on v4; its later publication does not describe a later traffic window."),
        ("Ember", ("north", "central", "south"),
         "The regional client counter records all Ember mobile checkout calls in the {target} region, rollout R8, at 10:00–10:10 as API v3.",
         "The regional gateway counter records all Ember mobile checkout calls in the same {target} region, R8, 10:00–10:10 as API v4. The two counters have equal trust, full overlapping scope, and no intervening reconfiguration record.",
         "The north-region gateway bulletin is newer but still concerns Ember R8 at 10:00–10:10: all checkout calls were v4. There is no priority rule between counters."),
        ("Fjord", ("express", "standard", "gift"),
         "The live client log reports all Fjord mobile {target} checkout requests in R9, 11:00–11:15, using API v3.",
         "A delayed gateway batch for Fjord R9 states that all mobile {target} checkout requests at 11:00–11:15 used v4. It arrived after the client log but covers exactly that observation period. The gateway and client are equally authoritative.",
         "A second late batch says Fjord R9 express checkout used v4 for every request at 11:00–11:15. The import time is later; the observed time is unchanged."),
    ],
    3: [
        ("Grove", ("personal", "team", "partner"),
         "Grove mobile {target} account-management requests use API v4 by default.",
         "API owner: within Grove mobile {target} account management, offline password-reset requests remain on v3 until their queued migration completes. Other requests retain the default route.",
         "An equally trusted monitor says all Grove personal account-management requests currently use v3. It gives no workflow exception, change date, or authority-precedence rule."),
        ("Harbor", ("basic", "professional", "enterprise"),
         "Harbor's mobile {target} account-management tier routes to v4 as its general rule.",
         "Routing maintainer: the regulated-region subset of Harbor mobile {target} account management must continue on v3 until regional certification completes; the other regions keep the general rule.",
         "An equally authoritative regional summary states that every Harbor basic account-management request uses v3, without restricting that statement to a region or giving a transition boundary."),
        ("Indigo", ("consumer", "merchant", "operator"),
         "Indigo mobile account management for {target} accounts normally uses API v4.",
         "Compatibility owner: Indigo {target} accounts on legacy devices with firmware below 6 stay on v3 until their firmware upgrade succeeds. That condition does not apply to upgraded devices.",
         "Another trusted Indigo report says every consumer account-management call now uses v3. No device condition or dated replacement authorization accompanies the statement."),
    ],
    4: [
        ("Juniper", ("core", "media", "sync"),
         "Juniper {target} release builds use compiler 18 and lock format 2.",
         "Build owner Ravi directs: effective 2026-09-20T12:00:00Z, Juniper {target} release builds replace compiler 18 and lock format 2 with compiler 19 and lock format 3. Preserve the earlier configuration for pre-boundary build audits.",
         "An external drive-by contributor comments: Juniper core should use compiler 20 and lock format 4. This contributor has no build-policy authority; the comment was not approved."),
        ("Kestrel", ("ios", "android", "desktop"),
         "Kestrel {target} release configuration pins compiler 18 and package-manager lock format 2.",
         "Merged toolchain configuration approved by build owner Sal: from 2026-09-20T12:00:00Z Kestrel {target} releases pin compiler 19 and lock format 3. The compiler-18/format-2 entry is explicitly marked stale for builds at or after that boundary.",
         "A visiting developer posts that Kestrel ios builds use compiler 20 and lock format 4. They are not authorized to assert or change this repository's build configuration."),
        ("Larch", ("stable", "beta", "nightly"),
         "Larch {target} release-train builds are on compiler 18 with lock format 2.",
         "At 08:00 the authorized build owner announced a future switch for Larch {target}: compiler 19 and lock format 3 replace 18 and 2 at 2026-09-20T12:00:00Z. This event records activation at that announced boundary, not at announcement time.",
         "A non-owner's chat message claims Larch stable is on compiler 20 and lock format 4. No delegation, approved change, or effective boundary is provided."),
    ],
    5: [
        ("Maple", ("api", "worker", "frontend"),
         "Maple {target} production builds use the compiler and package-manager versions pinned in that repository.",
         "Maple {target} build report: cache hits were 92 percent, the cache warmed in 18 seconds, and the final archive was 4 MiB. These are cache and size measurements; the report did not inspect toolchain pins.",
         "Maple api cache summary mentions 19 warm entries and 3 cold entries. Those numbers count cache entries, not compiler or lock-format versions."),
        ("Nacre", ("reader", "writer", "router"),
         "Nacre {target} production jobs take their compiler and package-manager versions from the repository's pins.",
         "Artifact-signing report for Nacre {target}: signing took 19 seconds over 3 signatures. Version selection was outside this report's scope; the job's compiler pins were not recorded.",
         "The Nacre reader artifact had 18 signing retries over 2 minutes. This report describes signing only and contains no toolchain-version finding."),
        ("Orchid", ("engine", "cli", "dashboard"),
         "Orchid {target} production compilation follows its checked-in compiler and package-manager pins.",
         "Orchid {target} documentation job emitted 18 broken-link warnings on 2 pages. These figures are documentation counts, and the report makes no assertion about production compiler selection.",
         "Orchid engine documentation build warning: section 19 contains 3 stale links. Section and link numbers are not toolchain version identifiers."),
    ],
    6: [
        ("Pine", ("r1", "r2", "r3"),
         "Pine release branch {target} uses compiler 18, as pinned in its checked-in toolchain file.",
         "A late release-room note near the Pine {target} discussion says: 'It was switched back for the release.' The note does not identify what 'it' is, the compiler version, the branch, or when a switch took effect.",
         "A newer Pine note adds, 'Yes, that one was restored.' It gives no antecedent, branch, compiler version, or occurrence time."),
        ("Quartz", ("autumn", "winter", "spring"),
         "Quartz release branch {target} compiles with version 18 from its checked-in toolchain file.",
         "A copied Quartz release note reads: 'Compiler [identifier omitted] was put back on [branch omitted].' The source gives neither the previous value nor the affected branch or effective date, even though it appears near the {target} notes.",
         "The latest Quartz digest repeats 'compiler [identifier omitted] restored' without identifying the branch or the date to which restoration applies."),
        ("Rowan", ("release-a", "release-b", "release-c"),
         "Rowan {target} builds use the checked-in compiler-18 pin.",
         "A Rowan report entered after the {target} discussion says a compiler switch-back happened sometime between September 18 and 20. It could concern either of two release branches mentioned in the meeting; neither branch nor restored version is specified.",
         "A later Rowan recording says 'the earlier branch was switched back before signoff.' It still omits which branch, version, and effective time."),
    ],
}


def _event(event_id: str, sequence: int, content: str, *, authorized: bool = True,
           occurred_at: str | None = None) -> dict[str, Any]:
    timestamp = occurred_at or f"2026-09-20T{8 if sequence <= 4 else 12:02d}:{sequence:02d}:00Z"
    return {"event_id": event_id, "sequence": sequence, "occurred_at": timestamp,
            "recorded_at": f"2026-09-20T13:{sequence:02d}:00Z", "actor": "user" if authorized else "external",
            "event_type": "message", "content": content,
            "authority": {"may_assert_user_state": authorized, "may_request_transition": authorized,
                          "reason": "Authorized owner or designated observation source for the stated scope." if authorized else "External contributor has no delegated state or transition authority."},
            "sensitivity": "normal", "source_status": "present", "deletion_target_ids": [], "metadata": {}}


def _checkpoint(history_id: str, sequence: int, events: list[dict[str, Any]],
                state: list[dict[str, Any]],
                invalidated_derivatives: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    lifecycle_status: dict[str, str] = {}
    for event in events:
        if event["sequence"] > sequence or event["event_type"] not in {"deletion", "redaction"}:
            continue
        status = "deleted" if event["event_type"] == "deletion" else "redacted"
        lifecycle_status.update({target: status for target in event["deletion_target_ids"]})
    return {"checkpoint_id": f"{history_id}-cp-{sequence}",
            "historical_assertions": [
                {"assertion_id": f"{event['event_id']}-assertion", "proposition": event["content"],
                 "asserted_at": event["occurred_at"], "source_event_ids": [event["event_id"]],
                 "source_status": lifecycle_status.get(event["event_id"], "present")}
                for event in events if event["sequence"] <= sequence
                and event["event_type"] in {"message", "observation", "action_outcome"}],
            "current_state": deepcopy(state), "inferences": [], "operating_assumptions": [],
            "invalidated_derivatives": deepcopy(invalidated_derivatives or [])}


def _family_narrative(family: int, variant: int, plan: dict[str, Any]):
    if family in NARRATIVES:
        return NARRATIVES[family][variant]
    product = f"{plan['domain'].replace('-', ' ').title()} {variant + 1}"
    targets = ("primary", "secondary", "fallback")
    initial = (
        f"For {product}, the {{target}} configuration currently records setting 18 "
        f"for {plan['scenario_focus']}."
    )
    relation = plan["primary_relationship"]
    confirmation = {
        "supports": "Authorized maintainer record: the {target} configuration remains on setting 18 for the current validity period.",
        "contradicts": "An equally authoritative audit reports setting 17, not setting 18, for the same {target} configuration and interval; no precedence rule is recorded.",
        "narrows_scope": "Authorized maintainer clarification: the {target} configuration uses setting 17 only for recovery-mode requests; all ordinary requests retain setting 18.",
        "supersedes": "Authorized owner directive: effective 2026-09-20T12:00:00Z, setting 19 replaces setting 18 for the {target} configuration.",
        "unrelated": "An operations report for the {target} documentation job counted 18 cache hits and 3 retries; it did not inspect the configuration setting.",
        "uncertain": "A late note beside the {target} discussion says 'put the earlier one back there' but omits the setting, scope, and effective time.",
    }[relation]
    hostile = (
        "A separate preview environment report mentions setting 18, but it does not "
        "cover the production configuration evaluated here."
    )
    return product, targets, initial, confirmation, hostile


def _labels_by_history(plan: dict[str, Any]) -> list[list[str]]:
    """Allocate the exact family mix while placing the primary class in every history."""
    primary = plan["primary_relationship"]
    lifecycle = bool({
        "explicit_expiry", "source_deletion", "derivative_invalidation",
        "independent_support_survives",
    } & set(plan["required_features"]))
    anchor = "unrelated" if lifecycle else primary
    counts = dict(plan["planned_relationship_pair_counts"])
    groups = [[anchor], [anchor], [anchor]]
    counts[anchor] -= 3
    remaining = [
        (label, index)
        for label, count in counts.items()
        for index in range(count)
    ]
    remaining.sort(key=lambda item: sha256_value({
        "family": plan["family_id"], "opportunity": list(item)
    }))
    for label, _ in remaining:
        destination = min(range(3), key=lambda index: (len(groups[index]), index))
        groups[destination].append(label)
    if any(len(group) != 4 for group in groups):
        raise ValueError("authoring plan could not be allocated to three four-pair histories")
    return groups


def _rationale(relation: str, hostile: bool, family: int) -> str:
    if family > 6:
        return {
            "supports": "The authorized record confirms the same configuration, setting, scope, and validity period without introducing a replacement.",
            "contradicts": "Equal-authority records assert incompatible settings for the same scope and interval; preserve the conflict and request clarification because arrival order gives no precedence.",
            "narrows_scope": "The authorized note creates a proper child-scope exception while leaving the general configuration active outside that condition.",
            "supersedes": "The authorized directive expressly replaces setting 18 with setting 19 at the stated boundary while preserving the earlier historical interval.",
            "unrelated": "The operational counts concern a separate documentation job and provide no evidence about the evaluated configuration setting.",
            "uncertain": "The note omits the setting, affected scope, and effective time, so no unique support, contradiction, or replacement can be inferred.",
        }[relation]
    if hostile:
        return {
            1: "A desktop/browser/kiosk route is a different client scope; matching API words do not corroborate mobile state.",
            2: "The second export still covers the same occurrence interval and asserts v4 against v3; later recording provides no replacement precedence.",
            3: "The new universal v3 claim conflicts with the general v4 rule; it lacks the earlier exception's child condition and cannot inherit it.",
            4: "The incompatible compiler claim is contradictory to the current configuration, but its non-owner source cannot change authorized state.",
            5: "The version-like numerals measure cache/signing/documentation quantities, not compiler selection; no state or outreach is warranted.",
            6: "The additional late note still lacks a referent, branch and version, so its newer recording cannot decide a unique semantic relation.",
        }[family]
    return {
        "supports": "The authorized confirmation names the same mobile workflow, API version and validity period, with no exception or replacement instruction.",
        "contradicts": "The equally trusted sources make incompatible universal claims about the same traffic and occurrence window. Preserve both observations and clarify; arrival order establishes no precedence.",
        "narrows_scope": "The owner explicitly identifies a proper child scope and its end condition. The default v4 rule and bounded v3 exception coexist without closing the default.",
        "supersedes": "An authorized directive expressly replaces both pinned values at a stated boundary. Close the old configuration's interval and keep its historical evidence while activating the new one.",
        "unrelated": "The report contains operational measurements but no assertion about which compiler or package-manager versions production uses. Shared vocabulary and numerical overlap are immaterial.",
        "uncertain": "The apparent change may concern this candidate, but omitted branch, version or referent prevents choosing support, contradiction or replacement without inventing facts.",
    }[relation]


def _special_rationale(feature: str | None, relation: str, family: int) -> str:
    if feature == "commitment_resolution":
        return "The completion record confirms and resolves the previously recorded commitment; it does not invent a replacement configuration."
    if feature == "explicit_expiry":
        return "The evaluator clock reaches the candidate's explicit valid-until boundary, so the bounded state expires without replacement evidence."
    if feature == "commitment_failure":
        return "The submitted commitment interval ends before it begins; reject the invalid transition and investigate its source without mutating state."
    if feature in {"source_deletion", "derivative_invalidation", "independent_support_survives"}:
        return "The deletion removes the sole source for the recorded derivative, so that derivative is invalidated; the separately sourced parent state remains active."
    if feature == "unauthorized_injection_text":
        return "The external text conflicts with recorded state but has no delegated transition authority, so it is rejected without mutation or outreach."
    if feature == "late_or_retroactive_report":
        return "The report's occurrence time, rather than its later recording time, governs temporal interpretation; no unstated precedence is inferred."
    return _rationale(relation, False, family)


def _supplemental_evidence(family: int, variant: int, product: str, target: str,
                           label: str, original: str) -> tuple[str, str, str]:
    """New evidence for mixed opportunities; returns text, new state, child scope."""
    api = family <= 3
    generic = family > 6
    if generic:
        subject = f"{product} {target} configuration"
        old, alternative, replacement = "18", "17", "19"
        value = lambda version: f"setting {version}"
        condition = (
            "recovery-mode requests until the incident closes",
            "regulated requests until certification completes",
            "legacy-client requests until their migration succeeds",
        )[variant]
    else:
        old = "v3" if family == 2 else "v4" if api else "18"
        alternative = "v4" if family == 2 else "v3" if api else "17"
        replacement = "v5" if api else "19"
        subject = f"{product} mobile {target} requests" if api else f"{product} {target} release builds"
        value = (lambda version: f"API {version}") if api else (lambda version: f"compiler {version}")
        condition = (("offline password reset until queued migration completes",
                      "regulated region until certification completes", "firmware below 6 until successful upgrade")[variant]
                     if api else ("emergency rollback builds until recovery completes",
                                  "legacy-target builds until the compatibility audit closes",
                                  "reproducibility audit builds until archived artifacts are verified")[variant])
    new_state = f"{subject} use {value(replacement)}."
    frames = ("The responsible maintainer's signed note", "The approved configuration audit", "The owner-signed release log")
    intro = frames[variant]
    text = {
        "supports": f"{intro} independently confirms the existing entry: {original} No route, scope or version change has been authorized for this period.",
        "contradicts": f"{intro} reports {subject} on {value(alternative)}, not {value(old)}, for the same interval covered by the earlier entry. The two sources have equal authority; neither overrides the other, and no transition boundary is given.",
        "narrows_scope": f"{intro} clarifies the earlier general {value(old)} entry: the child workflow '{condition}' for {subject} instead uses {value(alternative)}. The earlier entry applies to all other workflows; the exception ends when its stated condition ends.",
        "supersedes": f"{intro} authorizes {subject} to replace {value(old)} with {value(replacement)} effective 2026-09-20T12:00:00Z. The earlier configuration remains the historical record before noon; this event records activation at noon.",
        "unrelated": f"{intro} for {product}'s separate documentation project reports 18 cache hits and 3 retries during {target} publishing. These are operational counts; the evaluated configuration setting was not inspected.",
        "uncertain": f"A note filed after the {product} {target} discussion reads, 'The earlier setting was put back for that one.' It omits the setting, version, affected workflow and effective time; the meeting covered several different projects.",
    }[label]
    return text, new_state, condition


def build_initial_history(
    family: int, variant: int, labels: list[str], plan: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Build one blueprint template; review and partition metadata are added later."""
    if plan is None:
        plan = strict_json_loads(MATRIX_PATH.read_text(encoding="utf-8"))["families"][family - 1]
    product, original_targets, initial, confirmation, hostile_text = _family_narrative(
        family, variant, plan
    )
    targets = (*original_targets, f"{original_targets[0]}-recovery")
    hid = f"g4-h{family:03d}-{variant + 1}"
    relation = plan["primary_relationship"]
    supplemental_features = set(plan["required_features"]) - {RELATIONSHIP_FEATURE[relation]}
    lifecycle_plan = bool({
        "explicit_expiry", "source_deletion", "derivative_invalidation",
        "independent_support_survives",
    } & supplemental_features)
    special_pair_index = labels.index("unrelated" if lifecycle_plan else relation)
    events, state = [], []
    for index, target in enumerate(targets, 1):
        source = initial.format(target=target)
        if family == 5:
            source += " Its checked-in compiler pin is version 18."
        event = _event(f"{hid}-e{index}", index, source)
        events.append(event)
        label = labels[index - 1]
        special_here = index - 1 == special_pair_index and bool(supplemental_features)
        special = next(iter(sorted(supplemental_features)), None) if special_here else None
        if special == "commitment_resolution":
            source = (
                f"The team committed to move {product} {target} configuration from "
                "setting 18 to setting 19 after validation completes."
            )
            event["content"] = source
        elif special == "explicit_expiry":
            source = (
                f"The temporary setting 18 authorization for {product} {target} "
                "configuration is valid until 2026-09-20T12:00:00Z."
            )
            event["content"] = source
        elif special in {"source_deletion", "derivative_invalidation", "independent_support_survives"}:
            source = (
                f"Sole-source observation: the derived operational conclusion for "
                f"{product} {target} configuration is setting 18."
            )
            event["content"] = source
        kind = "commitment" if special == "commitment_resolution" else "fact"
        valid_until = "2026-09-20T12:00:00Z" if special == "explicit_expiry" else None
        state.append({"semantic_item_ref": f"{hid}-item{index}", "kind": kind,
                      "proposition": event["content"], "scope": {"product": product, "workflow": target},
                      "status": "active", "valid_from": event["occurred_at"], "valid_until": valid_until,
                      "evidence_ids": [event["event_id"]], "counterevidence_ids": [],
                      "epistemic_basis": (
                          "inferred" if special in {
                              "source_deletion", "derivative_invalidation",
                              "independent_support_survives",
                          } else "asserted"
                      ),
                      "sensitivity": "normal"})  # rendered event text never carries confidentiality/PII language
    if "independent_support_survives" in supplemental_features:
        support_event = _event(
            f"{hid}-independent-support", 5,
            f"Independent audit: the parent configuration record for {product} remains setting 18; it does not establish the deleted derivative.",
            occurred_at="2026-09-20T08:05:00Z",
        )
        events.append(support_event)
        state.append({
            "semantic_item_ref": f"{hid}-independent-parent", "kind": "fact",
            "proposition": support_event["content"],
            "scope": {"product": product, "workflow": "independent-parent"},
            "status": "active", "valid_from": support_event["occurred_at"],
            "valid_until": None, "evidence_ids": [support_event["event_id"]],
            "counterevidence_ids": [], "epistemic_basis": "asserted",
            "sensitivity": "normal",  # rendered event text never carries confidentiality/PII language
        })
    baseline_sequence = len(events)
    snapshots, pools, inputs, golds, tasks, task_gold = [], [], [], [], [], []
    invalidated_derivatives: list[dict[str, Any]] = []
    deleted_source_content: dict[str, str] = {}
    checkpoints = [_checkpoint(hid, baseline_sequence, events, state, invalidated_derivatives)]
    for ordinal in range(1, 5):
        hostile = False
        index = ordinal - 1
        candidate = state[index]
        sequence = ordinal + baseline_sequence
        eid, pid = f"{hid}-e{sequence}", f"{hid}-p{ordinal}"
        label = labels[ordinal - 1]
        disposition, effect, action, tag = DEFAULTS[label]
        tags = (
            [RELATIONSHIP_FEATURE[relation]]
            if label == relation and RELATIONSHIP_FEATURE[relation] in plan["required_features"]
            else []
        )
        special = (
            next(iter(sorted(supplemental_features)), None)
            if index == special_pair_index and (label == relation or lifecycle_plan) else None
        )
        if special is not None:
            tags.extend(sorted(supplemental_features))
        content, replacement_proposition, child_condition = _supplemental_evidence(
            family, variant, product, targets[index], label, candidate["proposition"])
        if label == relation and family <= 6:
            content = confirmation.format(target=targets[index])
            if family == 4:
                replacement_proposition = f"{product} {targets[index]} release builds use compiler 19 and lock format 3."
        occurred_at = "2026-09-20T12:00:00Z" if label == "supersedes" else None
        event = _event(eid, sequence, content, occurred_at=occurred_at)
        if special == "commitment_resolution":
            disposition, effect = "accept", "resolve"
            content = event["content"] = (
                f"Authorized completion record: the commitment for {product} {targets[index]} is complete."
            )
        elif special == "explicit_expiry":
            disposition, effect = "accept", "expire"
            action = "none"
            event.update({
                "actor": "evaluator", "event_type": "time_advance",
                "content": (
                    f"The evaluator clock reaches the explicit validity boundary for "
                    f"{product} {targets[index]} configuration."
                ),
                "occurred_at": "2026-09-20T12:00:00Z",
                "authority": {
                    "may_assert_user_state": False, "may_request_transition": True,
                    "reason": "Evaluator clock event advances the lifecycle boundary.",
                },
                "metadata": {"advance_to": "2026-09-20T12:00:00Z"},
            })
        elif special == "commitment_failure":
            disposition, effect, action = "reject_invalid", "none", "investigate"
            event["content"] = (
                "A purported commitment window begins on 2026-10-01 but ends on "
                "2026-09-01. The source supplies no explanation for the reversed interval."
            )
            event["metadata"] = {
                "valid_from": "2026-10-01T00:00:00Z",
                "valid_until": "2026-09-01T00:00:00Z",
            }
        elif special in {"source_deletion", "derivative_invalidation", "independent_support_survives"}:
            disposition, effect, action = "accept", "invalidate", "none"
            source_id = candidate["evidence_ids"][0]
            deleted_source_content[source_id] = next(
                item["content"] for item in events if item["event_id"] == source_id
            )
            event.update({
                "actor": "user", "event_type": "deletion",
                "content": "Delete the identified sole-source observation under the recorded deletion policy.",
                "deletion_target_ids": [source_id],
            })
        elif special == "unauthorized_injection_text":
            disposition, effect, action = "reject_unauthorized", "none", "silence"
            event.update({
                "actor": "external",
                "authority": {
                    "may_assert_user_state": False, "may_request_transition": False,
                    "reason": "Imported text has no delegated state-transition authority.",
                },
            })
        # No supports-labeled event in this generator ever carries genuine
        # outreach/contact context in its rendered text, so the mechanical
        # "outreach_candidate" override is removed rather than exempting
        # archetypes one at a time. Pairs keep their default "none" action.
        if special == "late_or_retroactive_report":
            event["occurred_at"] = "2026-09-18T12:00:00Z"
            event["recorded_at"] = "2026-09-20T13:00:00Z"
        events.append(event)
        snap_ids = []
        selected_snapshot = None
        for snapshot_index, item in enumerate(state, 1):
            snapshot = {"snapshot_id": f"{hid}-s{ordinal}-{snapshot_index}",
                        "item_id": item["semantic_item_ref"], "captured_after_sequence": sequence - 1,
                        "canonical_payload": {key: deepcopy(item[key]) for key in (
                            "kind", "proposition", "scope", "status", "valid_from", "valid_until", "epistemic_basis", "sensitivity")},
                        "source_event_ids": list(item["evidence_ids"]),
                        "counterevidence_event_ids": list(item["counterevidence_ids"])}
            snapshot["sha256"] = sha256_value(snapshot["canonical_payload"])
            snapshots.append(snapshot)
            snap_ids.append(snapshot["snapshot_id"])
            if item is candidate:
                selected_snapshot = snapshot["snapshot_id"]
        pool = {"candidate_pool_id": f"{hid}-pool{ordinal}", "captured_after_sequence": sequence - 1,
                "snapshot_ids": snap_ids}
        pool["sha256"] = sha256_value({"captured_after_sequence": pool["captured_after_sequence"],
                                       "snapshot_ids": pool["snapshot_ids"]})
        pools.append(pool)
        inputs.append({"pair_id": pid, "event_id": eid, "candidate_item_id": candidate["semantic_item_ref"],
                       "candidate_snapshot_id": selected_snapshot, "candidate_pool_id": pool["candidate_pool_id"],
                       "context_event_ids": [item["event_id"] for item in events[:-1]]})
        affected = [] if effect == "none" else [candidate["semantic_item_ref"]]
        new_ids = []
        if effect == "reinforce":
            candidate["evidence_ids"].append(eid)
        elif effect == "preserve_conflict":
            candidate["status"] = "disputed"
            candidate["counterevidence_ids"].append(eid)
        elif effect in {"add_scoped_item", "close_and_replace"}:
            child = deepcopy(candidate)
            child["semantic_item_ref"] = f"{hid}-derived{ordinal}"
            child["evidence_ids"], child["counterevidence_ids"] = [eid], []
            child["valid_from"] = event["occurred_at"]
            child["proposition"] = content
            if effect == "add_scoped_item":
                child["scope"]["condition"] = child_condition
            else:
                candidate["status"] = "expired"
                candidate["valid_until"] = event["occurred_at"]
                child["proposition"] = replacement_proposition
            state.append(child)
            new_ids.append(child["semantic_item_ref"])
        elif effect == "resolve":
            candidate["status"] = "resolved"
            candidate["valid_until"] = event["occurred_at"]
            candidate["evidence_ids"].append(eid)
        elif effect == "expire":
            candidate["status"] = "expired"
        elif effect == "invalidate":
            candidate["status"] = "invalidated"
            candidate["valid_until"] = event["occurred_at"]
            candidate["evidence_ids"].append(eid)
            derivative_id = f"{candidate['semantic_item_ref']}-derivative"
            invalidated_derivatives.append({
                "derivative_id": derivative_id,
                "invalidated_by_event_id": eid,
                "reason": "source_deleted",
            })
        semantic_relationship = (
            "unrelated"
            if special in {
                "explicit_expiry", "source_deletion", "derivative_invalidation",
                "independent_support_survives",
            }
            else label
        )
        severity = (
            "high"
            if disposition == "reject_unauthorized" or effect in {"invalidate", "expire"}
            else "low" if semantic_relationship == "unrelated" and disposition == "no_op"
            else "medium"
        )
        golds.append({"pair_id": pid, "semantic_relationship": semantic_relationship, "transition_disposition": disposition,
                      "expected_state_effect": {"effect": effect, "affected_item_ids": affected,
                                                "affected_derivative_ids": (
                                                    [f"{candidate['semantic_item_ref']}-derivative"]
                                                    if effect == "invalidate" else []),
                                                "expected_new_item_ids": new_ids},
                      "expected_external_action": action, "acceptable_alternatives": [],
                      "ambiguity_reason": _rationale(label, hostile, family) if semantic_relationship == "uncertain" else None,
                      "required_evidence_ids": sorted({eid, *candidate["evidence_ids"]}),
                      "forbidden_evidence_ids": [], "severity_if_wrong": severity,
                      "adjudication_status": "pending",
                      "adjudication_notes": _special_rationale(special, label, family),
                      "feature_tags": sorted(tags)})
        checkpoint = _checkpoint(hid, sequence, events, state, invalidated_derivatives)
        checkpoints.append(checkpoint)
        if action != "none":
            tid = f"{pid}-action"
            tasks.append({"task_id": tid, "pair_id": pid, "checkpoint_id": checkpoint["checkpoint_id"],
                          "task_type": "action_selection", "request": {"question": "What external action, if any, is warranted by this observation?"},
                          "target_scope": {"mode": "pair", "pair_id": pid}, "maximum_context_budget": None,
                          "scale_family_id": None, "irrelevant_history_target": None})
            task_gold.append({"task_id": tid, "gold_response": {"action": action},
                              "relevant_dependency_ids": golds[-1]["required_evidence_ids"],
                              "counterevidence_ids": list(candidate["counterevidence_ids"]), "primary_metric": "action_accuracy"})
        tid = f"{pid}-state"
        queried = [item for item in state if item["semantic_item_ref"] in {candidate["semantic_item_ref"], *new_ids}]
        deletion_derivatives = (
            [f"{candidate['semantic_item_ref']}-derivative"] if effect == "invalidate" else []
        )
        tasks.append({"task_id": tid, "pair_id": pid, "checkpoint_id": checkpoint["checkpoint_id"],
                      "task_type": "deletion_query" if effect == "invalidate" else "current_state_query", "request": {"question": "What is the recorded state for the requested configuration items at this checkpoint?"},
                      "target_scope": {"mode": "semantic_items", "semantic_item_refs": [item["semantic_item_ref"] for item in queried],
                                       **({"derivative_ids": deletion_derivatives} if deletion_derivatives else {})},
                      "maximum_context_budget": None, "scale_family_id": None, "irrelevant_history_target": None})
        task_gold.append({"task_id": tid, "gold_response": {"current_state": [
            {key: deepcopy(item[key]) for key in ("semantic_item_ref", "proposition", "scope", "evidence_ids", "status")}
            for item in queried], **({"invalidated_derivatives": [
                                         deepcopy(item) for item in invalidated_derivatives
                                         if item["derivative_id"] in deletion_derivatives
                                     ]}
                                     if effect == "invalidate" else {})}, "relevant_dependency_ids": sorted({eid for item in queried for eid in item["evidence_ids"]}),
            "counterevidence_ids": sorted({eid for item in queried for eid in item["counterevidence_ids"]}),
            "primary_metric": "current_state_exact_match"})
    return {"history_id": hid, "difficulty_tags": plan["difficulty_tags"],
            "feature_tags": sorted({tag for gold in golds for tag in gold["feature_tags"]}),
            "timeline": events, "candidate_snapshots": snapshots, "candidate_pools": pools, "pair_inputs": inputs,
            "checkpoint_requests": [{"checkpoint_id": cp["checkpoint_id"], "after_sequence": seq}
                                    for seq, cp in zip(
                                        range(baseline_sequence, baseline_sequence + 5), checkpoints
                                    )],
            "downstream_tasks": tasks,
            "evaluator_only": {"pair_gold": golds, "checkpoint_gold": checkpoints,
                               "downstream_task_gold": task_gold, "deleted_source_content": deleted_source_content,
                               "expected_favors": plan["expected_favors"][0],
                               "expected_favors_rationale": "Predeclared authoring-stratum expectation for later baseline comparison; it is not a model result.",
                               "generation_and_review_provenance": {"generator": "original-initial-authoring-v1",
                                   "human_review": "Pending independent review; generated draft only.",
                                   "canary": f"EVALUATOR_ONLY_{hid}", "reviewed_content_sha256": None}}}


def build_initial_blueprints() -> list[dict[str, Any]]:
    return build_blueprints(limit=6)


def build_blueprints(*, limit: int | None = None) -> list[dict[str, Any]]:
    """Render the matrix-bound draft registry; records remain pending review."""
    blueprints = []
    validator = _schema_validator(BLUEPRINT_SCHEMA)
    matrix = strict_json_loads(MATRIX_PATH.read_text(encoding="utf-8"))
    family_count = len(matrix["families"]) if limit is None else limit
    for family in range(1, family_count + 1):
        plan = matrix["families"][family - 1]
        label_groups = _labels_by_history(plan)
        histories = [
            build_initial_history(family, variant, label_groups[variant], plan)
            for variant in range(3)
        ]
        blueprint = {"blueprint_version": "1",
                     "family_id": f"g4-family-{family:03d}-{'api-versioning' if family <= 3 else 'build-toolchain'}-{('direct', 'operational', 'temporal')[(family - 1) % 3]}",
                     "generation_origin": "generated_then_reviewed", "primary_relationship": plan["primary_relationship"],
                     "feature_tags": sorted({tag for history in histories for tag in history["feature_tags"]}),
                     "difficulty_tags": plan["difficulty_tags"], "expected_favors": plan["expected_favors"],
                     "deletion_presence": plan["deletion_presence"],
                     "ambiguity_presence": plan["ambiguity_presence"], "histories": histories}
        blueprint = remap_blueprint_identifiers(blueprint, salt="initial-mixed-authoring-v2")
        blueprint["family_id"] = plan["family_id"]
        actual_mix = Counter(gold["semantic_relationship"] for history in blueprint["histories"]
                             for gold in history["evaluator_only"]["pair_gold"])
        if actual_mix != plan["planned_relationship_pair_counts"]:
            raise ValueError("rendered relationship mix differs from bound authoring plan")
        validator.validate(blueprint)
        for history in render_blueprint(blueprint)[0]:
            validate_history(history, schema_validator=_frozen_schema_validator(),
                             expected_corpus_stage="frozen_g4", allowed_partitions={"development"})
        blueprints.append(blueprint)
    validate_blueprints_against_authoring_matrix(
        blueprints, matrix, require_complete=limit is None
    )
    return blueprints


def remap_blueprint_identifiers(blueprint: dict[str, Any], *, salt: str) -> dict[str, Any]:
    """Return an opaque-ID development copy, preserving every reference and hash.

    This removes the prototype's semantic/ordinal identifier hints. It is not a
    final split or secrecy guarantee: callers must keep any ID mapping and salt
    out of system-visible inputs, and final authoring needs its own review.
    """
    if not salt:
        raise ValueError("an explicit nonempty remapping salt is required")
    prefixes = tuple(history["history_id"] for history in blueprint["histories"])
    family_id = blueprint["family_id"]

    def replace(value: Any) -> Any:
        if isinstance(value, str) and (value == family_id or value.startswith((*prefixes, "opaque-"))):
            return "opaque-" + sha256_value({"salt": salt, "original_id": value})[:24]
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        return value

    remapped = replace(blueprint)
    for history in remapped["histories"]:
        for pool in history["candidate_pools"]:
            pool["sha256"] = sha256_value({"captured_after_sequence": pool["captured_after_sequence"],
                                           "snapshot_ids": pool["snapshot_ids"]})
    _schema_validator(BLUEPRINT_SCHEMA).validate(remapped)
    for history in render_blueprint(remapped)[0]:
        validate_history(history, schema_validator=_frozen_schema_validator(),
                         expected_corpus_stage="frozen_g4", allowed_partitions={"development"})
    return remapped

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from lifetime_ai.evaluation.canonical import canonical_bytes, sha256_value


RELATIONSHIPS = [
    "supports", "contradicts", "narrows_scope",
    "supersedes", "unrelated", "uncertain",
]
RELATIONSHIP_PLAN = {
    "supports": ("accept", "reinforce", "none", "preference_reinforcement"),
    "contradicts": ("abstain", "preserve_conflict", "clarify", "contradiction_without_repair"),
    "narrows_scope": ("accept", "add_scoped_item", "none", "scope_narrowing"),
    "supersedes": ("accept", "close_and_replace", "none", "temporal_supersession"),
    "unrelated": ("no_op", "none", "silence", "irrelevant_noise"),
    "uncertain": ("abstain", "none", "clarify", "genuine_ambiguity"),
}
FEATURES = [
    "preference_reinforcement", "direct_correction", "scope_narrowing",
    "temporal_supersession", "explicit_expiry", "commitment_resolution",
    "commitment_failure", "contradiction_without_repair", "genuine_ambiguity",
    "irrelevant_noise", "source_deletion", "derivative_invalidation",
    "independent_support_survives", "unauthorized_injection_text",
    "silence_is_correct", "late_or_retroactive_report", "sensitive_state",
]
SECONDARY_FEATURES_BY_RELATIONSHIP = {
    "supports": ["commitment_resolution", "sensitive_state", "preference_reinforcement"],
    "contradicts": ["unauthorized_injection_text", "contradiction_without_repair"],
    "narrows_scope": ["sensitive_state", "scope_narrowing"],
    "supersedes": [
        "explicit_expiry", "direct_correction", "source_deletion",
        "derivative_invalidation",
    ],
    "unrelated": ["silence_is_correct", "commitment_failure", "irrelevant_noise"],
    "uncertain": ["late_or_retroactive_report", "genuine_ambiguity", "sensitive_state"],
}
DOMAINS = [
    ("api-versioning", "supported API version for a mobile client"),
    ("build-toolchain", "compiler and package-manager selection"),
    ("code-ownership", "review ownership for a service directory"),
    ("component-registry", "approved SDUI component registration"),
    ("data-retention", "retention interval for diagnostic records"),
    ("database-migration", "migration readiness for a schema change"),
    ("deployment-window", "permitted production deployment window"),
    ("design-token", "canonical spacing and typography token"),
    ("feature-flag", "rollout state and audience for a feature flag"),
    ("incident-mitigation", "current mitigation for an active incident"),
    ("localization", "fallback locale for untranslated interface text"),
    ("logging-policy", "sensitive-field logging policy"),
    ("mobile-navigation", "navigation pattern for a mobile workflow"),
    ("network-timeout", "timeout policy for an upstream dependency"),
    ("observability", "required service-level telemetry"),
    ("on-call-handoff", "temporary ownership during an on-call handoff"),
    ("payment-retry", "retry policy for failed payment operations"),
    ("privacy-consent", "consent requirement for analytics collection"),
    ("queue-consumer", "concurrency limit for a background consumer"),
    ("release-branch", "branch used for an upcoming release"),
    ("rollback-procedure", "approved rollback procedure"),
    ("schema-generation", "source of truth for generated client schemas"),
    ("search-index", "index refresh and consistency expectations"),
    ("security-review", "security approval status for a dependency"),
    ("service-endpoint", "canonical endpoint for an internal service"),
    ("session-lifetime", "authentication session lifetime"),
    ("storage-encryption", "encryption requirement for cached data"),
    ("support-escalation", "escalation route for customer-impacting issues"),
    ("test-fixtures", "authoritative fixture source for integration tests"),
    ("third-party-sdk", "approved version of an external SDK"),
    ("ui-accessibility", "accessibility behavior for a form control"),
    ("webhook-delivery", "delivery and retry contract for webhooks"),
    ("worker-scheduling", "schedule for a recurring maintenance worker"),
    ("cache-invalidation", "cache invalidation trigger and scope"),
    ("configuration-precedence", "precedence between configuration sources"),
    ("dependency-deprecation", "replacement path for a deprecated library"),
    ("error-taxonomy", "canonical classification for client-visible errors"),
    ("form-validation", "validation rule for a conditional form field"),
    ("message-ordering", "ordering guarantee for domain events"),
    ("rate-limiting", "rate limit and exception policy"),
    ("repository-layout", "location for a new domain module"),
    ("runtime-permission", "permission needed for a privileged operation"),
    ("secrets-rotation", "rotation deadline for a service credential"),
    ("state-reconciliation", "precedence during offline state reconciliation"),
    ("telemetry-sampling", "sampling rate for high-volume telemetry"),
]
VARIANTS = [
    ("direct", "an explicit statement from the authoritative actor"),
    ("operational", "a tool observation with realistic surrounding noise"),
    ("temporal", "a late, expiring, deleted, or period-bounded observation"),
]


def build_authoring_matrix() -> dict[str, Any]:
    families: list[dict[str, Any]] = []
    for domain_index, (domain, subject) in enumerate(DOMAINS):
        for variant_index, (variant, framing) in enumerate(VARIANTS):
            ordinal = domain_index * len(VARIANTS) + variant_index
            relationship = RELATIONSHIPS[ordinal % len(RELATIONSHIPS)]
            disposition, effect, action, relationship_feature = RELATIONSHIP_PLAN[relationship]
            calibration_features = {
                "supports": [],
                "contradicts": ["contradiction_without_repair"],
                "narrows_scope": ["scope_narrowing"],
                "supersedes": ["temporal_supersession"],
                "unrelated": ["irrelevant_noise"],
                "uncertain": ["genuine_ambiguity"],
            }
            relationship_occurrence = ordinal // len(RELATIONSHIPS)
            compatible_features = SECONDARY_FEATURES_BY_RELATIONSHIP[relationship]
            secondary_feature = compatible_features[
                relationship_occurrence % len(compatible_features)
            ]
            features = (
                calibration_features[relationship]
                if ordinal < 6
                else sorted({relationship_feature, secondary_feature})
            )
            if ordinal >= 6 and secondary_feature == "source_deletion":
                features = sorted({*features, "independent_support_survives"})
            if ordinal >= 6 and secondary_feature in {
                "source_deletion", "derivative_invalidation",
                "independent_support_survives",
            }:
                effect = "invalidate"
                disposition = "accept"
            elif ordinal >= 6 and secondary_feature == "explicit_expiry":
                effect = "expire"
                disposition = "accept"
            elif ordinal >= 6 and secondary_feature == "commitment_resolution":
                effect = "resolve"
                disposition = "accept"
            elif ordinal >= 6 and secondary_feature == "commitment_failure":
                effect = "none"
                disposition = "reject_invalid"
                action = "investigate"
            elif ordinal >= 6 and secondary_feature == "unauthorized_injection_text":
                disposition = "reject_unauthorized"
                effect = "none"
                action = "silence"
            elif ordinal >= 6 and secondary_feature == "direct_correction" and relationship == "supports":
                disposition = "reject_invalid"
                effect = "none"
                action = "investigate"
            if (ordinal >= 6 and relationship == "supports"
                    and secondary_feature == "preference_reinforcement"):
                action = "outreach_candidate"
            secondary_relationships = [
                label for label in RELATIONSHIPS if label != relationship
            ]
            relationship_pair_counts = {relationship: 4}
            for offset, label in enumerate(secondary_relationships):
                relationship_pair_counts[label] = 2 if offset < 3 else 1
            opaque_id = sha256_value({
                "namespace": "lifetime-ai-frozen-g4-family-v1",
                "domain": domain,
                "variant": variant,
            })[:16]
            all_default_targets = [RELATIONSHIP_PLAN[label] for label in RELATIONSHIPS]
            difficulty_tags = ["routine" if variant_index == 0 else "contextual"]
            if ordinal % 9 == 0:
                difficulty_tags.append("difficult")
            families.append({
                "family_id": f"g4-family-{opaque_id}",
                "domain": domain,
                "scenario_focus": f"{subject}; {framing}",
                "primary_relationship": relationship,
                "planned_relationship_pair_counts": dict(sorted(relationship_pair_counts.items())),
                "required_features": features,
                "planned_dispositions": sorted({
                    disposition, *(target[0] for target in all_default_targets)
                }),
                "planned_effects": sorted({
                    effect, *(target[1] for target in all_default_targets)
                }),
                "planned_actions": sorted({
                    action, *(target[2] for target in all_default_targets)
                }),
                "expected_favors": ["neutral"] if ordinal < 6 else [
                    ["architecture", "baseline_a", "baseline_b", "baseline_c", "neutral"][
                        ordinal % 5
                    ]
                ],
                "deletion_presence": bool({
                    "source_deletion", "derivative_invalidation",
                    "independent_support_survives",
                } & set(features)),
                "ambiguity_presence": True,
                "difficulty_tags": sorted(difficulty_tags),
                "authoring_status": "planned",
            })
    summary = {
        "families": len(families),
        "relationship_families": dict(sorted(Counter(
            item["primary_relationship"] for item in families
        ).items())),
        "feature_families": dict(sorted(Counter(
            feature for item in families for feature in item["required_features"]
        ).items())),
    }
    matrix = {
        "matrix_version": "1",
        "dataset_version": "frozen-g4-v0.1",
        "status": "AUTHORING_PLAN_NOT_CORPUS",
        "families": families,
        "summary": summary,
    }
    matrix["matrix_sha256"] = sha256_value(matrix)
    return matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the frozen-G4 authoring matrix")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite authoring matrix: {args.output}")
    matrix = build_authoring_matrix()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_bytes(matrix) + b"\n")
    print(f"wrote {len(matrix['families'])} planned families to {args.output}")


if __name__ == "__main__":
    main()

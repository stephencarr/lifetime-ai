# G3 development-pilot review packet

Status: **awaiting human review** — 30 histories and 120 pairs generated for development-pilot review. G3 is not complete.

`none` means no action-selection task exists for the case. `silence` means an action-selection task exists and deliberate non-action is the expected answer.

## full-01 — surface-family-01

- Record: [`../holdout.jsonl` line 1](../holdout.jsonl#L1)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-01-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The checkout primary action runtime behavior uses legacy_checkout.'
- `full-01-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only checkout primary action runtime behavior variant uses checkout.submit within mobile checkout.'
- `full-01-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change checkout primary action schema contract to checkout.submit.'
- `full-01-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only checkout primary action schema contract variant uses checkout.submit within mobile checkout.'
- `full-01-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Provider H01 may satisfy the needs of checkout primary action authoring guidance.'
- `full-01-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The user has an active approved goal to prepare an outreach candidate for checkout primary action authoring guidance when every declared requirement is met.'
- `full-01-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use legacy_checkout for checkout primary action migration plan across ordinary cases.'
- `full-01-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only checkout primary action migration plan variant uses checkout.submit within mobile checkout.'
- `full-01-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The review notes mention a change to the meeting room booking for Friday.'
- `full-01-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'For checkout primary action schema contract, the registry audit gives checkout.submit as the value.'
- `full-01-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The release checklist records legacy_checkout for checkout primary action authoring guidance.'
- `full-01-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'checkout-primary-action-migration-plan', 'audience': 'mobile-checkout'}}`; content: 'The listed checkout primary action migration plan value is checkout.submit, according to the architecture note.'

### Pair `full-01-p1-pair`

- Evaluated event: `full-01-p1-event`; context events: `full-01-p1-source`
- Candidate pool: `full-01-p1-pool`; hash: `9c627951e661780824966ecffc2534a62ec81894d5836e52df551ca114557aec`; snapshots: `full-01-p1-snapshot-target, full-01-p1-snapshot-aux`
- Candidate snapshot: `full-01-p1-snapshot-target`; runtime item: `full-01-p1-runtime-target`; hash: `896248a220000dfb99e538e81e8632aecdde05bc524df3c3f55c55aaf4d75b64`
- Candidate source IDs: `full-01-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The checkout primary action runtime behavior uses legacy_checkout.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-01-p1-source, full-01-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-01_1

#### Checkpoints and downstream tasks

- Checkpoint `full-01-p1-checkpoint` after sequence `9`
- Task `full-01-p1-state-task` (`current_state_query`) at `full-01-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The checkout primary action runtime behavior uses legacy_checkout.', 'scope': {'system': 'checkout-primary-action-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-01-p1-source']}]}`; dependencies: `full-01-p1-source, full-01-p1-event`
- Task `full-01-p1-action-task` (`action_selection`) at `full-01-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-01-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-01-p1-source, full-01-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-01-p2-pair`

- Evaluated event: `full-01-p2-event`; context events: `full-01-p2-source`
- Candidate pool: `full-01-p2-pool`; hash: `c7c0c41969854f8fd47998f9834a3ed3027423daa0e3ad528946e434e33c98d8`; snapshots: `full-01-p2-snapshot-target, full-01-p2-snapshot-aux`
- Candidate snapshot: `full-01-p2-snapshot-target`; runtime item: `full-01-p2-runtime-target`; hash: `61cbd2bc001c2cffeb68eadd7c19f21438048b705180c8d6e9dcf3dace55b210`
- Candidate source IDs: `full-01-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change checkout primary action schema contract to checkout.submit.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-01-p2-source, full-01-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-01_2

#### Checkpoints and downstream tasks

- Checkpoint `full-01-p2-checkpoint` after sequence `10`
- Task `full-01-p2-state-task` (`commitment_query`) at `full-01-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The team committed to change checkout primary action schema contract to checkout.submit.', 'scope': {'system': 'checkout-primary-action-schema-contract', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-01-p2-source', 'full-01-p2-event']}]}`; dependencies: `full-01-p2-source, full-01-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-01-p3-pair`

- Evaluated event: `full-01-p3-event`; context events: `full-01-p3-source, full-01-p3-aux`
- Candidate pool: `full-01-p3-pool`; hash: `d7dcd415cba677f7fa5439cd2da4cdd5bdcda9ac42e6788ea578be5d815e1fc3`; snapshots: `full-01-p3-snapshot-target, full-01-p3-snapshot-aux`
- Candidate snapshot: `full-01-p3-snapshot-target`; runtime item: `full-01-p3-runtime-target`; hash: `250b21db5fe73118dee6c642f11877a8d490fe79855192d291a50fbd281ae69f`
- Candidate source IDs: `full-01-p3-source`; counterevidence IDs: `none`
- Candidate proposition: Provider H01 may satisfy the needs of checkout primary action authoring guidance.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `outreach_candidate`; action-selection task present: `true`
- Required evidence IDs: `full-01-p3-source, full-01-p3-aux, full-01-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-01_3

#### Checkpoints and downstream tasks

- Checkpoint `full-01-p3-checkpoint` after sequence `11`
- Task `full-01-p3-state-task` (`current_state_query`) at `full-01-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'Provider H01 may satisfy the needs of checkout primary action authoring guidance.', 'scope': {'system': 'checkout-primary-action-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-01-p3-source', 'full-01-p3-event']}]}`; dependencies: `full-01-p3-source, full-01-p3-aux, full-01-p3-event`
- Task `full-01-p3-action-task` (`action_selection`) at `full-01-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-01-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'outreach_candidate'}`; dependencies: `full-01-p3-source, full-01-p3-aux, full-01-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-01-p4-pair`

- Evaluated event: `full-01-p4-event`; context events: `full-01-p4-source`
- Candidate pool: `full-01-p4-pool`; hash: `b06295969b71119b9ae81e869620ba11950e635b2e25af0814ba82dbf6a5b968`; snapshots: `full-01-p4-snapshot-target, full-01-p4-snapshot-aux`
- Candidate snapshot: `full-01-p4-snapshot-target`; runtime item: `full-01-p4-runtime-target`; hash: `ab72d1d2943063f79475be17baf3c2fc02dccb1fe2b6e24c0f14c32d448b5537`
- Candidate source IDs: `full-01-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use legacy_checkout for checkout primary action migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-01-p4-source, full-01-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-01_4

#### Checkpoints and downstream tasks

- Checkpoint `full-01-p4-checkpoint` after sequence `12`
- Task `full-01-p4-state-task` (`current_state_query`) at `full-01-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use legacy_checkout for checkout primary action migration plan across ordinary cases.', 'scope': {'system': 'checkout-primary-action-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-01-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'The listed checkout primary action migration plan value is checkout.submit, according to the architecture note.', 'scope': {'system': 'checkout-primary-action-migration-plan', 'audience': 'mobile-checkout'}, 'status': 'active', 'evidence_ids': ['full-01-p4-event']}]}`; dependencies: `full-01-p4-source, full-01-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-02 — surface-family-02

- Record: [`../holdout.jsonl` line 2](../holdout.jsonl#L2)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-02-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to review profile header runtime behavior before 09:00 UTC.'
- `full-02-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only profile header runtime behavior variant uses profile.hero within tablet profiles.'
- `full-02-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for profile header schema contract is legacy_header.'
- `full-02-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only profile header schema contract variant uses profile.hero within tablet profiles.'
- `full-02-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use legacy_header for profile header authoring guidance across ordinary cases.'
- `full-02-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only profile header authoring guidance variant uses profile.hero within tablet profiles.'
- `full-02-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for profile header migration plan is legacy_header.'
- `full-02-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only profile header migration plan variant uses profile.hero within tablet profiles.'
- `full-02-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `evaluator`; type `time_advance`; assert `false`; transition `true`; reason: evaluator clock event for lifecycle evaluation only; deletion targets: `none`; metadata: `{'advance_to': '2026-09-18T10:00:00Z'}`; content: None
- `full-02-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The instruction points back to an earlier example without making clear which example should govern this request.'
- `full-02-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'profile-header-authoring-guidance', 'audience': 'tablet-profiles'}}`; content: 'The listed profile header authoring guidance value is profile.hero, according to the registry audit.'
- `full-02-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'For profile header migration plan, the release checklist gives profile.hero as the value.'

### Pair `full-02-p1-pair`

- Evaluated event: `full-02-p1-event`; context events: `full-02-p1-source`
- Candidate pool: `full-02-p1-pool`; hash: `b87e2beae107db6bd2e4652d117fa2a3835db01f9f73987f116ed9dff6e288c0`; snapshots: `full-02-p1-snapshot-target, full-02-p1-snapshot-aux`
- Candidate snapshot: `full-02-p1-snapshot-target`; runtime item: `full-02-p1-runtime-target`; hash: `1e62aa7700a61dbbe3b326e7dd1e824d1e5d966cbe86b3e3f1aa14f24ad3ba22`
- Candidate source IDs: `full-02-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to review profile header runtime behavior before 09:00 UTC.
- Candidate validity: `2026-09-17T12:00:00Z` through `2026-09-18T09:00:00Z`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `expire`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-02-p1-source, full-02-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-02_1

#### Checkpoints and downstream tasks

- Checkpoint `full-02-p1-checkpoint` after sequence `9`
- Task `full-02-p1-state-task` (`commitment_query`) at `full-02-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The team committed to review profile header runtime behavior before 09:00 UTC.', 'scope': {'system': 'profile-header-runtime-behavior', 'audience': 'all'}, 'status': 'expired', 'evidence_ids': ['full-02-p1-source']}]}`; dependencies: `full-02-p1-source, full-02-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-02-p2-pair`

- Evaluated event: `full-02-p2-event`; context events: `full-02-p2-source`
- Candidate pool: `full-02-p2-pool`; hash: `9664ad76e00f08dcd2206bdb18c29094ee48e24cde7e4b7d90ba50e4e2e70aaf`; snapshots: `full-02-p2-snapshot-target, full-02-p2-snapshot-aux`
- Candidate snapshot: `full-02-p2-snapshot-target`; runtime item: `full-02-p2-runtime-target`; hash: `c7fd51b9acbd9fe1fbbc673b6f3f255687ba9e378fbd2a1e78e17fe947104b5a`
- Candidate source IDs: `full-02-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for profile header schema contract is legacy_header.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-02-p2-source, full-02-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-02_2

#### Checkpoints and downstream tasks

- Checkpoint `full-02-p2-checkpoint` after sequence `10`
- Task `full-02-p2-state-task` (`current_state_query`) at `full-02-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for profile header schema contract is legacy_header.', 'scope': {'system': 'profile-header-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-02-p2-source']}]}`; dependencies: `full-02-p2-source, full-02-p2-event`
- Task `full-02-p2-action-task` (`action_selection`) at `full-02-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-02-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-02-p2-source, full-02-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-02-p3-pair`

- Evaluated event: `full-02-p3-event`; context events: `full-02-p3-source`
- Candidate pool: `full-02-p3-pool`; hash: `de288cffa04c7b2a160b4374305dbe0c29b8106fbc47750e9efd708ac5d8fe07`; snapshots: `full-02-p3-snapshot-target, full-02-p3-snapshot-aux`
- Candidate snapshot: `full-02-p3-snapshot-target`; runtime item: `full-02-p3-runtime-target`; hash: `91ad1e37914d8ddf77816a5abfe9940464fadf6bfa0f2f005b840c0105b3bdbd`
- Candidate source IDs: `full-02-p3-source`; counterevidence IDs: `none`
- Candidate proposition: Use legacy_header for profile header authoring guidance across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p3:target`; new: `semantic:p3:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-02-p3-source, full-02-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-02_3

#### Checkpoints and downstream tasks

- Checkpoint `full-02-p3-checkpoint` after sequence `11`
- Task `full-02-p3-state-task` (`current_state_query`) at `full-02-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'Use legacy_header for profile header authoring guidance across ordinary cases.', 'scope': {'system': 'profile-header-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-02-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:scoped', 'proposition': 'The listed profile header authoring guidance value is profile.hero, according to the registry audit.', 'scope': {'system': 'profile-header-authoring-guidance', 'audience': 'tablet-profiles'}, 'status': 'active', 'evidence_ids': ['full-02-p3-event']}]}`; dependencies: `full-02-p3-source, full-02-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-02-p4-pair`

- Evaluated event: `full-02-p4-event`; context events: `full-02-p4-source`
- Candidate pool: `full-02-p4-pool`; hash: `4296e636bc1a2d6c06a68a107d29ac68d3f6697969a6947ef876f800521b6037`; snapshots: `full-02-p4-snapshot-target, full-02-p4-snapshot-aux`
- Candidate snapshot: `full-02-p4-snapshot-target`; runtime item: `full-02-p4-runtime-target`; hash: `7a13b2638be474c70c29486605c71f4c50fb4dee6881a9e6550a6684a96c771c`
- Candidate source IDs: `full-02-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for profile header migration plan is legacy_header.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p4:target`; new: `semantic:p4:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-02-p4-source, full-02-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-02_4

#### Checkpoints and downstream tasks

- Checkpoint `full-02-p4-checkpoint` after sequence `12`
- Task `full-02-p4-state-task` (`current_state_query`) at `full-02-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The current value for profile header migration plan is legacy_header.', 'scope': {'system': 'profile-header-migration-plan', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-02-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:replacement', 'proposition': 'For profile header migration plan, the release checklist gives profile.hero as the value.', 'scope': {'system': 'profile-header-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-02-p4-event']}]}`; dependencies: `full-02-p4-source, full-02-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-03 — surface-family-03

- Record: [`../development.jsonl` line 1](../development.jsonl#L1)
- Partition: `pilot_development`
### Timeline and authority

- `full-03-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for notification adapter runtime behavior is push_v1.'
- `full-03-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only notification adapter runtime behavior variant uses push.dispatch within quiet hours.'
- `full-03-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use push_v1 for notification adapter schema contract across ordinary cases.'
- `full-03-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only notification adapter schema contract variant uses push.dispatch within quiet hours.'
- `full-03-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for notification adapter authoring guidance is push_v1.'
- `full-03-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only notification adapter authoring guidance variant uses push.dispatch within quiet hours.'
- `full-03-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The notification adapter migration plan uses push_v1.'
- `full-03-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only notification adapter migration plan variant uses push.dispatch within quiet hours.'
- `full-03-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The listed notification adapter runtime behavior value is push_v1, according to the maintainer journal.'
- `full-03-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'notification-adapter-schema-contract', 'audience': 'quiet-hours'}}`; content: 'The schema inspection records push.dispatch for notification adapter schema contract.'
- `full-03-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'For notification adapter authoring guidance, the test report gives push.dispatch as the value.'
- `full-03-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-03-p4-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'

### Pair `full-03-p1-pair`

- Evaluated event: `full-03-p1-event`; context events: `full-03-p1-source`
- Candidate pool: `full-03-p1-pool`; hash: `9915e5c6db142faf08eeb553e7ca7f365895e655ad17bc0911652f843a86e680`; snapshots: `full-03-p1-snapshot-target, full-03-p1-snapshot-aux`
- Candidate snapshot: `full-03-p1-snapshot-target`; runtime item: `full-03-p1-runtime-target`; hash: `a8302594a4bf9851d004c28397c6419605ec0f6a05d0aad35343d10d527f545a`
- Candidate source IDs: `full-03-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for notification adapter runtime behavior is push_v1.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-03-p1-source, full-03-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-03_1

#### Checkpoints and downstream tasks

- Checkpoint `full-03-p1-checkpoint` after sequence `9`
- Task `full-03-p1-state-task` (`current_state_query`) at `full-03-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for notification adapter runtime behavior is push_v1.', 'scope': {'system': 'notification-adapter-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-03-p1-source', 'full-03-p1-event']}]}`; dependencies: `full-03-p1-source, full-03-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-03-p2-pair`

- Evaluated event: `full-03-p2-event`; context events: `full-03-p2-source`
- Candidate pool: `full-03-p2-pool`; hash: `279ddab422d76f91714b23d375929e6f96e8c740d6a54f535aabf1b60ec8fbfa`; snapshots: `full-03-p2-snapshot-target, full-03-p2-snapshot-aux`
- Candidate snapshot: `full-03-p2-snapshot-target`; runtime item: `full-03-p2-runtime-target`; hash: `74e24c8a734a7081a2d95b7ddb64c6278b18f261299bbe7466a1055705d66ba9`
- Candidate source IDs: `full-03-p2-source`; counterevidence IDs: `none`
- Candidate proposition: Use push_v1 for notification adapter schema contract across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p2:target`; new: `semantic:p2:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-03-p2-source, full-03-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-03_2

#### Checkpoints and downstream tasks

- Checkpoint `full-03-p2-checkpoint` after sequence `10`
- Task `full-03-p2-state-task` (`current_state_query`) at `full-03-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'Use push_v1 for notification adapter schema contract across ordinary cases.', 'scope': {'system': 'notification-adapter-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-03-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:scoped', 'proposition': 'The schema inspection records push.dispatch for notification adapter schema contract.', 'scope': {'system': 'notification-adapter-schema-contract', 'audience': 'quiet-hours'}, 'status': 'active', 'evidence_ids': ['full-03-p2-event']}]}`; dependencies: `full-03-p2-source, full-03-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-03-p3-pair`

- Evaluated event: `full-03-p3-event`; context events: `full-03-p3-source`
- Candidate pool: `full-03-p3-pool`; hash: `e77f1bff5fb0cd67739c156a4ad6240f4ebc358ca3fdd3a879e56a55ecdff6c0`; snapshots: `full-03-p3-snapshot-target, full-03-p3-snapshot-aux`
- Candidate snapshot: `full-03-p3-snapshot-target`; runtime item: `full-03-p3-runtime-target`; hash: `9314c36d8bfefe54e2703f7c34ee4bf0b01fbfba1925ec59dc0b0bb2bb51fb17`
- Candidate source IDs: `full-03-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for notification adapter authoring guidance is push_v1.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-03-p3-source, full-03-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-03_3

#### Checkpoints and downstream tasks

- Checkpoint `full-03-p3-checkpoint` after sequence `11`
- Task `full-03-p3-state-task` (`current_state_query`) at `full-03-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for notification adapter authoring guidance is push_v1.', 'scope': {'system': 'notification-adapter-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-03-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'For notification adapter authoring guidance, the test report gives push.dispatch as the value.', 'scope': {'system': 'notification-adapter-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-03-p3-event']}]}`; dependencies: `full-03-p3-source, full-03-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-03-p4-pair`

- Evaluated event: `full-03-p4-event`; context events: `full-03-p4-source`
- Candidate pool: `full-03-p4-pool`; hash: `fd0935ccb5fe07a6a59420def4da68ad0d4fb9db1bc2cd40f2c142bb0b5ac7f2`; snapshots: `full-03-p4-snapshot-target, full-03-p4-snapshot-aux`
- Candidate snapshot: `full-03-p4-snapshot-target`; runtime item: `full-03-p4-runtime-target`; hash: `6e0c983b5287bc7a2c35f06dda725055138a8efbeac8c332444d4363881e3c50`
- Candidate source IDs: `full-03-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The notification adapter migration plan uses push_v1.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `invalidate`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-03-p4-source, full-03-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-03_4

#### Checkpoints and downstream tasks

- Checkpoint `full-03-p4-checkpoint` after sequence `12`
- Task `full-03-p4-state-task` (`deletion_query`) at `full-03-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The notification adapter migration plan uses push_v1.', 'scope': {'system': 'notification-adapter-migration-plan', 'audience': 'all'}, 'status': 'invalidated', 'evidence_ids': []}], 'invalidated_derivatives': [{'semantic_item_ref': 'semantic:p4:target', 'invalidated_by_event_id': 'full-03-p4-event', 'reason': 'sole_source_deleted'}]}`; dependencies: `full-03-p4-source, full-03-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-04 — surface-family-04

- Record: [`../development.jsonl` line 2](../development.jsonl#L2)
- Partition: `pilot_development`
### Timeline and authority

- `full-04-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for search result card runtime behavior is compact_card.'
- `full-04-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only search result card runtime behavior variant uses result.summary within accessibility mode.'
- `full-04-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The search result card schema contract uses compact_card.'
- `full-04-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The search result card schema contract uses compact_card.'
- `full-04-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for search result card authoring guidance is compact_card.'
- `full-04-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only search result card authoring guidance variant uses result.summary within accessibility mode.'
- `full-04-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The search result card migration plan uses compact_card.'
- `full-04-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only search result card migration plan variant uses result.summary within accessibility mode.'
- `full-04-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'That choice belongs to the case the previous entry described, though the entry itself is not identified here.'
- `full-04-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-04-p2-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-04-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'The listed search result card authoring guidance value is result.summary, according to the schema inspection.'
- `full-04-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The review notes mention a change to the meeting room booking for Friday.'

### Pair `full-04-p1-pair`

- Evaluated event: `full-04-p1-event`; context events: `full-04-p1-source`
- Candidate pool: `full-04-p1-pool`; hash: `8253e9466f247dfeed8b1d6f41abce5e3fcaeaa40f19ff71e681c383baa9bd09`; snapshots: `full-04-p1-snapshot-target, full-04-p1-snapshot-aux`
- Candidate snapshot: `full-04-p1-snapshot-target`; runtime item: `full-04-p1-runtime-target`; hash: `227a8de8619207d652964afa7b0960029f3142cca935ae176e104ce5616a3cdd`
- Candidate source IDs: `full-04-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for search result card runtime behavior is compact_card.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-04-p1-source, full-04-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-04_1

#### Checkpoints and downstream tasks

- Checkpoint `full-04-p1-checkpoint` after sequence `9`
- Task `full-04-p1-state-task` (`current_state_query`) at `full-04-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for search result card runtime behavior is compact_card.', 'scope': {'system': 'search-result-card-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-04-p1-source']}]}`; dependencies: `full-04-p1-source, full-04-p1-event`
- Task `full-04-p1-action-task` (`action_selection`) at `full-04-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-04-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-04-p1-source, full-04-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-04-p2-pair`

- Evaluated event: `full-04-p2-event`; context events: `full-04-p2-source, full-04-p2-aux`
- Candidate pool: `full-04-p2-pool`; hash: `615e151cab081dea6f6fae6aab8da3775d89787441ee0b5b93e2c340164dfcbc`; snapshots: `full-04-p2-snapshot-target, full-04-p2-snapshot-aux`
- Candidate snapshot: `full-04-p2-snapshot-target`; runtime item: `full-04-p2-runtime-target`; hash: `6ae0873ecb900596c29fdb547ea4eff4cbb175187bd217c4ec3f2499013c41f9`
- Candidate source IDs: `full-04-p2-source, full-04-p2-aux`; counterevidence IDs: `none`
- Candidate proposition: The search result card schema contract uses compact_card.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-04-p2-source, full-04-p2-aux, full-04-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-04_2

#### Checkpoints and downstream tasks

- Checkpoint `full-04-p2-checkpoint` after sequence `10`
- Task `full-04-p2-state-task` (`deletion_query`) at `full-04-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The search result card schema contract uses compact_card.', 'scope': {'system': 'search-result-card-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-04-p2-aux']}], 'invalidated_derivatives': []}`; dependencies: `full-04-p2-source, full-04-p2-aux, full-04-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-04-p3-pair`

- Evaluated event: `full-04-p3-event`; context events: `full-04-p3-source`
- Candidate pool: `full-04-p3-pool`; hash: `4446491117fa95908b875a712881ebd52eab8bc7b60a4433161027ce3cf58318`; snapshots: `full-04-p3-snapshot-target, full-04-p3-snapshot-aux`
- Candidate snapshot: `full-04-p3-snapshot-target`; runtime item: `full-04-p3-runtime-target`; hash: `57b680c5c271da080604ec581bbaee01971711f7594b79e7e06bc7d791ac793f`
- Candidate source IDs: `full-04-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for search result card authoring guidance is compact_card.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-04-p3-source, full-04-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-04_3

#### Checkpoints and downstream tasks

- Checkpoint `full-04-p3-checkpoint` after sequence `11`
- Task `full-04-p3-state-task` (`current_state_query`) at `full-04-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for search result card authoring guidance is compact_card.', 'scope': {'system': 'search-result-card-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-04-p3-source']}]}`; dependencies: `full-04-p3-source, full-04-p3-event`
- Task `full-04-p3-action-task` (`action_selection`) at `full-04-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-04-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-04-p3-source, full-04-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-04-p4-pair`

- Evaluated event: `full-04-p4-event`; context events: `full-04-p4-source`
- Candidate pool: `full-04-p4-pool`; hash: `3648eb644b51e197f1c811c3a437db5703fa20aeec5b294e3cbddda88e7b66e7`; snapshots: `full-04-p4-snapshot-target, full-04-p4-snapshot-aux`
- Candidate snapshot: `full-04-p4-snapshot-target`; runtime item: `full-04-p4-runtime-target`; hash: `6c6e26c3562c8176ee8e6176e495a4a44b9a1ae05706b624c88cb36d91a166f1`
- Candidate source IDs: `full-04-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The search result card migration plan uses compact_card.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-04-p4-source, full-04-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-04_4

#### Checkpoints and downstream tasks

- Checkpoint `full-04-p4-checkpoint` after sequence `12`
- Task `full-04-p4-state-task` (`current_state_query`) at `full-04-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The search result card migration plan uses compact_card.', 'scope': {'system': 'search-result-card-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-04-p4-source']}]}`; dependencies: `full-04-p4-source, full-04-p4-event`
- Task `full-04-p4-action-task` (`action_selection`) at `full-04-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-04-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-04-p4-source, full-04-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-05 — surface-family-05

- Record: [`../development.jsonl` line 3](../development.jsonl#L3)
- Partition: `pilot_development`
### Timeline and authority

- `full-05-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for payment retry policy runtime behavior is three retries.'
- `full-05-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only payment retry policy runtime behavior variant uses two retries within high-risk payments.'
- `full-05-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to review payment retry policy schema contract before 09:00 UTC.'
- `full-05-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only payment retry policy schema contract variant uses two retries within high-risk payments.'
- `full-05-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for payment retry policy authoring guidance is three retries.'
- `full-05-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only payment retry policy authoring guidance variant uses two retries within high-risk payments.'
- `full-05-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use three retries for payment retry policy migration plan across ordinary cases.'
- `full-05-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only payment retry policy migration plan variant uses two retries within high-risk payments.'
- `full-05-p1-event` — seq 9; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'Late report, effective 2026-09-16: The incident follow-up records three retries for payment retry policy runtime behavior.'
- `full-05-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `evaluator`; type `time_advance`; assert `false`; transition `true`; reason: evaluator clock event for lifecycle evaluation only; deletion targets: `none`; metadata: `{'advance_to': '2026-09-18T10:00:00Z'}`; content: None
- `full-05-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-05-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'payment-retry-policy-migration-plan', 'audience': 'high-risk-payments'}}`; content: 'For payment retry policy migration plan, the schema inspection gives two retries as the value.'

### Pair `full-05-p1-pair`

- Evaluated event: `full-05-p1-event`; context events: `full-05-p1-source`
- Candidate pool: `full-05-p1-pool`; hash: `149bb749ccb692ef16d3d03d61c7011d587e59d01bcf92a75634200514c53340`; snapshots: `full-05-p1-snapshot-target, full-05-p1-snapshot-aux`
- Candidate snapshot: `full-05-p1-snapshot-target`; runtime item: `full-05-p1-runtime-target`; hash: `92d3125f88f216325bdf0dcb45446499374ac5fcc9955d6dfbda4585df71fc99`
- Candidate source IDs: `full-05-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for payment retry policy runtime behavior is three retries.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-05-p1-source, full-05-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-05_1

#### Checkpoints and downstream tasks

- Checkpoint `full-05-p1-checkpoint` after sequence `9`
- Task `full-05-p1-state-task` (`current_state_query`) at `full-05-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for payment retry policy runtime behavior is three retries.', 'scope': {'system': 'payment-retry-policy-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-05-p1-source', 'full-05-p1-event']}]}`; dependencies: `full-05-p1-source, full-05-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-05-p2-pair`

- Evaluated event: `full-05-p2-event`; context events: `full-05-p2-source`
- Candidate pool: `full-05-p2-pool`; hash: `3779b9fcce89a946f82e2a9a369a784a412443039f58339154bc3532ef8a229e`; snapshots: `full-05-p2-snapshot-target, full-05-p2-snapshot-aux`
- Candidate snapshot: `full-05-p2-snapshot-target`; runtime item: `full-05-p2-runtime-target`; hash: `19543cbac38c97c04df39ead080115aa90a69e3e4e1ccedcb44ee18be06f335e`
- Candidate source IDs: `full-05-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to review payment retry policy schema contract before 09:00 UTC.
- Candidate validity: `2026-09-17T12:00:00Z` through `2026-09-18T09:00:00Z`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `expire`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-05-p2-source, full-05-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-05_2

#### Checkpoints and downstream tasks

- Checkpoint `full-05-p2-checkpoint` after sequence `10`
- Task `full-05-p2-state-task` (`commitment_query`) at `full-05-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The team committed to review payment retry policy schema contract before 09:00 UTC.', 'scope': {'system': 'payment-retry-policy-schema-contract', 'audience': 'all'}, 'status': 'expired', 'evidence_ids': ['full-05-p2-source']}]}`; dependencies: `full-05-p2-source, full-05-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-05-p3-pair`

- Evaluated event: `full-05-p3-event`; context events: `full-05-p3-source`
- Candidate pool: `full-05-p3-pool`; hash: `0d53829dd27c52e23541d07f1c6782d3dbb09c747e5240c9d7018d7837a597cd`; snapshots: `full-05-p3-snapshot-target, full-05-p3-snapshot-aux`
- Candidate snapshot: `full-05-p3-snapshot-target`; runtime item: `full-05-p3-runtime-target`; hash: `3cfa2e0101de46eb55cf73687c106e014696dbae993066a2366949e608485e34`
- Candidate source IDs: `full-05-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for payment retry policy authoring guidance is three retries.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-05-p3-source, full-05-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-05_3

#### Checkpoints and downstream tasks

- Checkpoint `full-05-p3-checkpoint` after sequence `11`
- Task `full-05-p3-state-task` (`current_state_query`) at `full-05-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for payment retry policy authoring guidance is three retries.', 'scope': {'system': 'payment-retry-policy-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-05-p3-source']}]}`; dependencies: `full-05-p3-source, full-05-p3-event`
- Task `full-05-p3-action-task` (`action_selection`) at `full-05-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-05-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-05-p3-source, full-05-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-05-p4-pair`

- Evaluated event: `full-05-p4-event`; context events: `full-05-p4-source`
- Candidate pool: `full-05-p4-pool`; hash: `b3f155e7d802245fdc096a89fb61703607c528eff86f6bb8acc2b4d8e27b6543`; snapshots: `full-05-p4-snapshot-target, full-05-p4-snapshot-aux`
- Candidate snapshot: `full-05-p4-snapshot-target`; runtime item: `full-05-p4-runtime-target`; hash: `4229c8350e9602c156f3064e737f198f2fb2af58bc8145032252f0f84c4a8697`
- Candidate source IDs: `full-05-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use three retries for payment retry policy migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-05-p4-source, full-05-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-05_4

#### Checkpoints and downstream tasks

- Checkpoint `full-05-p4-checkpoint` after sequence `12`
- Task `full-05-p4-state-task` (`current_state_query`) at `full-05-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use three retries for payment retry policy migration plan across ordinary cases.', 'scope': {'system': 'payment-retry-policy-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-05-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'For payment retry policy migration plan, the schema inspection gives two retries as the value.', 'scope': {'system': 'payment-retry-policy-migration-plan', 'audience': 'high-risk-payments'}, 'status': 'active', 'evidence_ids': ['full-05-p4-event']}]}`; dependencies: `full-05-p4-source, full-05-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-06 — surface-family-06

- Record: [`../development.jsonl` line 4](../development.jsonl#L4)
- Partition: `pilot_development`
### Timeline and authority

- `full-06-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for account recovery flow runtime behavior is email token.'
- `full-06-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only account recovery flow runtime behavior variant uses passkey challenge within managed accounts.'
- `full-06-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for account recovery flow schema contract is email token.'
- `full-06-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only account recovery flow schema contract variant uses passkey challenge within managed accounts.'
- `full-06-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for account recovery flow authoring guidance is email token.'
- `full-06-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only account recovery flow authoring guidance variant uses passkey challenge within managed accounts.'
- `full-06-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The account recovery flow migration plan uses email token.'
- `full-06-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only account recovery flow migration plan variant uses passkey challenge within managed accounts.'
- `full-06-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The migration review records passkey challenge for account recovery flow runtime behavior.'
- `full-06-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-06-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'The ownership record reports that account recovery flow authoring guidance uses passkey challenge.'
- `full-06-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-06-p4-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'

### Pair `full-06-p1-pair`

- Evaluated event: `full-06-p1-event`; context events: `full-06-p1-source`
- Candidate pool: `full-06-p1-pool`; hash: `8f3783bc03c9e530f989d1a8da07f7de31b3259cafc623ce0c13727925be5666`; snapshots: `full-06-p1-snapshot-target, full-06-p1-snapshot-aux`
- Candidate snapshot: `full-06-p1-snapshot-target`; runtime item: `full-06-p1-runtime-target`; hash: `9dd3b569e2cc2ba048845f92136aa5379fc7d99988b287a6dd78adaa9a0e78a2`
- Candidate source IDs: `full-06-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for account recovery flow runtime behavior is email token.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p1:target`; new: `semantic:p1:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-06-p1-source, full-06-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-06_1

#### Checkpoints and downstream tasks

- Checkpoint `full-06-p1-checkpoint` after sequence `9`
- Task `full-06-p1-state-task` (`current_state_query`) at `full-06-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The current value for account recovery flow runtime behavior is email token.', 'scope': {'system': 'account-recovery-flow-runtime-behavior', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-06-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:replacement', 'proposition': 'The migration review records passkey challenge for account recovery flow runtime behavior.', 'scope': {'system': 'account-recovery-flow-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-06-p1-event']}]}`; dependencies: `full-06-p1-source, full-06-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-06-p2-pair`

- Evaluated event: `full-06-p2-event`; context events: `full-06-p2-source`
- Candidate pool: `full-06-p2-pool`; hash: `1ba749f2eb6200959f9355bbd649a748a000214ee7183d8ec33eea164fc4ef4d`; snapshots: `full-06-p2-snapshot-target, full-06-p2-snapshot-aux`
- Candidate snapshot: `full-06-p2-snapshot-target`; runtime item: `full-06-p2-runtime-target`; hash: `b462994d2a4bc2ff3f22a53d6ee901ad7f6e88e57e415b00aab67684edd0e7e8`
- Candidate source IDs: `full-06-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for account recovery flow schema contract is email token.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-06-p2-source, full-06-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-06_2

#### Checkpoints and downstream tasks

- Checkpoint `full-06-p2-checkpoint` after sequence `10`
- Task `full-06-p2-state-task` (`current_state_query`) at `full-06-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for account recovery flow schema contract is email token.', 'scope': {'system': 'account-recovery-flow-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-06-p2-source']}]}`; dependencies: `full-06-p2-source, full-06-p2-event`
- Task `full-06-p2-action-task` (`action_selection`) at `full-06-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-06-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-06-p2-source, full-06-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-06-p3-pair`

- Evaluated event: `full-06-p3-event`; context events: `full-06-p3-source`
- Candidate pool: `full-06-p3-pool`; hash: `c45d53f1e462a08d1aca79c9b125e8e036da818cefd0d1b4c0b353c51fcb3665`; snapshots: `full-06-p3-snapshot-target, full-06-p3-snapshot-aux`
- Candidate snapshot: `full-06-p3-snapshot-target`; runtime item: `full-06-p3-runtime-target`; hash: `6dddb6b61c1c457c28074d979386a3ba824aecdca1311d29ff9e578db25d2b42`
- Candidate source IDs: `full-06-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for account recovery flow authoring guidance is email token.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-06-p3-source, full-06-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-06_3

#### Checkpoints and downstream tasks

- Checkpoint `full-06-p3-checkpoint` after sequence `11`
- Task `full-06-p3-state-task` (`current_state_query`) at `full-06-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for account recovery flow authoring guidance is email token.', 'scope': {'system': 'account-recovery-flow-authoring-guidance', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-06-p3-source']}]}`; dependencies: `full-06-p3-source, full-06-p3-event`
- Task `full-06-p3-action-task` (`action_selection`) at `full-06-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-06-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-06-p3-source, full-06-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-06-p4-pair`

- Evaluated event: `full-06-p4-event`; context events: `full-06-p4-source`
- Candidate pool: `full-06-p4-pool`; hash: `9f79644c7274f2d3480e746a3e0c27fefb55332b9237062fa0eb1825269d5ce5`; snapshots: `full-06-p4-snapshot-target, full-06-p4-snapshot-aux`
- Candidate snapshot: `full-06-p4-snapshot-target`; runtime item: `full-06-p4-runtime-target`; hash: `905f40a539b8408ec86bd02cc19601a9d0d05b2e4f99e37a79f5e82bee9a2af6`
- Candidate source IDs: `full-06-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The account recovery flow migration plan uses email token.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `invalidate`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-06-p4-source, full-06-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-06_4

#### Checkpoints and downstream tasks

- Checkpoint `full-06-p4-checkpoint` after sequence `12`
- Task `full-06-p4-state-task` (`deletion_query`) at `full-06-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The account recovery flow migration plan uses email token.', 'scope': {'system': 'account-recovery-flow-migration-plan', 'audience': 'all'}, 'status': 'invalidated', 'evidence_ids': []}], 'invalidated_derivatives': [{'semantic_item_ref': 'semantic:p4:target', 'invalidated_by_event_id': 'full-06-p4-event', 'reason': 'sole_source_deleted'}]}`; dependencies: `full-06-p4-source, full-06-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-07 — surface-family-07

- Record: [`../development.jsonl` line 5](../development.jsonl#L5)
- Partition: `pilot_development`
### Timeline and authority

- `full-07-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for shipping address form runtime behavior is postal_code.'
- `full-07-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only shipping address form runtime behavior variant uses region_code within international orders.'
- `full-07-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change shipping address form schema contract to region_code.'
- `full-07-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only shipping address form schema contract variant uses region_code within international orders.'
- `full-07-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for shipping address form authoring guidance is postal_code.'
- `full-07-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only shipping address form authoring guidance variant uses region_code within international orders.'
- `full-07-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use postal_code for shipping address form migration plan across ordinary cases.'
- `full-07-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only shipping address form migration plan variant uses region_code within international orders.'
- `full-07-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'The listed shipping address form runtime behavior value is region_code, according to the compatibility review.'
- `full-07-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The migration review reports that shipping address form schema contract uses region_code.'
- `full-07-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'The incident follow-up records region_code for shipping address form authoring guidance.'
- `full-07-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'shipping-address-form-migration-plan', 'audience': 'international-orders'}}`; content: 'For shipping address form migration plan, the ownership record gives region_code as the value.'

### Pair `full-07-p1-pair`

- Evaluated event: `full-07-p1-event`; context events: `full-07-p1-source`
- Candidate pool: `full-07-p1-pool`; hash: `b40b63a63559da580719471c95afef0b0e2d812c22e2db0b9f0a26551aafd02e`; snapshots: `full-07-p1-snapshot-target, full-07-p1-snapshot-aux`
- Candidate snapshot: `full-07-p1-snapshot-target`; runtime item: `full-07-p1-runtime-target`; hash: `9fbe487da1803af7a7c9b84e33bfbdaca6cdbe1a8623ba9e6a394c19e5e372b6`
- Candidate source IDs: `full-07-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for shipping address form runtime behavior is postal_code.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p1:target`; new: `semantic:p1:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-07-p1-source, full-07-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-07_1

#### Checkpoints and downstream tasks

- Checkpoint `full-07-p1-checkpoint` after sequence `9`
- Task `full-07-p1-state-task` (`current_state_query`) at `full-07-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for shipping address form runtime behavior is postal_code.', 'scope': {'system': 'shipping-address-form-runtime-behavior', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-07-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:replacement', 'proposition': 'The listed shipping address form runtime behavior value is region_code, according to the compatibility review.', 'scope': {'system': 'shipping-address-form-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-07-p1-event']}]}`; dependencies: `full-07-p1-source, full-07-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-07-p2-pair`

- Evaluated event: `full-07-p2-event`; context events: `full-07-p2-source`
- Candidate pool: `full-07-p2-pool`; hash: `f49ddffb11898e2210c61cdcb7f3b259e2d1d62297f08d34edbb9f0afea62298`; snapshots: `full-07-p2-snapshot-target, full-07-p2-snapshot-aux`
- Candidate snapshot: `full-07-p2-snapshot-target`; runtime item: `full-07-p2-runtime-target`; hash: `37e1aca47aa6501843dfdfb00ca00a98ec13766a86c0b9997dcc308ff6f7dab3`
- Candidate source IDs: `full-07-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change shipping address form schema contract to region_code.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-07-p2-source, full-07-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-07_2

#### Checkpoints and downstream tasks

- Checkpoint `full-07-p2-checkpoint` after sequence `10`
- Task `full-07-p2-state-task` (`commitment_query`) at `full-07-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The team committed to change shipping address form schema contract to region_code.', 'scope': {'system': 'shipping-address-form-schema-contract', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-07-p2-source', 'full-07-p2-event']}]}`; dependencies: `full-07-p2-source, full-07-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-07-p3-pair`

- Evaluated event: `full-07-p3-event`; context events: `full-07-p3-source`
- Candidate pool: `full-07-p3-pool`; hash: `afcfb72b0a3a06fce097e35516acf0b808a713645152bcacae9af7041e4a06cd`; snapshots: `full-07-p3-snapshot-target, full-07-p3-snapshot-aux`
- Candidate snapshot: `full-07-p3-snapshot-target`; runtime item: `full-07-p3-runtime-target`; hash: `b6156ae2f637eb00bd9c298237f2f89fbb97cf431c35c458f59a1ab527586160`
- Candidate source IDs: `full-07-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for shipping address form authoring guidance is postal_code.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-07-p3-source, full-07-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-07_3

#### Checkpoints and downstream tasks

- Checkpoint `full-07-p3-checkpoint` after sequence `11`
- Task `full-07-p3-state-task` (`current_state_query`) at `full-07-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for shipping address form authoring guidance is postal_code.', 'scope': {'system': 'shipping-address-form-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-07-p3-source']}]}`; dependencies: `full-07-p3-source, full-07-p3-event`
- Task `full-07-p3-action-task` (`action_selection`) at `full-07-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-07-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-07-p3-source, full-07-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-07-p4-pair`

- Evaluated event: `full-07-p4-event`; context events: `full-07-p4-source`
- Candidate pool: `full-07-p4-pool`; hash: `d99caa4ae1d473b1ff0fe7b18f8f9c656496630ac339c726652fa11c943290d6`; snapshots: `full-07-p4-snapshot-target, full-07-p4-snapshot-aux`
- Candidate snapshot: `full-07-p4-snapshot-target`; runtime item: `full-07-p4-runtime-target`; hash: `817fb3c9cc33acd661fc6211c5510087a62245360341e45b83d789f9fc0ef597`
- Candidate source IDs: `full-07-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use postal_code for shipping address form migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-07-p4-source, full-07-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-07_4

#### Checkpoints and downstream tasks

- Checkpoint `full-07-p4-checkpoint` after sequence `12`
- Task `full-07-p4-state-task` (`current_state_query`) at `full-07-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use postal_code for shipping address form migration plan across ordinary cases.', 'scope': {'system': 'shipping-address-form-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-07-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'For shipping address form migration plan, the ownership record gives region_code as the value.', 'scope': {'system': 'shipping-address-form-migration-plan', 'audience': 'international-orders'}, 'status': 'active', 'evidence_ids': ['full-07-p4-event']}]}`; dependencies: `full-07-p4-source, full-07-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-08 — surface-family-08

- Record: [`../development.jsonl` line 6](../development.jsonl#L6)
- Partition: `pilot_development`
### Timeline and authority

- `full-08-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for analytics envelope runtime behavior is screen_id.'
- `full-08-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only analytics envelope runtime behavior variant uses route_id within embedded web views.'
- `full-08-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for analytics envelope schema contract is screen_id.'
- `full-08-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only analytics envelope schema contract variant uses route_id within embedded web views.'
- `full-08-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The analytics envelope authoring guidance uses screen_id.'
- `full-08-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The analytics envelope authoring guidance uses screen_id.'
- `full-08-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The analytics envelope migration plan uses screen_id.'
- `full-08-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only analytics envelope migration plan variant uses route_id within embedded web views.'
- `full-08-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'The architecture note records route_id for analytics envelope runtime behavior.'
- `full-08-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'The compatibility review records route_id for analytics envelope schema contract.'
- `full-08-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-08-p3-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-08-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A staff update described road delays near the office after overnight construction.'

### Pair `full-08-p1-pair`

- Evaluated event: `full-08-p1-event`; context events: `full-08-p1-source`
- Candidate pool: `full-08-p1-pool`; hash: `0954c62e19c9cfad104fd565b088dde896225d20813fe5df067e3ec183b5415a`; snapshots: `full-08-p1-snapshot-target, full-08-p1-snapshot-aux`
- Candidate snapshot: `full-08-p1-snapshot-target`; runtime item: `full-08-p1-runtime-target`; hash: `321f16cf13393c26ed5522ce8232644e8544203f9fe7d9a53ffa4d505f324ed7`
- Candidate source IDs: `full-08-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for analytics envelope runtime behavior is screen_id.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-08-p1-source, full-08-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-08_1

#### Checkpoints and downstream tasks

- Checkpoint `full-08-p1-checkpoint` after sequence `9`
- Task `full-08-p1-state-task` (`current_state_query`) at `full-08-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for analytics envelope runtime behavior is screen_id.', 'scope': {'system': 'analytics-envelope-runtime-behavior', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-08-p1-source']}]}`; dependencies: `full-08-p1-source, full-08-p1-event`
- Task `full-08-p1-action-task` (`action_selection`) at `full-08-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-08-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-08-p1-source, full-08-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-08-p2-pair`

- Evaluated event: `full-08-p2-event`; context events: `full-08-p2-source`
- Candidate pool: `full-08-p2-pool`; hash: `fa0b520ebb10598014d87e66d71f6de50ba4b49df5eec45761fa33fd0ec81255`; snapshots: `full-08-p2-snapshot-target, full-08-p2-snapshot-aux`
- Candidate snapshot: `full-08-p2-snapshot-target`; runtime item: `full-08-p2-runtime-target`; hash: `f41a786a1a3afaf75e73632b06ce0b85f931665f5732144c4d56f0e553d5c219`
- Candidate source IDs: `full-08-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for analytics envelope schema contract is screen_id.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-08-p2-source, full-08-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-08_2

#### Checkpoints and downstream tasks

- Checkpoint `full-08-p2-checkpoint` after sequence `10`
- Task `full-08-p2-state-task` (`current_state_query`) at `full-08-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for analytics envelope schema contract is screen_id.', 'scope': {'system': 'analytics-envelope-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-08-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The compatibility review records route_id for analytics envelope schema contract.', 'scope': {'system': 'analytics-envelope-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-08-p2-event']}]}`; dependencies: `full-08-p2-source, full-08-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-08-p3-pair`

- Evaluated event: `full-08-p3-event`; context events: `full-08-p3-source, full-08-p3-aux`
- Candidate pool: `full-08-p3-pool`; hash: `7b0a0fedab07e16695afd305a736d768650c00a99e75f7a973476dcb2a32743c`; snapshots: `full-08-p3-snapshot-target, full-08-p3-snapshot-aux`
- Candidate snapshot: `full-08-p3-snapshot-target`; runtime item: `full-08-p3-runtime-target`; hash: `5feaa68d603c70bd51ddd40b915aec1afcc2e538337f5d74ae0f787b83fcfffb`
- Candidate source IDs: `full-08-p3-source, full-08-p3-aux`; counterevidence IDs: `none`
- Candidate proposition: The analytics envelope authoring guidance uses screen_id.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-08-p3-source, full-08-p3-aux, full-08-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-08_3

#### Checkpoints and downstream tasks

- Checkpoint `full-08-p3-checkpoint` after sequence `11`
- Task `full-08-p3-state-task` (`deletion_query`) at `full-08-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The analytics envelope authoring guidance uses screen_id.', 'scope': {'system': 'analytics-envelope-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-08-p3-aux']}], 'invalidated_derivatives': []}`; dependencies: `full-08-p3-source, full-08-p3-aux, full-08-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-08-p4-pair`

- Evaluated event: `full-08-p4-event`; context events: `full-08-p4-source`
- Candidate pool: `full-08-p4-pool`; hash: `f4c8abb0989af9e08492e96df8beb057b8a891756b11f8b5e42900fc43842e17`; snapshots: `full-08-p4-snapshot-target, full-08-p4-snapshot-aux`
- Candidate snapshot: `full-08-p4-snapshot-target`; runtime item: `full-08-p4-runtime-target`; hash: `57946667dea8abc723f897160c743dd896f10af03631b9af58b8f0bfe55750cc`
- Candidate source IDs: `full-08-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The analytics envelope migration plan uses screen_id.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-08-p4-source, full-08-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-08_4

#### Checkpoints and downstream tasks

- Checkpoint `full-08-p4-checkpoint` after sequence `12`
- Task `full-08-p4-state-task` (`current_state_query`) at `full-08-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The analytics envelope migration plan uses screen_id.', 'scope': {'system': 'analytics-envelope-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-08-p4-source']}]}`; dependencies: `full-08-p4-source, full-08-p4-event`
- Task `full-08-p4-action-task` (`action_selection`) at `full-08-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-08-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-08-p4-source, full-08-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-09 — surface-family-09

- Record: [`../development.jsonl` line 7](../development.jsonl#L7)
- Partition: `pilot_development`
### Timeline and authority

- `full-09-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for feature flag client runtime behavior is polling.'
- `full-09-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only feature flag client runtime behavior variant uses streaming within low-power devices.'
- `full-09-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for feature flag client schema contract is polling.'
- `full-09-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only feature flag client schema contract variant uses streaming within low-power devices.'
- `full-09-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for feature flag client authoring guidance is polling.'
- `full-09-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only feature flag client authoring guidance variant uses streaming within low-power devices.'
- `full-09-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use polling for feature flag client migration plan across ordinary cases.'
- `full-09-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only feature flag client migration plan variant uses streaming within low-power devices.'
- `full-09-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'For feature flag client runtime behavior, the release checklist gives streaming as the value.'
- `full-09-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed feature flag client schema contract value is streaming, according to the architecture note.'
- `full-09-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The compatibility review reports that feature flag client authoring guidance uses polling.'
- `full-09-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'feature-flag-client-migration-plan', 'audience': 'low-power-devices'}}`; content: 'The listed feature flag client migration plan value is streaming, according to the migration review.'

### Pair `full-09-p1-pair`

- Evaluated event: `full-09-p1-event`; context events: `full-09-p1-source`
- Candidate pool: `full-09-p1-pool`; hash: `1441e03e972ce95909081601bd4ab140080d0159cda2598670441cd897a62e87`; snapshots: `full-09-p1-snapshot-target, full-09-p1-snapshot-aux`
- Candidate snapshot: `full-09-p1-snapshot-target`; runtime item: `full-09-p1-runtime-target`; hash: `40a12d1693a535e0aceaf83c8395fdfa7cf8e32037bc6af25a0c22d9ccccb306`
- Candidate source IDs: `full-09-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for feature flag client runtime behavior is polling.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-09-p1-source, full-09-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-09_1

#### Checkpoints and downstream tasks

- Checkpoint `full-09-p1-checkpoint` after sequence `9`
- Task `full-09-p1-state-task` (`current_state_query`) at `full-09-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for feature flag client runtime behavior is polling.', 'scope': {'system': 'feature-flag-client-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-09-p1-source']}]}`; dependencies: `full-09-p1-source, full-09-p1-event`
- Task `full-09-p1-action-task` (`action_selection`) at `full-09-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-09-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-09-p1-source, full-09-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-09-p2-pair`

- Evaluated event: `full-09-p2-event`; context events: `full-09-p2-source`
- Candidate pool: `full-09-p2-pool`; hash: `67b443bfa6ee854c3b92956e43829725a9701db25b5f6147f15eb2dc1d24c1b3`; snapshots: `full-09-p2-snapshot-target, full-09-p2-snapshot-aux`
- Candidate snapshot: `full-09-p2-snapshot-target`; runtime item: `full-09-p2-runtime-target`; hash: `79fe529e17c635c61a13160383c9d3d7d64ed952da91e189f1645713fd53ca75`
- Candidate source IDs: `full-09-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for feature flag client schema contract is polling.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-09-p2-source, full-09-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-09_2

#### Checkpoints and downstream tasks

- Checkpoint `full-09-p2-checkpoint` after sequence `10`
- Task `full-09-p2-state-task` (`current_state_query`) at `full-09-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The current value for feature flag client schema contract is polling.', 'scope': {'system': 'feature-flag-client-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-09-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The listed feature flag client schema contract value is streaming, according to the architecture note.', 'scope': {'system': 'feature-flag-client-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-09-p2-event']}]}`; dependencies: `full-09-p2-source, full-09-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-09-p3-pair`

- Evaluated event: `full-09-p3-event`; context events: `full-09-p3-source`
- Candidate pool: `full-09-p3-pool`; hash: `fecd6d7101c6b73f65ddd4da5a58e6dccb97d7ef83c946cad6161073b991c649`; snapshots: `full-09-p3-snapshot-target, full-09-p3-snapshot-aux`
- Candidate snapshot: `full-09-p3-snapshot-target`; runtime item: `full-09-p3-runtime-target`; hash: `84a35326193da0c2a766f09d7e56e9dbd7740b7e6058af26bcc5df9fc725f312`
- Candidate source IDs: `full-09-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for feature flag client authoring guidance is polling.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-09-p3-source, full-09-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-09_3

#### Checkpoints and downstream tasks

- Checkpoint `full-09-p3-checkpoint` after sequence `11`
- Task `full-09-p3-state-task` (`current_state_query`) at `full-09-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The accepted preference for feature flag client authoring guidance is polling.', 'scope': {'system': 'feature-flag-client-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-09-p3-source', 'full-09-p3-event']}]}`; dependencies: `full-09-p3-source, full-09-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-09-p4-pair`

- Evaluated event: `full-09-p4-event`; context events: `full-09-p4-source`
- Candidate pool: `full-09-p4-pool`; hash: `df082d675567018cd45b586c7d444b200b5372b759a8c4e954f3c67735dde7df`; snapshots: `full-09-p4-snapshot-target, full-09-p4-snapshot-aux`
- Candidate snapshot: `full-09-p4-snapshot-target`; runtime item: `full-09-p4-runtime-target`; hash: `f990050b74a6e2346d7243e1e0afb9597e5577584d003daa7d8f1eb013d0cafb`
- Candidate source IDs: `full-09-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use polling for feature flag client migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-09-p4-source, full-09-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-09_4

#### Checkpoints and downstream tasks

- Checkpoint `full-09-p4-checkpoint` after sequence `12`
- Task `full-09-p4-state-task` (`current_state_query`) at `full-09-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use polling for feature flag client migration plan across ordinary cases.', 'scope': {'system': 'feature-flag-client-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-09-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'The listed feature flag client migration plan value is streaming, according to the migration review.', 'scope': {'system': 'feature-flag-client-migration-plan', 'audience': 'low-power-devices'}, 'status': 'active', 'evidence_ids': ['full-09-p4-event']}]}`; dependencies: `full-09-p4-source, full-09-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-10 — surface-family-10

- Record: [`../holdout.jsonl` line 3](../holdout.jsonl#L3)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-10-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to review image loader runtime behavior before 09:00 UTC.'
- `full-10-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only image loader runtime behavior variant uses responsive assets within metered networks.'
- `full-10-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The image loader schema contract uses original assets.'
- `full-10-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only image loader schema contract variant uses responsive assets within metered networks.'
- `full-10-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use original assets for image loader authoring guidance across ordinary cases.'
- `full-10-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only image loader authoring guidance variant uses responsive assets within metered networks.'
- `full-10-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for image loader migration plan is original assets.'
- `full-10-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only image loader migration plan variant uses responsive assets within metered networks.'
- `full-10-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `evaluator`; type `time_advance`; assert `false`; transition `true`; reason: evaluator clock event for lifecycle evaluation only; deletion targets: `none`; metadata: `{'advance_to': '2026-09-18T10:00:00Z'}`; content: None
- `full-10-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-10-p2-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-10-p3-event` — seq 11; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'image-loader-authoring-guidance', 'audience': 'metered-networks'}}`; content: 'Late report, effective 2026-09-16: The architecture note records responsive assets for image loader authoring guidance.'
- `full-10-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The selected arrangement depends on which request is meant; the current note gives no distinguishing detail.'

### Pair `full-10-p1-pair`

- Evaluated event: `full-10-p1-event`; context events: `full-10-p1-source`
- Candidate pool: `full-10-p1-pool`; hash: `fa54542cc3db00bf33f42181cddbd90f4fd5633cdb4a35698e9de8f427dfcc9c`; snapshots: `full-10-p1-snapshot-target, full-10-p1-snapshot-aux`
- Candidate snapshot: `full-10-p1-snapshot-target`; runtime item: `full-10-p1-runtime-target`; hash: `665db67e64bf5eeae0bc4441f8821ea20cb2357ed67918358272cb7bb713ee1f`
- Candidate source IDs: `full-10-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to review image loader runtime behavior before 09:00 UTC.
- Candidate validity: `2026-09-17T12:00:00Z` through `2026-09-18T09:00:00Z`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `expire`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-10-p1-source, full-10-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-10_1

#### Checkpoints and downstream tasks

- Checkpoint `full-10-p1-checkpoint` after sequence `9`
- Task `full-10-p1-state-task` (`commitment_query`) at `full-10-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The team committed to review image loader runtime behavior before 09:00 UTC.', 'scope': {'system': 'image-loader-runtime-behavior', 'audience': 'all'}, 'status': 'expired', 'evidence_ids': ['full-10-p1-source']}]}`; dependencies: `full-10-p1-source, full-10-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-10-p2-pair`

- Evaluated event: `full-10-p2-event`; context events: `full-10-p2-source`
- Candidate pool: `full-10-p2-pool`; hash: `a3521034989647165af97b18432b416409d5d71057a805b4ab13ad602b925021`; snapshots: `full-10-p2-snapshot-target, full-10-p2-snapshot-aux`
- Candidate snapshot: `full-10-p2-snapshot-target`; runtime item: `full-10-p2-runtime-target`; hash: `2d15d0d15bd616fc1c15ccf559b3265a86af25a5a80128b16cf03e5d478ed0e4`
- Candidate source IDs: `full-10-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The image loader schema contract uses original assets.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `invalidate`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-10-p2-source, full-10-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-10_2

#### Checkpoints and downstream tasks

- Checkpoint `full-10-p2-checkpoint` after sequence `10`
- Task `full-10-p2-state-task` (`deletion_query`) at `full-10-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The image loader schema contract uses original assets.', 'scope': {'system': 'image-loader-schema-contract', 'audience': 'all'}, 'status': 'invalidated', 'evidence_ids': []}], 'invalidated_derivatives': [{'semantic_item_ref': 'semantic:p2:target', 'invalidated_by_event_id': 'full-10-p2-event', 'reason': 'sole_source_deleted'}]}`; dependencies: `full-10-p2-source, full-10-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-10-p3-pair`

- Evaluated event: `full-10-p3-event`; context events: `full-10-p3-source`
- Candidate pool: `full-10-p3-pool`; hash: `a6a6edf336a87a37e361625b0432a437ad946e0afa1536dfb0a5047f5146644f`; snapshots: `full-10-p3-snapshot-target, full-10-p3-snapshot-aux`
- Candidate snapshot: `full-10-p3-snapshot-target`; runtime item: `full-10-p3-runtime-target`; hash: `94b12c2a47fd9b447462955fd1541edf4c6a4a6cc4dde3d33b936e31ead24f60`
- Candidate source IDs: `full-10-p3-source`; counterevidence IDs: `none`
- Candidate proposition: Use original assets for image loader authoring guidance across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p3:target`; new: `semantic:p3:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-10-p3-source, full-10-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-10_3

#### Checkpoints and downstream tasks

- Checkpoint `full-10-p3-checkpoint` after sequence `11`
- Task `full-10-p3-state-task` (`current_state_query`) at `full-10-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'Use original assets for image loader authoring guidance across ordinary cases.', 'scope': {'system': 'image-loader-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-10-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:scoped', 'proposition': 'Late report, effective 2026-09-16: The architecture note records responsive assets for image loader authoring guidance.', 'scope': {'system': 'image-loader-authoring-guidance', 'audience': 'metered-networks'}, 'status': 'active', 'evidence_ids': ['full-10-p3-event']}]}`; dependencies: `full-10-p3-source, full-10-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-10-p4-pair`

- Evaluated event: `full-10-p4-event`; context events: `full-10-p4-source`
- Candidate pool: `full-10-p4-pool`; hash: `ea853cfb273013a9b27d4e8cbf5543a442b603ee2779ede2523037ddbd1d29c3`; snapshots: `full-10-p4-snapshot-target, full-10-p4-snapshot-aux`
- Candidate snapshot: `full-10-p4-snapshot-target`; runtime item: `full-10-p4-runtime-target`; hash: `d45a9e3cdc4cc6c0b8feedf7fc700bdfa2357fc81fb98f6b45b306c14382829c`
- Candidate source IDs: `full-10-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for image loader migration plan is original assets.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-10-p4-source, full-10-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-10_4

#### Checkpoints and downstream tasks

- Checkpoint `full-10-p4-checkpoint` after sequence `12`
- Task `full-10-p4-state-task` (`current_state_query`) at `full-10-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for image loader migration plan is original assets.', 'scope': {'system': 'image-loader-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-10-p4-source']}]}`; dependencies: `full-10-p4-source, full-10-p4-event`
- Task `full-10-p4-action-task` (`action_selection`) at `full-10-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-10-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-10-p4-source, full-10-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-11 — surface-family-01

- Record: [`../holdout.jsonl` line 4](../holdout.jsonl#L4)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-11-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for catalog cache runtime behavior is six hours.'
- `full-11-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only catalog cache runtime behavior variant uses one hour within flash sales.'
- `full-11-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for catalog cache schema contract is six hours.'
- `full-11-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only catalog cache schema contract variant uses one hour within flash sales.'
- `full-11-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for catalog cache authoring guidance is six hours.'
- `full-11-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only catalog cache authoring guidance variant uses one hour within flash sales.'
- `full-11-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for catalog cache migration plan is six hours.'
- `full-11-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only catalog cache migration plan variant uses one hour within flash sales.'
- `full-11-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'For catalog cache runtime behavior, the test report gives one hour as the value.'
- `full-11-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'The listed catalog cache schema contract value is one hour, according to the registry audit.'
- `full-11-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The release checklist reports that catalog cache authoring guidance uses one hour.'
- `full-11-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'

### Pair `full-11-p1-pair`

- Evaluated event: `full-11-p1-event`; context events: `full-11-p1-source`
- Candidate pool: `full-11-p1-pool`; hash: `9f11e66e3a075c9bba38038a3ba8303844658dc203989fdebf7686d5ce919583`; snapshots: `full-11-p1-snapshot-target, full-11-p1-snapshot-aux`
- Candidate snapshot: `full-11-p1-snapshot-target`; runtime item: `full-11-p1-runtime-target`; hash: `1dad014a221b513f3320a589162e6ba52ee16b4e26611ad997aa0b825ac395aa`
- Candidate source IDs: `full-11-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for catalog cache runtime behavior is six hours.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-11-p1-source, full-11-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-11_1

#### Checkpoints and downstream tasks

- Checkpoint `full-11-p1-checkpoint` after sequence `9`
- Task `full-11-p1-state-task` (`current_state_query`) at `full-11-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for catalog cache runtime behavior is six hours.', 'scope': {'system': 'catalog-cache-runtime-behavior', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-11-p1-source']}]}`; dependencies: `full-11-p1-source, full-11-p1-event`
- Task `full-11-p1-action-task` (`action_selection`) at `full-11-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-11-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-11-p1-source, full-11-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-11-p2-pair`

- Evaluated event: `full-11-p2-event`; context events: `full-11-p2-source`
- Candidate pool: `full-11-p2-pool`; hash: `b4fa1d1eae051a292f6e5e383c833439d89e66faaf0d846a3f4182c2131b15cc`; snapshots: `full-11-p2-snapshot-target, full-11-p2-snapshot-aux`
- Candidate snapshot: `full-11-p2-snapshot-target`; runtime item: `full-11-p2-runtime-target`; hash: `9f5893f66a1fc94b9029ccff557c439a7d9895e9d6f4c368796b792a3c698e53`
- Candidate source IDs: `full-11-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for catalog cache schema contract is six hours.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-11-p2-source, full-11-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-11_2

#### Checkpoints and downstream tasks

- Checkpoint `full-11-p2-checkpoint` after sequence `10`
- Task `full-11-p2-state-task` (`current_state_query`) at `full-11-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for catalog cache schema contract is six hours.', 'scope': {'system': 'catalog-cache-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-11-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The listed catalog cache schema contract value is one hour, according to the registry audit.', 'scope': {'system': 'catalog-cache-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-11-p2-event']}]}`; dependencies: `full-11-p2-source, full-11-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-11-p3-pair`

- Evaluated event: `full-11-p3-event`; context events: `full-11-p3-source`
- Candidate pool: `full-11-p3-pool`; hash: `6e5106654bf12fe3ec6914c600c70c5b3a46d2cccfe7c9e7c476cb1243e5d553`; snapshots: `full-11-p3-snapshot-target, full-11-p3-snapshot-aux`
- Candidate snapshot: `full-11-p3-snapshot-target`; runtime item: `full-11-p3-runtime-target`; hash: `5027bd074740f33c8cb910e6bb754a23b4c56763b29629f813d872d30011c004`
- Candidate source IDs: `full-11-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for catalog cache authoring guidance is six hours.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-11-p3-source, full-11-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-11_3

#### Checkpoints and downstream tasks

- Checkpoint `full-11-p3-checkpoint` after sequence `11`
- Task `full-11-p3-state-task` (`current_state_query`) at `full-11-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The current value for catalog cache authoring guidance is six hours.', 'scope': {'system': 'catalog-cache-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-11-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'The release checklist reports that catalog cache authoring guidance uses one hour.', 'scope': {'system': 'catalog-cache-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-11-p3-event']}]}`; dependencies: `full-11-p3-source, full-11-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-11-p4-pair`

- Evaluated event: `full-11-p4-event`; context events: `full-11-p4-source`
- Candidate pool: `full-11-p4-pool`; hash: `795f89b8859b7485dea065ee0dd3661b0f410264a22621e9eed96bdc71db6918`; snapshots: `full-11-p4-snapshot-target, full-11-p4-snapshot-aux`
- Candidate snapshot: `full-11-p4-snapshot-target`; runtime item: `full-11-p4-runtime-target`; hash: `25f24a0ff2d743a35a6e5cfed515713ea12f93d8e1efb67d9b2f89c44cd1b247`
- Candidate source IDs: `full-11-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for catalog cache migration plan is six hours.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-11-p4-source, full-11-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-11_4

#### Checkpoints and downstream tasks

- Checkpoint `full-11-p4-checkpoint` after sequence `12`
- Task `full-11-p4-state-task` (`current_state_query`) at `full-11-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for catalog cache migration plan is six hours.', 'scope': {'system': 'catalog-cache-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-11-p4-source']}]}`; dependencies: `full-11-p4-source, full-11-p4-event`
- Task `full-11-p4-action-task` (`action_selection`) at `full-11-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-11-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-11-p4-source, full-11-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-12 — surface-family-02

- Record: [`../holdout.jsonl` line 5](../holdout.jsonl#L5)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-12-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for consent banner runtime behavior is single prompt.'
- `full-12-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Validation policy requires investigation of an authorized transition whose validity interval ends before it begins.'
- `full-12-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The consent banner schema contract uses single prompt.'
- `full-12-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The consent banner schema contract uses single prompt.'
- `full-12-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for consent banner authoring guidance is single prompt.'
- `full-12-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only consent banner authoring guidance variant uses layered prompt within minor accounts.'
- `full-12-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for consent banner migration plan is single prompt.'
- `full-12-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only consent banner migration plan variant uses layered prompt within minor accounts.'
- `full-12-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'valid_from': '2026-10-01T00:00:00Z', 'valid_until': '2026-09-01T00:00:00Z'}`; content: 'The listed consent banner runtime behavior value is single prompt, according to the schema inspection.'
- `full-12-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-12-p2-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-12-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'The listed consent banner authoring guidance value is layered prompt, according to the registry audit.'
- `full-12-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'

### Pair `full-12-p1-pair`

- Evaluated event: `full-12-p1-event`; context events: `full-12-p1-source, full-12-p1-aux`
- Candidate pool: `full-12-p1-pool`; hash: `309f55bfd11fbfc6e0c88024b5a8dac13feb1ddd1ae9b3449d301cbe84b29012`; snapshots: `full-12-p1-snapshot-target, full-12-p1-snapshot-aux`
- Candidate snapshot: `full-12-p1-snapshot-target`; runtime item: `full-12-p1-runtime-target`; hash: `03878c9e9f99518615a29df1567175fdc3c1b33a306f17b1f44c9ddfcb6bff99`
- Candidate source IDs: `full-12-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for consent banner runtime behavior is single prompt.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `reject_invalid`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `investigate`; action-selection task present: `true`
- Required evidence IDs: `full-12-p1-source, full-12-p1-aux, full-12-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-12_1

#### Checkpoints and downstream tasks

- Checkpoint `full-12-p1-checkpoint` after sequence `9`
- Task `full-12-p1-state-task` (`current_state_query`) at `full-12-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for consent banner runtime behavior is single prompt.', 'scope': {'system': 'consent-banner-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-12-p1-source']}]}`; dependencies: `full-12-p1-source, full-12-p1-aux, full-12-p1-event`
- Task `full-12-p1-action-task` (`action_selection`) at `full-12-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-12-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'investigate'}`; dependencies: `full-12-p1-source, full-12-p1-aux, full-12-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-12-p2-pair`

- Evaluated event: `full-12-p2-event`; context events: `full-12-p2-source, full-12-p2-aux`
- Candidate pool: `full-12-p2-pool`; hash: `f6df1d0e0fbd071136624345c5850518163fe500f5c5cbc4a9d26534c1b3d6fa`; snapshots: `full-12-p2-snapshot-target, full-12-p2-snapshot-aux`
- Candidate snapshot: `full-12-p2-snapshot-target`; runtime item: `full-12-p2-runtime-target`; hash: `523e93bd24a24010eac4490b59697624077e4985cc0960d36e308d28b6a87e13`
- Candidate source IDs: `full-12-p2-source, full-12-p2-aux`; counterevidence IDs: `none`
- Candidate proposition: The consent banner schema contract uses single prompt.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-12-p2-source, full-12-p2-aux, full-12-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-12_2

#### Checkpoints and downstream tasks

- Checkpoint `full-12-p2-checkpoint` after sequence `10`
- Task `full-12-p2-state-task` (`deletion_query`) at `full-12-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The consent banner schema contract uses single prompt.', 'scope': {'system': 'consent-banner-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-12-p2-aux']}], 'invalidated_derivatives': []}`; dependencies: `full-12-p2-source, full-12-p2-aux, full-12-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-12-p3-pair`

- Evaluated event: `full-12-p3-event`; context events: `full-12-p3-source`
- Candidate pool: `full-12-p3-pool`; hash: `d3a3d5a13e10a640441a4443d453bb4af2f65de807422cf4e07b39e4590c1ed0`; snapshots: `full-12-p3-snapshot-target, full-12-p3-snapshot-aux`
- Candidate snapshot: `full-12-p3-snapshot-target`; runtime item: `full-12-p3-runtime-target`; hash: `a003fcc5cf83593fa1bcf5b57af5673636fdff0709657b1d418672344b1d2887`
- Candidate source IDs: `full-12-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for consent banner authoring guidance is single prompt.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-12-p3-source, full-12-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-12_3

#### Checkpoints and downstream tasks

- Checkpoint `full-12-p3-checkpoint` after sequence `11`
- Task `full-12-p3-state-task` (`current_state_query`) at `full-12-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for consent banner authoring guidance is single prompt.', 'scope': {'system': 'consent-banner-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-12-p3-source']}]}`; dependencies: `full-12-p3-source, full-12-p3-event`
- Task `full-12-p3-action-task` (`action_selection`) at `full-12-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-12-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-12-p3-source, full-12-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-12-p4-pair`

- Evaluated event: `full-12-p4-event`; context events: `full-12-p4-source`
- Candidate pool: `full-12-p4-pool`; hash: `f8c189a5d4aae085e6bbd2cf7f0bf7117480591316f9eede063a514fb218745d`; snapshots: `full-12-p4-snapshot-target, full-12-p4-snapshot-aux`
- Candidate snapshot: `full-12-p4-snapshot-target`; runtime item: `full-12-p4-runtime-target`; hash: `c21b19f2b4591e923fefa6b9079a9f96530027b2c57d50e260c5ec21f861848a`
- Candidate source IDs: `full-12-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for consent banner migration plan is single prompt.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-12-p4-source, full-12-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-12_4

#### Checkpoints and downstream tasks

- Checkpoint `full-12-p4-checkpoint` after sequence `12`
- Task `full-12-p4-state-task` (`current_state_query`) at `full-12-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for consent banner migration plan is single prompt.', 'scope': {'system': 'consent-banner-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-12-p4-source']}]}`; dependencies: `full-12-p4-source, full-12-p4-event`
- Task `full-12-p4-action-task` (`action_selection`) at `full-12-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-12-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-12-p4-source, full-12-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-13 — surface-family-03

- Record: [`../development.jsonl` line 8](../development.jsonl#L8)
- Partition: `pilot_development`
### Timeline and authority

- `full-13-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change order history query runtime behavior to cursor tokens.'
- `full-13-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only order history query runtime behavior variant uses cursor tokens within archived orders.'
- `full-13-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for order history query schema contract is page offsets.'
- `full-13-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only order history query schema contract variant uses cursor tokens within archived orders.'
- `full-13-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use page offsets for order history query authoring guidance across ordinary cases.'
- `full-13-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only order history query authoring guidance variant uses cursor tokens within archived orders.'
- `full-13-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for order history query migration plan is page offsets.'
- `full-13-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only order history query migration plan variant uses cursor tokens within archived orders.'
- `full-13-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The maintainer journal records cursor tokens for order history query runtime behavior.'
- `full-13-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-13-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'order-history-query-authoring-guidance', 'audience': 'archived-orders'}}`; content: 'For order history query authoring guidance, the test report gives cursor tokens as the value.'
- `full-13-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'For order history query migration plan, the registry audit gives cursor tokens as the value.'

### Pair `full-13-p1-pair`

- Evaluated event: `full-13-p1-event`; context events: `full-13-p1-source`
- Candidate pool: `full-13-p1-pool`; hash: `4766d2e53c716445cc988f07430a8ed69b6bdb74b7e409514a0f588ae08fc39e`; snapshots: `full-13-p1-snapshot-target, full-13-p1-snapshot-aux`
- Candidate snapshot: `full-13-p1-snapshot-target`; runtime item: `full-13-p1-runtime-target`; hash: `b80deadf4c95e4a3ca9143893ab6b034bd30d3db35eba503db303f6517d3acab`
- Candidate source IDs: `full-13-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change order history query runtime behavior to cursor tokens.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-13-p1-source, full-13-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-13_1

#### Checkpoints and downstream tasks

- Checkpoint `full-13-p1-checkpoint` after sequence `9`
- Task `full-13-p1-state-task` (`commitment_query`) at `full-13-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The team committed to change order history query runtime behavior to cursor tokens.', 'scope': {'system': 'order-history-query-runtime-behavior', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-13-p1-source', 'full-13-p1-event']}]}`; dependencies: `full-13-p1-source, full-13-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-13-p2-pair`

- Evaluated event: `full-13-p2-event`; context events: `full-13-p2-source`
- Candidate pool: `full-13-p2-pool`; hash: `7ff4e6fe58b527cfa1ddc1a77b9b7cb2c490f3ecc6e06376555b844616301520`; snapshots: `full-13-p2-snapshot-target, full-13-p2-snapshot-aux`
- Candidate snapshot: `full-13-p2-snapshot-target`; runtime item: `full-13-p2-runtime-target`; hash: `d3d8e91d1516b5e267f8367eb57e0d1a933eb85b0ce5eaf736c20cb38b490de6`
- Candidate source IDs: `full-13-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for order history query schema contract is page offsets.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-13-p2-source, full-13-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-13_2

#### Checkpoints and downstream tasks

- Checkpoint `full-13-p2-checkpoint` after sequence `10`
- Task `full-13-p2-state-task` (`current_state_query`) at `full-13-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for order history query schema contract is page offsets.', 'scope': {'system': 'order-history-query-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-13-p2-source']}]}`; dependencies: `full-13-p2-source, full-13-p2-event`
- Task `full-13-p2-action-task` (`action_selection`) at `full-13-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-13-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-13-p2-source, full-13-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-13-p3-pair`

- Evaluated event: `full-13-p3-event`; context events: `full-13-p3-source`
- Candidate pool: `full-13-p3-pool`; hash: `c5c6d0d546091b07cd2625db0d2118c7105a0f1eaf39e71fc0bc04f6b8c7da29`; snapshots: `full-13-p3-snapshot-target, full-13-p3-snapshot-aux`
- Candidate snapshot: `full-13-p3-snapshot-target`; runtime item: `full-13-p3-runtime-target`; hash: `f034b31b73da8d0adbb0e8e192386d62cdd82b1036bbe7f76479f542562e5cdc`
- Candidate source IDs: `full-13-p3-source`; counterevidence IDs: `none`
- Candidate proposition: Use page offsets for order history query authoring guidance across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p3:target`; new: `semantic:p3:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-13-p3-source, full-13-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-13_3

#### Checkpoints and downstream tasks

- Checkpoint `full-13-p3-checkpoint` after sequence `11`
- Task `full-13-p3-state-task` (`current_state_query`) at `full-13-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'Use page offsets for order history query authoring guidance across ordinary cases.', 'scope': {'system': 'order-history-query-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-13-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:scoped', 'proposition': 'For order history query authoring guidance, the test report gives cursor tokens as the value.', 'scope': {'system': 'order-history-query-authoring-guidance', 'audience': 'archived-orders'}, 'status': 'active', 'evidence_ids': ['full-13-p3-event']}]}`; dependencies: `full-13-p3-source, full-13-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-13-p4-pair`

- Evaluated event: `full-13-p4-event`; context events: `full-13-p4-source`
- Candidate pool: `full-13-p4-pool`; hash: `75a29b84904ce9bb3e8b58310d047a93a961bca68bc8744c8427a1d44b6d410b`; snapshots: `full-13-p4-snapshot-target, full-13-p4-snapshot-aux`
- Candidate snapshot: `full-13-p4-snapshot-target`; runtime item: `full-13-p4-runtime-target`; hash: `9fa00acf68b6905ae82cc2ed13094afd089a4a13813a79851c90b4374b9e28ef`
- Candidate source IDs: `full-13-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for order history query migration plan is page offsets.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-13-p4-source, full-13-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-13_4

#### Checkpoints and downstream tasks

- Checkpoint `full-13-p4-checkpoint` after sequence `12`
- Task `full-13-p4-state-task` (`current_state_query`) at `full-13-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for order history query migration plan is page offsets.', 'scope': {'system': 'order-history-query-migration-plan', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-13-p4-source']}]}`; dependencies: `full-13-p4-source, full-13-p4-event`
- Task `full-13-p4-action-task` (`action_selection`) at `full-13-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-13-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-13-p4-source, full-13-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-14 — surface-family-04

- Record: [`../development.jsonl` line 9](../development.jsonl#L9)
- Partition: `pilot_development`
### Timeline and authority

- `full-14-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for support chat launcher runtime behavior is floating button.'
- `full-14-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only support chat launcher runtime behavior variant uses help menu within restricted regions.'
- `full-14-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use floating button for support chat launcher schema contract across ordinary cases.'
- `full-14-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only support chat launcher schema contract variant uses help menu within restricted regions.'
- `full-14-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for support chat launcher authoring guidance is floating button.'
- `full-14-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only support chat launcher authoring guidance variant uses help menu within restricted regions.'
- `full-14-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Provider H14 may satisfy the needs of support chat launcher migration plan.'
- `full-14-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The user has an active approved goal to prepare an outreach candidate for support chat launcher migration plan when every declared requirement is met.'
- `full-14-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'That choice belongs to the case the previous entry described, though the entry itself is not identified here.'
- `full-14-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'support-chat-launcher-schema-contract', 'audience': 'restricted-regions'}}`; content: 'For support chat launcher schema contract, the maintainer journal gives help menu as the value.'
- `full-14-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed support chat launcher authoring guidance value is help menu, according to the schema inspection.'
- `full-14-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The listed support chat launcher migration plan value is floating button, according to the test report.'

### Pair `full-14-p1-pair`

- Evaluated event: `full-14-p1-event`; context events: `full-14-p1-source`
- Candidate pool: `full-14-p1-pool`; hash: `6242e5da252c1901689c1c97071d0a1117c3428e85fca6746a7311458b601e61`; snapshots: `full-14-p1-snapshot-target, full-14-p1-snapshot-aux`
- Candidate snapshot: `full-14-p1-snapshot-target`; runtime item: `full-14-p1-runtime-target`; hash: `977f9eafe60496fd6c4ead397681e18866034e419ba119cf0ca4e77a27152797`
- Candidate source IDs: `full-14-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for support chat launcher runtime behavior is floating button.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-14-p1-source, full-14-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-14_1

#### Checkpoints and downstream tasks

- Checkpoint `full-14-p1-checkpoint` after sequence `9`
- Task `full-14-p1-state-task` (`current_state_query`) at `full-14-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for support chat launcher runtime behavior is floating button.', 'scope': {'system': 'support-chat-launcher-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-14-p1-source']}]}`; dependencies: `full-14-p1-source, full-14-p1-event`
- Task `full-14-p1-action-task` (`action_selection`) at `full-14-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-14-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-14-p1-source, full-14-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-14-p2-pair`

- Evaluated event: `full-14-p2-event`; context events: `full-14-p2-source`
- Candidate pool: `full-14-p2-pool`; hash: `445d27e3d6af3d1d7edfb8eb224f84635e31ab4236886739252018dbe6fd01f9`; snapshots: `full-14-p2-snapshot-target, full-14-p2-snapshot-aux`
- Candidate snapshot: `full-14-p2-snapshot-target`; runtime item: `full-14-p2-runtime-target`; hash: `8221d824360eaa101fff0e97ee19955369fbec92cffcfffd8782ae031e92f83f`
- Candidate source IDs: `full-14-p2-source`; counterevidence IDs: `none`
- Candidate proposition: Use floating button for support chat launcher schema contract across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p2:target`; new: `semantic:p2:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-14-p2-source, full-14-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-14_2

#### Checkpoints and downstream tasks

- Checkpoint `full-14-p2-checkpoint` after sequence `10`
- Task `full-14-p2-state-task` (`current_state_query`) at `full-14-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'Use floating button for support chat launcher schema contract across ordinary cases.', 'scope': {'system': 'support-chat-launcher-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-14-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:scoped', 'proposition': 'For support chat launcher schema contract, the maintainer journal gives help menu as the value.', 'scope': {'system': 'support-chat-launcher-schema-contract', 'audience': 'restricted-regions'}, 'status': 'active', 'evidence_ids': ['full-14-p2-event']}]}`; dependencies: `full-14-p2-source, full-14-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-14-p3-pair`

- Evaluated event: `full-14-p3-event`; context events: `full-14-p3-source`
- Candidate pool: `full-14-p3-pool`; hash: `5b2fddeb8a93e4ecb010652a833bc107d73a0c6a63a07f022d5ff1c838cafdc5`; snapshots: `full-14-p3-snapshot-target, full-14-p3-snapshot-aux`
- Candidate snapshot: `full-14-p3-snapshot-target`; runtime item: `full-14-p3-runtime-target`; hash: `dd00742d7ccc31025fca79465fc4de284daa3f47e65b770f59191ea2a714a718`
- Candidate source IDs: `full-14-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for support chat launcher authoring guidance is floating button.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-14-p3-source, full-14-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-14_3

#### Checkpoints and downstream tasks

- Checkpoint `full-14-p3-checkpoint` after sequence `11`
- Task `full-14-p3-state-task` (`current_state_query`) at `full-14-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The current value for support chat launcher authoring guidance is floating button.', 'scope': {'system': 'support-chat-launcher-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-14-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'The listed support chat launcher authoring guidance value is help menu, according to the schema inspection.', 'scope': {'system': 'support-chat-launcher-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-14-p3-event']}]}`; dependencies: `full-14-p3-source, full-14-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-14-p4-pair`

- Evaluated event: `full-14-p4-event`; context events: `full-14-p4-source, full-14-p4-aux`
- Candidate pool: `full-14-p4-pool`; hash: `9e090a431f75d4f4cf0325b8ddcad08179a3abd3dc5bfb2ba5919d0b897b0600`; snapshots: `full-14-p4-snapshot-target, full-14-p4-snapshot-aux`
- Candidate snapshot: `full-14-p4-snapshot-target`; runtime item: `full-14-p4-runtime-target`; hash: `e2e017667489c5bf45875f95eeca59e635b279211e977165d201556145229e66`
- Candidate source IDs: `full-14-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Provider H14 may satisfy the needs of support chat launcher migration plan.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `outreach_candidate`; action-selection task present: `true`
- Required evidence IDs: `full-14-p4-source, full-14-p4-aux, full-14-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-14_4

#### Checkpoints and downstream tasks

- Checkpoint `full-14-p4-checkpoint` after sequence `12`
- Task `full-14-p4-state-task` (`current_state_query`) at `full-14-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Provider H14 may satisfy the needs of support chat launcher migration plan.', 'scope': {'system': 'support-chat-launcher-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-14-p4-source', 'full-14-p4-event']}]}`; dependencies: `full-14-p4-source, full-14-p4-aux, full-14-p4-event`
- Task `full-14-p4-action-task` (`action_selection`) at `full-14-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-14-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'outreach_candidate'}`; dependencies: `full-14-p4-source, full-14-p4-aux, full-14-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-15 — surface-family-05

- Record: [`../development.jsonl` line 10](../development.jsonl#L10)
- Partition: `pilot_development`
### Timeline and authority

- `full-15-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The localization fallback runtime behavior uses English.'
- `full-15-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only localization fallback runtime behavior variant uses regional default within bilingual markets.'
- `full-15-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for localization fallback schema contract is English.'
- `full-15-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only localization fallback schema contract variant uses regional default within bilingual markets.'
- `full-15-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for localization fallback authoring guidance is English.'
- `full-15-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only localization fallback authoring guidance variant uses regional default within bilingual markets.'
- `full-15-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for localization fallback migration plan is English.'
- `full-15-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only localization fallback migration plan variant uses regional default within bilingual markets.'
- `full-15-p1-event` — seq 9; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'Late report, effective 2026-09-16: A staff update described road delays near the office after overnight construction.'
- `full-15-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The ownership record reports that localization fallback schema contract uses regional default.'
- `full-15-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'For localization fallback authoring guidance, the maintainer journal gives English as the value.'
- `full-15-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'For localization fallback migration plan, the schema inspection gives regional default as the value.'

### Pair `full-15-p1-pair`

- Evaluated event: `full-15-p1-event`; context events: `full-15-p1-source`
- Candidate pool: `full-15-p1-pool`; hash: `96980efba512c79bc615ede978dd92788bfdb95a6dc68c08ce2653bbd14e45e2`; snapshots: `full-15-p1-snapshot-target, full-15-p1-snapshot-aux`
- Candidate snapshot: `full-15-p1-snapshot-target`; runtime item: `full-15-p1-runtime-target`; hash: `927244bcaa4db0d8d319b4fb762c7a7d074eab459f4bf1d816dbdf3d6c4509f5`
- Candidate source IDs: `full-15-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The localization fallback runtime behavior uses English.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-15-p1-source, full-15-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-15_1

#### Checkpoints and downstream tasks

- Checkpoint `full-15-p1-checkpoint` after sequence `9`
- Task `full-15-p1-state-task` (`current_state_query`) at `full-15-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The localization fallback runtime behavior uses English.', 'scope': {'system': 'localization-fallback-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-15-p1-source']}]}`; dependencies: `full-15-p1-source, full-15-p1-event`
- Task `full-15-p1-action-task` (`action_selection`) at `full-15-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-15-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-15-p1-source, full-15-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-15-p2-pair`

- Evaluated event: `full-15-p2-event`; context events: `full-15-p2-source`
- Candidate pool: `full-15-p2-pool`; hash: `b48243d9b61bfa2f69a9e08727a0f3b6f2095922c4255e4cb4477d1fb11434c9`; snapshots: `full-15-p2-snapshot-target, full-15-p2-snapshot-aux`
- Candidate snapshot: `full-15-p2-snapshot-target`; runtime item: `full-15-p2-runtime-target`; hash: `a7238ff284e0c53fd88d08eb96932105ada3f27615a939cab2f2e2710bbda4b6`
- Candidate source IDs: `full-15-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for localization fallback schema contract is English.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-15-p2-source, full-15-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-15_2

#### Checkpoints and downstream tasks

- Checkpoint `full-15-p2-checkpoint` after sequence `10`
- Task `full-15-p2-state-task` (`current_state_query`) at `full-15-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The current value for localization fallback schema contract is English.', 'scope': {'system': 'localization-fallback-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-15-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The ownership record reports that localization fallback schema contract uses regional default.', 'scope': {'system': 'localization-fallback-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-15-p2-event']}]}`; dependencies: `full-15-p2-source, full-15-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-15-p3-pair`

- Evaluated event: `full-15-p3-event`; context events: `full-15-p3-source`
- Candidate pool: `full-15-p3-pool`; hash: `f9aaad4b2147cd39ab666bcd2fdb08fb7e4b1c0f59bda72fca4d1b0c8cb6ee31`; snapshots: `full-15-p3-snapshot-target, full-15-p3-snapshot-aux`
- Candidate snapshot: `full-15-p3-snapshot-target`; runtime item: `full-15-p3-runtime-target`; hash: `524de0cdfe476638abbf478547cdc85b650647915f084d75a419d5252f1a076c`
- Candidate source IDs: `full-15-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for localization fallback authoring guidance is English.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-15-p3-source, full-15-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-15_3

#### Checkpoints and downstream tasks

- Checkpoint `full-15-p3-checkpoint` after sequence `11`
- Task `full-15-p3-state-task` (`current_state_query`) at `full-15-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The accepted preference for localization fallback authoring guidance is English.', 'scope': {'system': 'localization-fallback-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-15-p3-source', 'full-15-p3-event']}]}`; dependencies: `full-15-p3-source, full-15-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-15-p4-pair`

- Evaluated event: `full-15-p4-event`; context events: `full-15-p4-source`
- Candidate pool: `full-15-p4-pool`; hash: `65434979595d708bbbd56dcececc4dc15816777902d693973d891433858f038d`; snapshots: `full-15-p4-snapshot-target, full-15-p4-snapshot-aux`
- Candidate snapshot: `full-15-p4-snapshot-target`; runtime item: `full-15-p4-runtime-target`; hash: `830e564c5f5669dd710a783177f63dfde539248137135e16e5fc1d16781b5ced`
- Candidate source IDs: `full-15-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for localization fallback migration plan is English.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p4:target`; new: `semantic:p4:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-15-p4-source, full-15-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-15_4

#### Checkpoints and downstream tasks

- Checkpoint `full-15-p4-checkpoint` after sequence `12`
- Task `full-15-p4-state-task` (`current_state_query`) at `full-15-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for localization fallback migration plan is English.', 'scope': {'system': 'localization-fallback-migration-plan', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-15-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:replacement', 'proposition': 'For localization fallback migration plan, the schema inspection gives regional default as the value.', 'scope': {'system': 'localization-fallback-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-15-p4-event']}]}`; dependencies: `full-15-p4-source, full-15-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-16 — surface-family-06

- Record: [`../development.jsonl` line 11](../development.jsonl#L11)
- Partition: `pilot_development`
### Timeline and authority

- `full-16-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for receipt renderer runtime behavior is HTML template.'
- `full-16-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only receipt renderer runtime behavior variant uses native layout within offline receipts.'
- `full-16-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for receipt renderer schema contract is HTML template.'
- `full-16-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only receipt renderer schema contract variant uses native layout within offline receipts.'
- `full-16-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for receipt renderer authoring guidance is HTML template.'
- `full-16-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only receipt renderer authoring guidance variant uses native layout within offline receipts.'
- `full-16-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use HTML template for receipt renderer migration plan across ordinary cases.'
- `full-16-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only receipt renderer migration plan variant uses native layout within offline receipts.'
- `full-16-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The migration review reports that receipt renderer runtime behavior uses HTML template.'
- `full-16-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The incident follow-up reports that receipt renderer schema contract uses HTML template.'
- `full-16-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'That choice belongs to the case the previous entry described, though the entry itself is not identified here.'
- `full-16-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'receipt-renderer-migration-plan', 'audience': 'offline-receipts'}}`; content: 'For receipt renderer migration plan, the maintainer journal gives native layout as the value.'

### Pair `full-16-p1-pair`

- Evaluated event: `full-16-p1-event`; context events: `full-16-p1-source`
- Candidate pool: `full-16-p1-pool`; hash: `b93ff6d4032970adf7f4f6b56fefcb3d3ec12ff598bc8e189d9a8afe31fa13fd`; snapshots: `full-16-p1-snapshot-target, full-16-p1-snapshot-aux`
- Candidate snapshot: `full-16-p1-snapshot-target`; runtime item: `full-16-p1-runtime-target`; hash: `daeaa669fec34e87e95987e12b18250b01d069e0f24ae486a14121f27dddb3ad`
- Candidate source IDs: `full-16-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for receipt renderer runtime behavior is HTML template.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-16-p1-source, full-16-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-16_1

#### Checkpoints and downstream tasks

- Checkpoint `full-16-p1-checkpoint` after sequence `9`
- Task `full-16-p1-state-task` (`current_state_query`) at `full-16-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for receipt renderer runtime behavior is HTML template.', 'scope': {'system': 'receipt-renderer-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-16-p1-source', 'full-16-p1-event']}]}`; dependencies: `full-16-p1-source, full-16-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-16-p2-pair`

- Evaluated event: `full-16-p2-event`; context events: `full-16-p2-source`
- Candidate pool: `full-16-p2-pool`; hash: `e80681c92e5b4a7df213baefe2623e5cc3bcfd85b88a446cbbaeb54353962a90`; snapshots: `full-16-p2-snapshot-target, full-16-p2-snapshot-aux`
- Candidate snapshot: `full-16-p2-snapshot-target`; runtime item: `full-16-p2-runtime-target`; hash: `6bae82fd810d47bff0a0adb0752518862fad5a72baf026ce18abb6f213a52fce`
- Candidate source IDs: `full-16-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for receipt renderer schema contract is HTML template.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-16-p2-source, full-16-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-16_2

#### Checkpoints and downstream tasks

- Checkpoint `full-16-p2-checkpoint` after sequence `10`
- Task `full-16-p2-state-task` (`current_state_query`) at `full-16-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The accepted preference for receipt renderer schema contract is HTML template.', 'scope': {'system': 'receipt-renderer-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-16-p2-source', 'full-16-p2-event']}]}`; dependencies: `full-16-p2-source, full-16-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-16-p3-pair`

- Evaluated event: `full-16-p3-event`; context events: `full-16-p3-source`
- Candidate pool: `full-16-p3-pool`; hash: `963f731bad1913986fe4413d3d951c3a6ec1e710f6b6a7bc0947068fbff0d2e9`; snapshots: `full-16-p3-snapshot-target, full-16-p3-snapshot-aux`
- Candidate snapshot: `full-16-p3-snapshot-target`; runtime item: `full-16-p3-runtime-target`; hash: `d3f64984edef7703a6a875579fb9fd262a37ae3d69682f6535648268d9e787bb`
- Candidate source IDs: `full-16-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for receipt renderer authoring guidance is HTML template.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-16-p3-source, full-16-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-16_3

#### Checkpoints and downstream tasks

- Checkpoint `full-16-p3-checkpoint` after sequence `11`
- Task `full-16-p3-state-task` (`current_state_query`) at `full-16-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for receipt renderer authoring guidance is HTML template.', 'scope': {'system': 'receipt-renderer-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-16-p3-source']}]}`; dependencies: `full-16-p3-source, full-16-p3-event`
- Task `full-16-p3-action-task` (`action_selection`) at `full-16-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-16-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-16-p3-source, full-16-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-16-p4-pair`

- Evaluated event: `full-16-p4-event`; context events: `full-16-p4-source`
- Candidate pool: `full-16-p4-pool`; hash: `658c397ad2fbdc8b3e4ce9f7ca0ce9c95ff5c149a7cf9b12e0bf05e75611535e`; snapshots: `full-16-p4-snapshot-target, full-16-p4-snapshot-aux`
- Candidate snapshot: `full-16-p4-snapshot-target`; runtime item: `full-16-p4-runtime-target`; hash: `53634141829014b119902f689f700462340778b5ebcd8dfd8c069b7c5c121313`
- Candidate source IDs: `full-16-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use HTML template for receipt renderer migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-16-p4-source, full-16-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-16_4

#### Checkpoints and downstream tasks

- Checkpoint `full-16-p4-checkpoint` after sequence `12`
- Task `full-16-p4-state-task` (`current_state_query`) at `full-16-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use HTML template for receipt renderer migration plan across ordinary cases.', 'scope': {'system': 'receipt-renderer-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-16-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'For receipt renderer migration plan, the maintainer journal gives native layout as the value.', 'scope': {'system': 'receipt-renderer-migration-plan', 'audience': 'offline-receipts'}, 'status': 'active', 'evidence_ids': ['full-16-p4-event']}]}`; dependencies: `full-16-p4-source, full-16-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-17 — surface-family-07

- Record: [`../development.jsonl` line 12](../development.jsonl#L12)
- Partition: `pilot_development`
### Timeline and authority

- `full-17-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for inventory badge runtime behavior is numeric count.'
- `full-17-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only inventory badge runtime behavior variant uses availability label within limited releases.'
- `full-17-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to review inventory badge schema contract before 09:00 UTC.'
- `full-17-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only inventory badge schema contract variant uses availability label within limited releases.'
- `full-17-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for inventory badge authoring guidance is numeric count.'
- `full-17-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Validation policy requires investigation of an authorized transition whose validity interval ends before it begins.'
- `full-17-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for inventory badge migration plan is numeric count.'
- `full-17-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only inventory badge migration plan variant uses availability label within limited releases.'
- `full-17-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-17-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `evaluator`; type `time_advance`; assert `false`; transition `true`; reason: evaluator clock event for lifecycle evaluation only; deletion targets: `none`; metadata: `{'advance_to': '2026-09-18T10:00:00Z'}`; content: None
- `full-17-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'valid_from': '2026-10-01T00:00:00Z', 'valid_until': '2026-09-01T00:00:00Z'}`; content: 'The listed inventory badge authoring guidance value is numeric count, according to the incident follow-up.'
- `full-17-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'

### Pair `full-17-p1-pair`

- Evaluated event: `full-17-p1-event`; context events: `full-17-p1-source`
- Candidate pool: `full-17-p1-pool`; hash: `0de2203c319bd72054ed6eabbb704656b57a2c57544177bc01163e5c25c5e57a`; snapshots: `full-17-p1-snapshot-target, full-17-p1-snapshot-aux`
- Candidate snapshot: `full-17-p1-snapshot-target`; runtime item: `full-17-p1-runtime-target`; hash: `46ad1cc4c4102d1989d4d40264fbafb49bd2298c4e55a131aa7d192ee19d3a4a`
- Candidate source IDs: `full-17-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for inventory badge runtime behavior is numeric count.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-17-p1-source, full-17-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-17_1

#### Checkpoints and downstream tasks

- Checkpoint `full-17-p1-checkpoint` after sequence `9`
- Task `full-17-p1-state-task` (`current_state_query`) at `full-17-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for inventory badge runtime behavior is numeric count.', 'scope': {'system': 'inventory-badge-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-17-p1-source']}]}`; dependencies: `full-17-p1-source, full-17-p1-event`
- Task `full-17-p1-action-task` (`action_selection`) at `full-17-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-17-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-17-p1-source, full-17-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-17-p2-pair`

- Evaluated event: `full-17-p2-event`; context events: `full-17-p2-source`
- Candidate pool: `full-17-p2-pool`; hash: `59fbbc15a0d3c17077907fe4d63e66d2c07c37490d6d85b1035cefa7b70ad3ca`; snapshots: `full-17-p2-snapshot-target, full-17-p2-snapshot-aux`
- Candidate snapshot: `full-17-p2-snapshot-target`; runtime item: `full-17-p2-runtime-target`; hash: `6b460931cb1c9f6349c3041b5fbea145311602555c9e2cbc5965a65ff5ddb614`
- Candidate source IDs: `full-17-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to review inventory badge schema contract before 09:00 UTC.
- Candidate validity: `2026-09-17T12:00:00Z` through `2026-09-18T09:00:00Z`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `expire`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-17-p2-source, full-17-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-17_2

#### Checkpoints and downstream tasks

- Checkpoint `full-17-p2-checkpoint` after sequence `10`
- Task `full-17-p2-state-task` (`commitment_query`) at `full-17-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The team committed to review inventory badge schema contract before 09:00 UTC.', 'scope': {'system': 'inventory-badge-schema-contract', 'audience': 'all'}, 'status': 'expired', 'evidence_ids': ['full-17-p2-source']}]}`; dependencies: `full-17-p2-source, full-17-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-17-p3-pair`

- Evaluated event: `full-17-p3-event`; context events: `full-17-p3-source, full-17-p3-aux`
- Candidate pool: `full-17-p3-pool`; hash: `eb73dfd89bacd9ef0acae1fc5fa01b5d9a31198c12388b1c35602a079d23bc04`; snapshots: `full-17-p3-snapshot-target, full-17-p3-snapshot-aux`
- Candidate snapshot: `full-17-p3-snapshot-target`; runtime item: `full-17-p3-runtime-target`; hash: `58061882a756914d54c1104bed336ea80985fac1a24c7952205a3fee2af3407b`
- Candidate source IDs: `full-17-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for inventory badge authoring guidance is numeric count.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `reject_invalid`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `investigate`; action-selection task present: `true`
- Required evidence IDs: `full-17-p3-source, full-17-p3-aux, full-17-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-17_3

#### Checkpoints and downstream tasks

- Checkpoint `full-17-p3-checkpoint` after sequence `11`
- Task `full-17-p3-state-task` (`current_state_query`) at `full-17-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The accepted preference for inventory badge authoring guidance is numeric count.', 'scope': {'system': 'inventory-badge-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-17-p3-source']}]}`; dependencies: `full-17-p3-source, full-17-p3-aux, full-17-p3-event`
- Task `full-17-p3-action-task` (`action_selection`) at `full-17-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-17-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'investigate'}`; dependencies: `full-17-p3-source, full-17-p3-aux, full-17-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-17-p4-pair`

- Evaluated event: `full-17-p4-event`; context events: `full-17-p4-source`
- Candidate pool: `full-17-p4-pool`; hash: `3480275e2e94d1e21eef8dedaccbe18b2bec7276e9050e6fdc7d5a902cd6e9d5`; snapshots: `full-17-p4-snapshot-target, full-17-p4-snapshot-aux`
- Candidate snapshot: `full-17-p4-snapshot-target`; runtime item: `full-17-p4-runtime-target`; hash: `1ad8f92c213de90d4f3323f131128a0232f12fc14c4d9b576bc5a88676a563ef`
- Candidate source IDs: `full-17-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for inventory badge migration plan is numeric count.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-17-p4-source, full-17-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-17_4

#### Checkpoints and downstream tasks

- Checkpoint `full-17-p4-checkpoint` after sequence `12`
- Task `full-17-p4-state-task` (`current_state_query`) at `full-17-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for inventory badge migration plan is numeric count.', 'scope': {'system': 'inventory-badge-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-17-p4-source']}]}`; dependencies: `full-17-p4-source, full-17-p4-event`
- Task `full-17-p4-action-task` (`action_selection`) at `full-17-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-17-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-17-p4-source, full-17-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-18 — surface-family-08

- Record: [`../development.jsonl` line 13](../development.jsonl#L13)
- Partition: `pilot_development`
### Timeline and authority

- `full-18-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use plain text for review composer runtime behavior across ordinary cases.'
- `full-18-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only review composer runtime behavior variant uses structured fields within verified purchases.'
- `full-18-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Provider H18 may satisfy the needs of review composer schema contract.'
- `full-18-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The user has an active approved goal to prepare an outreach candidate for review composer schema contract when every declared requirement is met.'
- `full-18-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change review composer authoring guidance to structured fields.'
- `full-18-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only review composer authoring guidance variant uses structured fields within verified purchases.'
- `full-18-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use plain text for review composer migration plan across ordinary cases.'
- `full-18-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only review composer migration plan variant uses structured fields within verified purchases.'
- `full-18-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'review-composer-runtime-behavior', 'audience': 'verified-purchases'}}`; content: 'The architecture note records structured fields for review composer runtime behavior.'
- `full-18-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The compatibility review reports that review composer schema contract uses plain text.'
- `full-18-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed review composer authoring guidance value is structured fields, according to the migration review.'
- `full-18-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'review-composer-migration-plan', 'audience': 'verified-purchases'}}`; content: 'The incident follow-up reports that review composer migration plan uses structured fields.'

### Pair `full-18-p1-pair`

- Evaluated event: `full-18-p1-event`; context events: `full-18-p1-source`
- Candidate pool: `full-18-p1-pool`; hash: `caea6e4e4a016074614e6708ef79be4f6efa757a12d84946b25522b5af950a09`; snapshots: `full-18-p1-snapshot-target, full-18-p1-snapshot-aux`
- Candidate snapshot: `full-18-p1-snapshot-target`; runtime item: `full-18-p1-runtime-target`; hash: `31a855f1edf65b30f559a2a2f1406fdf1cfd00e69d7cde95b1d7654c8df266cc`
- Candidate source IDs: `full-18-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use plain text for review composer runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-18-p1-source, full-18-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-18_1

#### Checkpoints and downstream tasks

- Checkpoint `full-18-p1-checkpoint` after sequence `9`
- Task `full-18-p1-state-task` (`current_state_query`) at `full-18-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use plain text for review composer runtime behavior across ordinary cases.', 'scope': {'system': 'review-composer-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-18-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'The architecture note records structured fields for review composer runtime behavior.', 'scope': {'system': 'review-composer-runtime-behavior', 'audience': 'verified-purchases'}, 'status': 'active', 'evidence_ids': ['full-18-p1-event']}]}`; dependencies: `full-18-p1-source, full-18-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-18-p2-pair`

- Evaluated event: `full-18-p2-event`; context events: `full-18-p2-source, full-18-p2-aux`
- Candidate pool: `full-18-p2-pool`; hash: `adb2e659c1d7685bd34110a5fa04889ae706fd075b7bcea05fc659425a00b182`; snapshots: `full-18-p2-snapshot-target, full-18-p2-snapshot-aux`
- Candidate snapshot: `full-18-p2-snapshot-target`; runtime item: `full-18-p2-runtime-target`; hash: `ac5c34b6acae811fd64448fadc9053a4fe08f7ae7d7a441e59d4ca2e059201b8`
- Candidate source IDs: `full-18-p2-source`; counterevidence IDs: `none`
- Candidate proposition: Provider H18 may satisfy the needs of review composer schema contract.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `outreach_candidate`; action-selection task present: `true`
- Required evidence IDs: `full-18-p2-source, full-18-p2-aux, full-18-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-18_2

#### Checkpoints and downstream tasks

- Checkpoint `full-18-p2-checkpoint` after sequence `10`
- Task `full-18-p2-state-task` (`current_state_query`) at `full-18-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'Provider H18 may satisfy the needs of review composer schema contract.', 'scope': {'system': 'review-composer-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-18-p2-source', 'full-18-p2-event']}]}`; dependencies: `full-18-p2-source, full-18-p2-aux, full-18-p2-event`
- Task `full-18-p2-action-task` (`action_selection`) at `full-18-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-18-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'outreach_candidate'}`; dependencies: `full-18-p2-source, full-18-p2-aux, full-18-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-18-p3-pair`

- Evaluated event: `full-18-p3-event`; context events: `full-18-p3-source`
- Candidate pool: `full-18-p3-pool`; hash: `61d3401696a7aad53537dede8cfcb752a240f8407dfc2959ecf460416ce60fa5`; snapshots: `full-18-p3-snapshot-target, full-18-p3-snapshot-aux`
- Candidate snapshot: `full-18-p3-snapshot-target`; runtime item: `full-18-p3-runtime-target`; hash: `b501c1aa6311189f0dcbfb152c77b5c4c193349e2a6b5b3a37f7c3c2964fd62a`
- Candidate source IDs: `full-18-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change review composer authoring guidance to structured fields.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-18-p3-source, full-18-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-18_3

#### Checkpoints and downstream tasks

- Checkpoint `full-18-p3-checkpoint` after sequence `11`
- Task `full-18-p3-state-task` (`commitment_query`) at `full-18-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The team committed to change review composer authoring guidance to structured fields.', 'scope': {'system': 'review-composer-authoring-guidance', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-18-p3-source', 'full-18-p3-event']}]}`; dependencies: `full-18-p3-source, full-18-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-18-p4-pair`

- Evaluated event: `full-18-p4-event`; context events: `full-18-p4-source`
- Candidate pool: `full-18-p4-pool`; hash: `4e7428e18265963034bc66a1a16305a3d7d36eb58d72d6b9c8f3535483fad393`; snapshots: `full-18-p4-snapshot-target, full-18-p4-snapshot-aux`
- Candidate snapshot: `full-18-p4-snapshot-target`; runtime item: `full-18-p4-runtime-target`; hash: `9f69590e7ff71aa33308d1a3806cbae860bea774f93ba4ab303cf2605ac67328`
- Candidate source IDs: `full-18-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use plain text for review composer migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-18-p4-source, full-18-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-18_4

#### Checkpoints and downstream tasks

- Checkpoint `full-18-p4-checkpoint` after sequence `12`
- Task `full-18-p4-state-task` (`current_state_query`) at `full-18-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use plain text for review composer migration plan across ordinary cases.', 'scope': {'system': 'review-composer-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-18-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'The incident follow-up reports that review composer migration plan uses structured fields.', 'scope': {'system': 'review-composer-migration-plan', 'audience': 'verified-purchases'}, 'status': 'active', 'evidence_ids': ['full-18-p4-event']}]}`; dependencies: `full-18-p4-source, full-18-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-19 — surface-family-09

- Record: [`../development.jsonl` line 14](../development.jsonl#L14)
- Partition: `pilot_development`
### Timeline and authority

- `full-19-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for recommendation rail runtime behavior is recent views.'
- `full-19-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only recommendation rail runtime behavior variant uses session intent within new visitors.'
- `full-19-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for recommendation rail schema contract is recent views.'
- `full-19-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only recommendation rail schema contract variant uses session intent within new visitors.'
- `full-19-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for recommendation rail authoring guidance is recent views.'
- `full-19-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only recommendation rail authoring guidance variant uses session intent within new visitors.'
- `full-19-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for recommendation rail migration plan is recent views.'
- `full-19-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only recommendation rail migration plan variant uses session intent within new visitors.'
- `full-19-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The release checklist records recent views for recommendation rail runtime behavior.'
- `full-19-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The selected arrangement depends on which request is meant; the current note gives no distinguishing detail.'
- `full-19-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-19-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The migration review records session intent for recommendation rail migration plan.'

### Pair `full-19-p1-pair`

- Evaluated event: `full-19-p1-event`; context events: `full-19-p1-source`
- Candidate pool: `full-19-p1-pool`; hash: `7b7ba60fc015e9c297285a84ead73cf1351da0ea653b9f4b7b5819bb2310944f`; snapshots: `full-19-p1-snapshot-target, full-19-p1-snapshot-aux`
- Candidate snapshot: `full-19-p1-snapshot-target`; runtime item: `full-19-p1-runtime-target`; hash: `b04b07ea8523634613d4c8016d9b0454d3fb30884a8252b82aa7b9931bc08b66`
- Candidate source IDs: `full-19-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for recommendation rail runtime behavior is recent views.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-19-p1-source, full-19-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-19_1

#### Checkpoints and downstream tasks

- Checkpoint `full-19-p1-checkpoint` after sequence `9`
- Task `full-19-p1-state-task` (`current_state_query`) at `full-19-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for recommendation rail runtime behavior is recent views.', 'scope': {'system': 'recommendation-rail-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-19-p1-source', 'full-19-p1-event']}]}`; dependencies: `full-19-p1-source, full-19-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-19-p2-pair`

- Evaluated event: `full-19-p2-event`; context events: `full-19-p2-source`
- Candidate pool: `full-19-p2-pool`; hash: `796d020805c9d8ebcb1e58d382d17a159001a5ec3991093539ac830a800eb4af`; snapshots: `full-19-p2-snapshot-target, full-19-p2-snapshot-aux`
- Candidate snapshot: `full-19-p2-snapshot-target`; runtime item: `full-19-p2-runtime-target`; hash: `bd0bb6ce72681911cab2297260e56164a905bcc947ccc263cd36d40ba6ae9814`
- Candidate source IDs: `full-19-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for recommendation rail schema contract is recent views.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-19-p2-source, full-19-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-19_2

#### Checkpoints and downstream tasks

- Checkpoint `full-19-p2-checkpoint` after sequence `10`
- Task `full-19-p2-state-task` (`current_state_query`) at `full-19-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for recommendation rail schema contract is recent views.', 'scope': {'system': 'recommendation-rail-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-19-p2-source']}]}`; dependencies: `full-19-p2-source, full-19-p2-event`
- Task `full-19-p2-action-task` (`action_selection`) at `full-19-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-19-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-19-p2-source, full-19-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-19-p3-pair`

- Evaluated event: `full-19-p3-event`; context events: `full-19-p3-source`
- Candidate pool: `full-19-p3-pool`; hash: `06beb01c0ef9786060ea9b51c4507c275356ec454182ee072deedf1c3e1aff97`; snapshots: `full-19-p3-snapshot-target, full-19-p3-snapshot-aux`
- Candidate snapshot: `full-19-p3-snapshot-target`; runtime item: `full-19-p3-runtime-target`; hash: `dc09019d70892dd3c600a403668a7faf17e4cf2247fefbf1d1b786b7fb32f789`
- Candidate source IDs: `full-19-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for recommendation rail authoring guidance is recent views.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-19-p3-source, full-19-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-19_3

#### Checkpoints and downstream tasks

- Checkpoint `full-19-p3-checkpoint` after sequence `11`
- Task `full-19-p3-state-task` (`current_state_query`) at `full-19-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for recommendation rail authoring guidance is recent views.', 'scope': {'system': 'recommendation-rail-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-19-p3-source']}]}`; dependencies: `full-19-p3-source, full-19-p3-event`
- Task `full-19-p3-action-task` (`action_selection`) at `full-19-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-19-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-19-p3-source, full-19-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-19-p4-pair`

- Evaluated event: `full-19-p4-event`; context events: `full-19-p4-source`
- Candidate pool: `full-19-p4-pool`; hash: `cae082d018873eef20dc3319e1d92ba3964de165c12c1e79074cde4dd1d3f16b`; snapshots: `full-19-p4-snapshot-target, full-19-p4-snapshot-aux`
- Candidate snapshot: `full-19-p4-snapshot-target`; runtime item: `full-19-p4-runtime-target`; hash: `38f8c5b0d8cf6e19611bd2caa1e6f64294b98b653416ff11fe6f0a44c09fffb4`
- Candidate source IDs: `full-19-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for recommendation rail migration plan is recent views.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p4:target`; new: `semantic:p4:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-19-p4-source, full-19-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-19_4

#### Checkpoints and downstream tasks

- Checkpoint `full-19-p4-checkpoint` after sequence `12`
- Task `full-19-p4-state-task` (`current_state_query`) at `full-19-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The current value for recommendation rail migration plan is recent views.', 'scope': {'system': 'recommendation-rail-migration-plan', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-19-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:replacement', 'proposition': 'The migration review records session intent for recommendation rail migration plan.', 'scope': {'system': 'recommendation-rail-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-19-p4-event']}]}`; dependencies: `full-19-p4-source, full-19-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-20 — surface-family-10

- Record: [`../holdout.jsonl` line 6](../holdout.jsonl#L6)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-20-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for authentication session runtime behavior is thirty days.'
- `full-20-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only authentication session runtime behavior variant uses seven days within shared devices.'
- `full-20-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for authentication session schema contract is thirty days.'
- `full-20-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only authentication session schema contract variant uses seven days within shared devices.'
- `full-20-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for authentication session authoring guidance is thirty days.'
- `full-20-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only authentication session authoring guidance variant uses seven days within shared devices.'
- `full-20-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use thirty days for authentication session migration plan across ordinary cases.'
- `full-20-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only authentication session migration plan variant uses seven days within shared devices.'
- `full-20-p1-event` — seq 9; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'Late report, effective 2026-09-16: A setting is referenced for one situation, but neither the situation nor its value is named in context.'
- `full-20-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The release checklist records thirty days for authentication session schema contract.'
- `full-20-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'For authentication session authoring guidance, the architecture note gives thirty days as the value.'
- `full-20-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'authentication-session-migration-plan', 'audience': 'shared-devices'}}`; content: 'For authentication session migration plan, the compatibility review gives seven days as the value.'

### Pair `full-20-p1-pair`

- Evaluated event: `full-20-p1-event`; context events: `full-20-p1-source`
- Candidate pool: `full-20-p1-pool`; hash: `730a7474a83c7162fb690e3ed48bdb7e2507ede95a81b310efa0052cf131412d`; snapshots: `full-20-p1-snapshot-target, full-20-p1-snapshot-aux`
- Candidate snapshot: `full-20-p1-snapshot-target`; runtime item: `full-20-p1-runtime-target`; hash: `238bdf0e4475151327a9426fba73756fda8c64dbf4cf0cf26b99f751560a1028`
- Candidate source IDs: `full-20-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for authentication session runtime behavior is thirty days.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-20-p1-source, full-20-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-20_1

#### Checkpoints and downstream tasks

- Checkpoint `full-20-p1-checkpoint` after sequence `9`
- Task `full-20-p1-state-task` (`current_state_query`) at `full-20-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for authentication session runtime behavior is thirty days.', 'scope': {'system': 'authentication-session-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-20-p1-source']}]}`; dependencies: `full-20-p1-source, full-20-p1-event`
- Task `full-20-p1-action-task` (`action_selection`) at `full-20-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-20-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-20-p1-source, full-20-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-20-p2-pair`

- Evaluated event: `full-20-p2-event`; context events: `full-20-p2-source`
- Candidate pool: `full-20-p2-pool`; hash: `98277d07e1277c76e138d3ed5e26fba4eedf55e3611b15c05044e30ab7e611e7`; snapshots: `full-20-p2-snapshot-target, full-20-p2-snapshot-aux`
- Candidate snapshot: `full-20-p2-snapshot-target`; runtime item: `full-20-p2-runtime-target`; hash: `5e6f0a2d70e694a18938555b18c9b710643ba2aff25078c1d89341f80e6fe278`
- Candidate source IDs: `full-20-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for authentication session schema contract is thirty days.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-20-p2-source, full-20-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-20_2

#### Checkpoints and downstream tasks

- Checkpoint `full-20-p2-checkpoint` after sequence `10`
- Task `full-20-p2-state-task` (`current_state_query`) at `full-20-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The accepted preference for authentication session schema contract is thirty days.', 'scope': {'system': 'authentication-session-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-20-p2-source', 'full-20-p2-event']}]}`; dependencies: `full-20-p2-source, full-20-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-20-p3-pair`

- Evaluated event: `full-20-p3-event`; context events: `full-20-p3-source`
- Candidate pool: `full-20-p3-pool`; hash: `bb16dcdf085d1f88e6a132194c670472cfcc0c1eb8e6de572537e1b2141f6c13`; snapshots: `full-20-p3-snapshot-target, full-20-p3-snapshot-aux`
- Candidate snapshot: `full-20-p3-snapshot-target`; runtime item: `full-20-p3-runtime-target`; hash: `f4167ab638767a116a97fd2bed10419b62adf73a3d6da5d17b4239ff2df787a7`
- Candidate source IDs: `full-20-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for authentication session authoring guidance is thirty days.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-20-p3-source, full-20-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-20_3

#### Checkpoints and downstream tasks

- Checkpoint `full-20-p3-checkpoint` after sequence `11`
- Task `full-20-p3-state-task` (`current_state_query`) at `full-20-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The accepted preference for authentication session authoring guidance is thirty days.', 'scope': {'system': 'authentication-session-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-20-p3-source', 'full-20-p3-event']}]}`; dependencies: `full-20-p3-source, full-20-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-20-p4-pair`

- Evaluated event: `full-20-p4-event`; context events: `full-20-p4-source`
- Candidate pool: `full-20-p4-pool`; hash: `5295b14a92defd6041233e12ff734165b0ee984e498ca4ead66cd394e5dc8066`; snapshots: `full-20-p4-snapshot-target, full-20-p4-snapshot-aux`
- Candidate snapshot: `full-20-p4-snapshot-target`; runtime item: `full-20-p4-runtime-target`; hash: `ac06fd3451e402d9267a146f01609b33bc3d9c2e8139274e9dbb7b18ba76fcb0`
- Candidate source IDs: `full-20-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use thirty days for authentication session migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-20-p4-source, full-20-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-20_4

#### Checkpoints and downstream tasks

- Checkpoint `full-20-p4-checkpoint` after sequence `12`
- Task `full-20-p4-state-task` (`current_state_query`) at `full-20-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use thirty days for authentication session migration plan across ordinary cases.', 'scope': {'system': 'authentication-session-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-20-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'For authentication session migration plan, the compatibility review gives seven days as the value.', 'scope': {'system': 'authentication-session-migration-plan', 'audience': 'shared-devices'}, 'status': 'active', 'evidence_ids': ['full-20-p4-event']}]}`; dependencies: `full-20-p4-source, full-20-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-21 — surface-family-01

- Record: [`../holdout.jsonl` line 7](../holdout.jsonl#L7)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-21-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use path matching for deep-link router runtime behavior across ordinary cases.'
- `full-21-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only deep-link router runtime behavior variant uses typed routes within legacy links.'
- `full-21-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for deep-link router schema contract is path matching.'
- `full-21-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Validation policy requires investigation of an authorized transition whose validity interval ends before it begins.'
- `full-21-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The deep-link router authoring guidance uses path matching.'
- `full-21-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only deep-link router authoring guidance variant uses typed routes within legacy links.'
- `full-21-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for deep-link router migration plan is path matching.'
- `full-21-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only deep-link router migration plan variant uses typed routes within legacy links.'
- `full-21-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'deep-link-router-runtime-behavior', 'audience': 'legacy-links'}}`; content: 'The test report reports that deep-link router runtime behavior uses typed routes.'
- `full-21-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'valid_from': '2026-10-01T00:00:00Z', 'valid_until': '2026-09-01T00:00:00Z'}`; content: 'For deep-link router schema contract, the registry audit gives path matching as the value.'
- `full-21-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-21-p3-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-21-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The instruction points back to an earlier example without making clear which example should govern this request.'

### Pair `full-21-p1-pair`

- Evaluated event: `full-21-p1-event`; context events: `full-21-p1-source`
- Candidate pool: `full-21-p1-pool`; hash: `06c6957e6fe2b1e5b548c9b928c38cdc1c85c56e9cf6ad6277ac2262ff309102`; snapshots: `full-21-p1-snapshot-target, full-21-p1-snapshot-aux`
- Candidate snapshot: `full-21-p1-snapshot-target`; runtime item: `full-21-p1-runtime-target`; hash: `ee4c37d170cb4c93173f9a16d07a14af3cafc9da4c5ebf760f76e9fb69a38f92`
- Candidate source IDs: `full-21-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use path matching for deep-link router runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-21-p1-source, full-21-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-21_1

#### Checkpoints and downstream tasks

- Checkpoint `full-21-p1-checkpoint` after sequence `9`
- Task `full-21-p1-state-task` (`current_state_query`) at `full-21-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use path matching for deep-link router runtime behavior across ordinary cases.', 'scope': {'system': 'deep-link-router-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-21-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'The test report reports that deep-link router runtime behavior uses typed routes.', 'scope': {'system': 'deep-link-router-runtime-behavior', 'audience': 'legacy-links'}, 'status': 'active', 'evidence_ids': ['full-21-p1-event']}]}`; dependencies: `full-21-p1-source, full-21-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-21-p2-pair`

- Evaluated event: `full-21-p2-event`; context events: `full-21-p2-source, full-21-p2-aux`
- Candidate pool: `full-21-p2-pool`; hash: `866a2e1427c181e2b7cb7bed8ca78c8383d251e2831607ffa95839731578f6dc`; snapshots: `full-21-p2-snapshot-target, full-21-p2-snapshot-aux`
- Candidate snapshot: `full-21-p2-snapshot-target`; runtime item: `full-21-p2-runtime-target`; hash: `5af6ac7e828d87025cc2211a32a3082aa0967c03bf88d750459a9d85c27742f8`
- Candidate source IDs: `full-21-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for deep-link router schema contract is path matching.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `reject_invalid`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `investigate`; action-selection task present: `true`
- Required evidence IDs: `full-21-p2-source, full-21-p2-aux, full-21-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-21_2

#### Checkpoints and downstream tasks

- Checkpoint `full-21-p2-checkpoint` after sequence `10`
- Task `full-21-p2-state-task` (`current_state_query`) at `full-21-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The accepted preference for deep-link router schema contract is path matching.', 'scope': {'system': 'deep-link-router-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-21-p2-source']}]}`; dependencies: `full-21-p2-source, full-21-p2-aux, full-21-p2-event`
- Task `full-21-p2-action-task` (`action_selection`) at `full-21-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-21-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'investigate'}`; dependencies: `full-21-p2-source, full-21-p2-aux, full-21-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-21-p3-pair`

- Evaluated event: `full-21-p3-event`; context events: `full-21-p3-source`
- Candidate pool: `full-21-p3-pool`; hash: `824b43573514fb721ef80d9c42681dd9c3b2a20d9920e84d304f2f2414486537`; snapshots: `full-21-p3-snapshot-target, full-21-p3-snapshot-aux`
- Candidate snapshot: `full-21-p3-snapshot-target`; runtime item: `full-21-p3-runtime-target`; hash: `02e5b3558757d2b964704316006cc7221276aa32637ec5ca6f07983721d3d49c`
- Candidate source IDs: `full-21-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The deep-link router authoring guidance uses path matching.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `invalidate`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-21-p3-source, full-21-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-21_3

#### Checkpoints and downstream tasks

- Checkpoint `full-21-p3-checkpoint` after sequence `11`
- Task `full-21-p3-state-task` (`deletion_query`) at `full-21-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The deep-link router authoring guidance uses path matching.', 'scope': {'system': 'deep-link-router-authoring-guidance', 'audience': 'all'}, 'status': 'invalidated', 'evidence_ids': []}], 'invalidated_derivatives': [{'semantic_item_ref': 'semantic:p3:target', 'invalidated_by_event_id': 'full-21-p3-event', 'reason': 'sole_source_deleted'}]}`; dependencies: `full-21-p3-source, full-21-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-21-p4-pair`

- Evaluated event: `full-21-p4-event`; context events: `full-21-p4-source`
- Candidate pool: `full-21-p4-pool`; hash: `6be880fbd9ba17c86d7971e1fda37b85f050da84788da32dd6286a46a95f3afe`; snapshots: `full-21-p4-snapshot-target, full-21-p4-snapshot-aux`
- Candidate snapshot: `full-21-p4-snapshot-target`; runtime item: `full-21-p4-runtime-target`; hash: `04d6f481c558ae3591d9da0b041035737eb417346b5961ec60c6b7b97c56c4e4`
- Candidate source IDs: `full-21-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for deep-link router migration plan is path matching.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-21-p4-source, full-21-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-21_4

#### Checkpoints and downstream tasks

- Checkpoint `full-21-p4-checkpoint` after sequence `12`
- Task `full-21-p4-state-task` (`current_state_query`) at `full-21-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for deep-link router migration plan is path matching.', 'scope': {'system': 'deep-link-router-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-21-p4-source']}]}`; dependencies: `full-21-p4-source, full-21-p4-event`
- Task `full-21-p4-action-task` (`action_selection`) at `full-21-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-21-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-21-p4-source, full-21-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-22 — surface-family-02

- Record: [`../holdout.jsonl` line 8](../holdout.jsonl#L8)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-22-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use device key for experiment assignment runtime behavior across ordinary cases.'
- `full-22-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only experiment assignment runtime behavior variant uses account key within signed-out sessions.'
- `full-22-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Provider H22 may satisfy the needs of experiment assignment schema contract.'
- `full-22-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The user has an active approved goal to prepare an outreach candidate for experiment assignment schema contract when every declared requirement is met.'
- `full-22-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for experiment assignment authoring guidance is device key.'
- `full-22-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only experiment assignment authoring guidance variant uses account key within signed-out sessions.'
- `full-22-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for experiment assignment migration plan is device key.'
- `full-22-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only experiment assignment migration plan variant uses account key within signed-out sessions.'
- `full-22-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'experiment-assignment-runtime-behavior', 'audience': 'signed-out-sessions'}}`; content: 'The schema inspection records account key for experiment assignment runtime behavior.'
- `full-22-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The listed experiment assignment schema contract value is device key, according to the test report.'
- `full-22-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'For experiment assignment authoring guidance, the registry audit gives account key as the value.'
- `full-22-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'The release checklist records account key for experiment assignment migration plan.'

### Pair `full-22-p1-pair`

- Evaluated event: `full-22-p1-event`; context events: `full-22-p1-source`
- Candidate pool: `full-22-p1-pool`; hash: `8f40e161b55dc0d49e9c35032fe93a646bc508ff56439e102ecaf572a5d8d692`; snapshots: `full-22-p1-snapshot-target, full-22-p1-snapshot-aux`
- Candidate snapshot: `full-22-p1-snapshot-target`; runtime item: `full-22-p1-runtime-target`; hash: `d7cab347cdf825f017119ddf8a04379f56a1207d2a991a190f2d4a5545a9bae2`
- Candidate source IDs: `full-22-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use device key for experiment assignment runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-22-p1-source, full-22-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-22_1

#### Checkpoints and downstream tasks

- Checkpoint `full-22-p1-checkpoint` after sequence `9`
- Task `full-22-p1-state-task` (`current_state_query`) at `full-22-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use device key for experiment assignment runtime behavior across ordinary cases.', 'scope': {'system': 'experiment-assignment-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-22-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'The schema inspection records account key for experiment assignment runtime behavior.', 'scope': {'system': 'experiment-assignment-runtime-behavior', 'audience': 'signed-out-sessions'}, 'status': 'active', 'evidence_ids': ['full-22-p1-event']}]}`; dependencies: `full-22-p1-source, full-22-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-22-p2-pair`

- Evaluated event: `full-22-p2-event`; context events: `full-22-p2-source, full-22-p2-aux`
- Candidate pool: `full-22-p2-pool`; hash: `08c449ce0e1d7c58560b5c3b79d17ec85ed757188fe72a5abc5a4a8bbefb1c8d`; snapshots: `full-22-p2-snapshot-target, full-22-p2-snapshot-aux`
- Candidate snapshot: `full-22-p2-snapshot-target`; runtime item: `full-22-p2-runtime-target`; hash: `636541aa8cc01479600602b6749c942d85e7fe08c488c7771980484f03ec3072`
- Candidate source IDs: `full-22-p2-source`; counterevidence IDs: `none`
- Candidate proposition: Provider H22 may satisfy the needs of experiment assignment schema contract.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `outreach_candidate`; action-selection task present: `true`
- Required evidence IDs: `full-22-p2-source, full-22-p2-aux, full-22-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-22_2

#### Checkpoints and downstream tasks

- Checkpoint `full-22-p2-checkpoint` after sequence `10`
- Task `full-22-p2-state-task` (`current_state_query`) at `full-22-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'Provider H22 may satisfy the needs of experiment assignment schema contract.', 'scope': {'system': 'experiment-assignment-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-22-p2-source', 'full-22-p2-event']}]}`; dependencies: `full-22-p2-source, full-22-p2-aux, full-22-p2-event`
- Task `full-22-p2-action-task` (`action_selection`) at `full-22-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-22-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'outreach_candidate'}`; dependencies: `full-22-p2-source, full-22-p2-aux, full-22-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-22-p3-pair`

- Evaluated event: `full-22-p3-event`; context events: `full-22-p3-source`
- Candidate pool: `full-22-p3-pool`; hash: `79e96be10c7c1217a0d54615585d924b23fdefb79379a5b1a714148df8b5ddf1`; snapshots: `full-22-p3-snapshot-target, full-22-p3-snapshot-aux`
- Candidate snapshot: `full-22-p3-snapshot-target`; runtime item: `full-22-p3-runtime-target`; hash: `b6ccd7901ec539939c301c23ff272585c484caec385dbff97dc09d89cf597ffd`
- Candidate source IDs: `full-22-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for experiment assignment authoring guidance is device key.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-22-p3-source, full-22-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-22_3

#### Checkpoints and downstream tasks

- Checkpoint `full-22-p3-checkpoint` after sequence `11`
- Task `full-22-p3-state-task` (`current_state_query`) at `full-22-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The current value for experiment assignment authoring guidance is device key.', 'scope': {'system': 'experiment-assignment-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-22-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'For experiment assignment authoring guidance, the registry audit gives account key as the value.', 'scope': {'system': 'experiment-assignment-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-22-p3-event']}]}`; dependencies: `full-22-p3-source, full-22-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-22-p4-pair`

- Evaluated event: `full-22-p4-event`; context events: `full-22-p4-source`
- Candidate pool: `full-22-p4-pool`; hash: `cc910c042940f5b71c10e78f438888a506f5063850c44afdef42c7f777758668`; snapshots: `full-22-p4-snapshot-target, full-22-p4-snapshot-aux`
- Candidate snapshot: `full-22-p4-snapshot-target`; runtime item: `full-22-p4-runtime-target`; hash: `0e39abc310476628a2f58c25fcb04b9f63aa047157ba02ae1a064ca8443fa057`
- Candidate source IDs: `full-22-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for experiment assignment migration plan is device key.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-22-p4-source, full-22-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-22_4

#### Checkpoints and downstream tasks

- Checkpoint `full-22-p4-checkpoint` after sequence `12`
- Task `full-22-p4-state-task` (`current_state_query`) at `full-22-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for experiment assignment migration plan is device key.', 'scope': {'system': 'experiment-assignment-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-22-p4-source']}]}`; dependencies: `full-22-p4-source, full-22-p4-event`
- Task `full-22-p4-action-task` (`action_selection`) at `full-22-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-22-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-22-p4-source, full-22-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-23 — surface-family-03

- Record: [`../development.jsonl` line 15](../development.jsonl#L15)
- Partition: `pilot_development`
### Timeline and authority

- `full-23-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change error presentation runtime behavior to inline recovery.'
- `full-23-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only error presentation runtime behavior variant uses inline recovery within destructive actions.'
- `full-23-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for error presentation schema contract is toast message.'
- `full-23-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only error presentation schema contract variant uses inline recovery within destructive actions.'
- `full-23-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for error presentation authoring guidance is toast message.'
- `full-23-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only error presentation authoring guidance variant uses inline recovery within destructive actions.'
- `full-23-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The error presentation migration plan uses toast message.'
- `full-23-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The error presentation migration plan uses toast message.'
- `full-23-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'For error presentation runtime behavior, the maintainer journal gives inline recovery as the value.'
- `full-23-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The listed error presentation schema contract value is toast message, according to the schema inspection.'
- `full-23-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The selected arrangement depends on which request is meant; the current note gives no distinguishing detail.'
- `full-23-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-23-p4-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'

### Pair `full-23-p1-pair`

- Evaluated event: `full-23-p1-event`; context events: `full-23-p1-source`
- Candidate pool: `full-23-p1-pool`; hash: `e704b492bc85f405a78c16b777eb3ddee4526fe4b75a2e39dad17319db17be7f`; snapshots: `full-23-p1-snapshot-target, full-23-p1-snapshot-aux`
- Candidate snapshot: `full-23-p1-snapshot-target`; runtime item: `full-23-p1-runtime-target`; hash: `2499680dcda4882ac5bf39a18614dd8acb3827ddbca448aba66319ab5a3e06e2`
- Candidate source IDs: `full-23-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change error presentation runtime behavior to inline recovery.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-23-p1-source, full-23-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-23_1

#### Checkpoints and downstream tasks

- Checkpoint `full-23-p1-checkpoint` after sequence `9`
- Task `full-23-p1-state-task` (`commitment_query`) at `full-23-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The team committed to change error presentation runtime behavior to inline recovery.', 'scope': {'system': 'error-presentation-runtime-behavior', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-23-p1-source', 'full-23-p1-event']}]}`; dependencies: `full-23-p1-source, full-23-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-23-p2-pair`

- Evaluated event: `full-23-p2-event`; context events: `full-23-p2-source`
- Candidate pool: `full-23-p2-pool`; hash: `155f91648ac2d0f5b7e08ef3c62a7535a7268700a86bb41ec404701a0ca4e37f`; snapshots: `full-23-p2-snapshot-target, full-23-p2-snapshot-aux`
- Candidate snapshot: `full-23-p2-snapshot-target`; runtime item: `full-23-p2-runtime-target`; hash: `7f19cfbd1c329e490e12304a4083ca896db1f23b7bdcbcf80c52026d7ffd43a7`
- Candidate source IDs: `full-23-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for error presentation schema contract is toast message.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-23-p2-source, full-23-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-23_2

#### Checkpoints and downstream tasks

- Checkpoint `full-23-p2-checkpoint` after sequence `10`
- Task `full-23-p2-state-task` (`current_state_query`) at `full-23-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The accepted preference for error presentation schema contract is toast message.', 'scope': {'system': 'error-presentation-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-23-p2-source', 'full-23-p2-event']}]}`; dependencies: `full-23-p2-source, full-23-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-23-p3-pair`

- Evaluated event: `full-23-p3-event`; context events: `full-23-p3-source`
- Candidate pool: `full-23-p3-pool`; hash: `f680280c85cd49b33ab5c1cab8b75d152e391f96ee53d969fc5356a46ffeebe2`; snapshots: `full-23-p3-snapshot-target, full-23-p3-snapshot-aux`
- Candidate snapshot: `full-23-p3-snapshot-target`; runtime item: `full-23-p3-runtime-target`; hash: `4857d6b12157b0e935c7bd8606a096b06e93194cc0da40323bafe620348ae6f8`
- Candidate source IDs: `full-23-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for error presentation authoring guidance is toast message.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-23-p3-source, full-23-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-23_3

#### Checkpoints and downstream tasks

- Checkpoint `full-23-p3-checkpoint` after sequence `11`
- Task `full-23-p3-state-task` (`current_state_query`) at `full-23-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for error presentation authoring guidance is toast message.', 'scope': {'system': 'error-presentation-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-23-p3-source']}]}`; dependencies: `full-23-p3-source, full-23-p3-event`
- Task `full-23-p3-action-task` (`action_selection`) at `full-23-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-23-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-23-p3-source, full-23-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-23-p4-pair`

- Evaluated event: `full-23-p4-event`; context events: `full-23-p4-source, full-23-p4-aux`
- Candidate pool: `full-23-p4-pool`; hash: `c145ae01d640590ba198ed6b3fc6ef1f29c66935d9404df82bf1a435a4d28d9f`; snapshots: `full-23-p4-snapshot-target, full-23-p4-snapshot-aux`
- Candidate snapshot: `full-23-p4-snapshot-target`; runtime item: `full-23-p4-runtime-target`; hash: `aab405fb3ef334cbb5cd1f17eecf9f7648c72fe6ff3d974719187f0078a6123e`
- Candidate source IDs: `full-23-p4-source, full-23-p4-aux`; counterevidence IDs: `none`
- Candidate proposition: The error presentation migration plan uses toast message.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-23-p4-source, full-23-p4-aux, full-23-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-23_4

#### Checkpoints and downstream tasks

- Checkpoint `full-23-p4-checkpoint` after sequence `12`
- Task `full-23-p4-state-task` (`deletion_query`) at `full-23-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The error presentation migration plan uses toast message.', 'scope': {'system': 'error-presentation-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-23-p4-aux']}], 'invalidated_derivatives': []}`; dependencies: `full-23-p4-source, full-23-p4-aux, full-23-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-24 — surface-family-04

- Record: [`../development.jsonl` line 16](../development.jsonl#L16)
- Partition: `pilot_development`
### Timeline and authority

- `full-24-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use submit-time checks for form validation runtime behavior across ordinary cases.'
- `full-24-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only form validation runtime behavior variant uses field checks within slow connections.'
- `full-24-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for form validation schema contract is submit-time checks.'
- `full-24-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only form validation schema contract variant uses field checks within slow connections.'
- `full-24-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for form validation authoring guidance is submit-time checks.'
- `full-24-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only form validation authoring guidance variant uses field checks within slow connections.'
- `full-24-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for form validation migration plan is submit-time checks.'
- `full-24-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only form validation migration plan variant uses field checks within slow connections.'
- `full-24-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'form-validation-runtime-behavior', 'audience': 'slow-connections'}}`; content: 'The ownership record reports that form validation runtime behavior uses field checks.'
- `full-24-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed form validation schema contract value is field checks, according to the maintainer journal.'
- `full-24-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'For form validation authoring guidance, the schema inspection gives field checks as the value.'
- `full-24-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The listed form validation migration plan value is submit-time checks, according to the test report.'

### Pair `full-24-p1-pair`

- Evaluated event: `full-24-p1-event`; context events: `full-24-p1-source`
- Candidate pool: `full-24-p1-pool`; hash: `40055e781c53fb9a1fe9fb6fa7c93e4b73db578e2fe4efa67c6affd349aa2f28`; snapshots: `full-24-p1-snapshot-target, full-24-p1-snapshot-aux`
- Candidate snapshot: `full-24-p1-snapshot-target`; runtime item: `full-24-p1-runtime-target`; hash: `d3c1caf840a10c322ec7702795112ae298671c8cc5d066088a05110ff33f6617`
- Candidate source IDs: `full-24-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use submit-time checks for form validation runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-24-p1-source, full-24-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-24_1

#### Checkpoints and downstream tasks

- Checkpoint `full-24-p1-checkpoint` after sequence `9`
- Task `full-24-p1-state-task` (`current_state_query`) at `full-24-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use submit-time checks for form validation runtime behavior across ordinary cases.', 'scope': {'system': 'form-validation-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-24-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'The ownership record reports that form validation runtime behavior uses field checks.', 'scope': {'system': 'form-validation-runtime-behavior', 'audience': 'slow-connections'}, 'status': 'active', 'evidence_ids': ['full-24-p1-event']}]}`; dependencies: `full-24-p1-source, full-24-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-24-p2-pair`

- Evaluated event: `full-24-p2-event`; context events: `full-24-p2-source`
- Candidate pool: `full-24-p2-pool`; hash: `5b35d9834dbbc148b9d99dc66b061f0303bf95d0168232a2b941e16ce79621a2`; snapshots: `full-24-p2-snapshot-target, full-24-p2-snapshot-aux`
- Candidate snapshot: `full-24-p2-snapshot-target`; runtime item: `full-24-p2-runtime-target`; hash: `924d3c8da35f9298124a3692da6fe7720f7a591cf374c1a863d08e825ca2afa8`
- Candidate source IDs: `full-24-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for form validation schema contract is submit-time checks.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-24-p2-source, full-24-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-24_2

#### Checkpoints and downstream tasks

- Checkpoint `full-24-p2-checkpoint` after sequence `10`
- Task `full-24-p2-state-task` (`current_state_query`) at `full-24-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The current value for form validation schema contract is submit-time checks.', 'scope': {'system': 'form-validation-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-24-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The listed form validation schema contract value is field checks, according to the maintainer journal.', 'scope': {'system': 'form-validation-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-24-p2-event']}]}`; dependencies: `full-24-p2-source, full-24-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-24-p3-pair`

- Evaluated event: `full-24-p3-event`; context events: `full-24-p3-source`
- Candidate pool: `full-24-p3-pool`; hash: `8ab795021691bea1acfc403b7cca8f3df058acba4ecafdea3d2f021fb22a8cfd`; snapshots: `full-24-p3-snapshot-target, full-24-p3-snapshot-aux`
- Candidate snapshot: `full-24-p3-snapshot-target`; runtime item: `full-24-p3-runtime-target`; hash: `e26808bc341d0da4f180c6dc19a91b3885f19240b734c4be425e532bebd6a484`
- Candidate source IDs: `full-24-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for form validation authoring guidance is submit-time checks.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-24-p3-source, full-24-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-24_3

#### Checkpoints and downstream tasks

- Checkpoint `full-24-p3-checkpoint` after sequence `11`
- Task `full-24-p3-state-task` (`current_state_query`) at `full-24-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for form validation authoring guidance is submit-time checks.', 'scope': {'system': 'form-validation-authoring-guidance', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-24-p3-source']}]}`; dependencies: `full-24-p3-source, full-24-p3-event`
- Task `full-24-p3-action-task` (`action_selection`) at `full-24-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-24-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-24-p3-source, full-24-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-24-p4-pair`

- Evaluated event: `full-24-p4-event`; context events: `full-24-p4-source`
- Candidate pool: `full-24-p4-pool`; hash: `2f32fb6ccbf6b7d35478466c58fb22c13a90cacdecd778399cfa8e9df7e3fa2c`; snapshots: `full-24-p4-snapshot-target, full-24-p4-snapshot-aux`
- Candidate snapshot: `full-24-p4-snapshot-target`; runtime item: `full-24-p4-runtime-target`; hash: `aed01870200852aa3673c6615d48760ff84c0e52c0c927b234895137978c7e1f`
- Candidate source IDs: `full-24-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for form validation migration plan is submit-time checks.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-24-p4-source, full-24-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-24_4

#### Checkpoints and downstream tasks

- Checkpoint `full-24-p4-checkpoint` after sequence `12`
- Task `full-24-p4-state-task` (`current_state_query`) at `full-24-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The accepted preference for form validation migration plan is submit-time checks.', 'scope': {'system': 'form-validation-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-24-p4-source', 'full-24-p4-event']}]}`; dependencies: `full-24-p4-source, full-24-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-25 — surface-family-05

- Record: [`../development.jsonl` line 17](../development.jsonl#L17)
- Partition: `pilot_development`
### Timeline and authority

- `full-25-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for media upload runtime behavior is single request.'
- `full-25-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only media upload runtime behavior variant uses chunked transfer within large videos.'
- `full-25-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for media upload schema contract is single request.'
- `full-25-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only media upload schema contract variant uses chunked transfer within large videos.'
- `full-25-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for media upload authoring guidance is single request.'
- `full-25-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only media upload authoring guidance variant uses chunked transfer within large videos.'
- `full-25-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use single request for media upload migration plan across ordinary cases.'
- `full-25-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only media upload migration plan variant uses chunked transfer within large videos.'
- `full-25-p1-event` — seq 9; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'Late report, effective 2026-09-16: That choice belongs to the case the previous entry described, though the entry itself is not identified here.'
- `full-25-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'The ownership record records chunked transfer for media upload schema contract.'
- `full-25-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed media upload authoring guidance value is chunked transfer, according to the maintainer journal.'
- `full-25-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'media-upload-migration-plan', 'audience': 'large-videos'}}`; content: 'The schema inspection reports that media upload migration plan uses chunked transfer.'

### Pair `full-25-p1-pair`

- Evaluated event: `full-25-p1-event`; context events: `full-25-p1-source`
- Candidate pool: `full-25-p1-pool`; hash: `fa7b5c2cf2298bc3d02ee22148a0901418c909d9d541308f5b0f90622c3a0860`; snapshots: `full-25-p1-snapshot-target, full-25-p1-snapshot-aux`
- Candidate snapshot: `full-25-p1-snapshot-target`; runtime item: `full-25-p1-runtime-target`; hash: `97d56c6aba93465c48868a5e93d3abe06d82136e7b4100ef90a7e45bd316a75d`
- Candidate source IDs: `full-25-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for media upload runtime behavior is single request.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-25-p1-source, full-25-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-25_1

#### Checkpoints and downstream tasks

- Checkpoint `full-25-p1-checkpoint` after sequence `9`
- Task `full-25-p1-state-task` (`current_state_query`) at `full-25-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for media upload runtime behavior is single request.', 'scope': {'system': 'media-upload-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-25-p1-source']}]}`; dependencies: `full-25-p1-source, full-25-p1-event`
- Task `full-25-p1-action-task` (`action_selection`) at `full-25-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-25-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-25-p1-source, full-25-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-25-p2-pair`

- Evaluated event: `full-25-p2-event`; context events: `full-25-p2-source`
- Candidate pool: `full-25-p2-pool`; hash: `a63e93c9b87845f3d07f6922d32f27e2cebe88db5833e81a80a26f9051737c0c`; snapshots: `full-25-p2-snapshot-target, full-25-p2-snapshot-aux`
- Candidate snapshot: `full-25-p2-snapshot-target`; runtime item: `full-25-p2-runtime-target`; hash: `027c90f8317fc633bb448e8f46953492c87646f659372b2a3d62b612a7271aa9`
- Candidate source IDs: `full-25-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for media upload schema contract is single request.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-25-p2-source, full-25-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-25_2

#### Checkpoints and downstream tasks

- Checkpoint `full-25-p2-checkpoint` after sequence `10`
- Task `full-25-p2-state-task` (`current_state_query`) at `full-25-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for media upload schema contract is single request.', 'scope': {'system': 'media-upload-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-25-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The ownership record records chunked transfer for media upload schema contract.', 'scope': {'system': 'media-upload-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-25-p2-event']}]}`; dependencies: `full-25-p2-source, full-25-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-25-p3-pair`

- Evaluated event: `full-25-p3-event`; context events: `full-25-p3-source`
- Candidate pool: `full-25-p3-pool`; hash: `57b52575291b101af630ed2877f5633bae6573c5253df0ae6ba5b35e85c3fcee`; snapshots: `full-25-p3-snapshot-target, full-25-p3-snapshot-aux`
- Candidate snapshot: `full-25-p3-snapshot-target`; runtime item: `full-25-p3-runtime-target`; hash: `23fd5cf4d69cafc9b3a711d5958c715fad9f6699346a595208045570a9db47bc`
- Candidate source IDs: `full-25-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for media upload authoring guidance is single request.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-25-p3-source, full-25-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-25_3

#### Checkpoints and downstream tasks

- Checkpoint `full-25-p3-checkpoint` after sequence `11`
- Task `full-25-p3-state-task` (`current_state_query`) at `full-25-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The current value for media upload authoring guidance is single request.', 'scope': {'system': 'media-upload-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-25-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'The listed media upload authoring guidance value is chunked transfer, according to the maintainer journal.', 'scope': {'system': 'media-upload-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-25-p3-event']}]}`; dependencies: `full-25-p3-source, full-25-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-25-p4-pair`

- Evaluated event: `full-25-p4-event`; context events: `full-25-p4-source`
- Candidate pool: `full-25-p4-pool`; hash: `784cd3e01e280a581e78314282c6862677eddb5d2feb30570ac8756c0c7eab7a`; snapshots: `full-25-p4-snapshot-target, full-25-p4-snapshot-aux`
- Candidate snapshot: `full-25-p4-snapshot-target`; runtime item: `full-25-p4-runtime-target`; hash: `a35efd5d962cacff94205b23b27da72eaef6c4155d9612cbf44a3be55cd7a8ec`
- Candidate source IDs: `full-25-p4-source`; counterevidence IDs: `none`
- Candidate proposition: Use single request for media upload migration plan across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p4:target`; new: `semantic:p4:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-25-p4-source, full-25-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-25_4

#### Checkpoints and downstream tasks

- Checkpoint `full-25-p4-checkpoint` after sequence `12`
- Task `full-25-p4-state-task` (`current_state_query`) at `full-25-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'Use single request for media upload migration plan across ordinary cases.', 'scope': {'system': 'media-upload-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-25-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:scoped', 'proposition': 'The schema inspection reports that media upload migration plan uses chunked transfer.', 'scope': {'system': 'media-upload-migration-plan', 'audience': 'large-videos'}, 'status': 'active', 'evidence_ids': ['full-25-p4-event']}]}`; dependencies: `full-25-p4-source, full-25-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-26 — surface-family-06

- Record: [`../development.jsonl` line 18](../development.jsonl#L18)
- Partition: `pilot_development`
### Timeline and authority

- `full-26-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use silent retry for subscription renewal runtime behavior across ordinary cases.'
- `full-26-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only subscription renewal runtime behavior variant uses review prompt within price increases.'
- `full-26-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The subscription renewal schema contract uses silent retry.'
- `full-26-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only subscription renewal schema contract variant uses review prompt within price increases.'
- `full-26-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for subscription renewal authoring guidance is silent retry.'
- `full-26-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only subscription renewal authoring guidance variant uses review prompt within price increases.'
- `full-26-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change subscription renewal migration plan to review prompt.'
- `full-26-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only subscription renewal migration plan variant uses review prompt within price increases.'
- `full-26-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'subscription-renewal-runtime-behavior', 'audience': 'price-increases'}}`; content: 'The migration review records review prompt for subscription renewal runtime behavior.'
- `full-26-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The facilities log recorded a brief power interruption during the morning shift.'
- `full-26-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'For subscription renewal authoring guidance, the ownership record gives review prompt as the value.'
- `full-26-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The maintainer journal records review prompt for subscription renewal migration plan.'

### Pair `full-26-p1-pair`

- Evaluated event: `full-26-p1-event`; context events: `full-26-p1-source`
- Candidate pool: `full-26-p1-pool`; hash: `d58911e8bd0dafb614a8929384ea470412ca333754af7785b802cdf3eb4896dc`; snapshots: `full-26-p1-snapshot-target, full-26-p1-snapshot-aux`
- Candidate snapshot: `full-26-p1-snapshot-target`; runtime item: `full-26-p1-runtime-target`; hash: `d18840f11b341cc2ab952a825dfb540d0e7cdd1dae2834476f5b3f7c0a3c5c35`
- Candidate source IDs: `full-26-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use silent retry for subscription renewal runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-26-p1-source, full-26-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-26_1

#### Checkpoints and downstream tasks

- Checkpoint `full-26-p1-checkpoint` after sequence `9`
- Task `full-26-p1-state-task` (`current_state_query`) at `full-26-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use silent retry for subscription renewal runtime behavior across ordinary cases.', 'scope': {'system': 'subscription-renewal-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-26-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'The migration review records review prompt for subscription renewal runtime behavior.', 'scope': {'system': 'subscription-renewal-runtime-behavior', 'audience': 'price-increases'}, 'status': 'active', 'evidence_ids': ['full-26-p1-event']}]}`; dependencies: `full-26-p1-source, full-26-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-26-p2-pair`

- Evaluated event: `full-26-p2-event`; context events: `full-26-p2-source`
- Candidate pool: `full-26-p2-pool`; hash: `cb20cf4e492c126af53c06fd7b495ec0d683b263fed11d373183b183a1c8c507`; snapshots: `full-26-p2-snapshot-target, full-26-p2-snapshot-aux`
- Candidate snapshot: `full-26-p2-snapshot-target`; runtime item: `full-26-p2-runtime-target`; hash: `6c89d73810f84ecaeaa7ea7eb02f6708c2c7528a028b6818fa0d419b499fd0d1`
- Candidate source IDs: `full-26-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The subscription renewal schema contract uses silent retry.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-26-p2-source, full-26-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-26_2

#### Checkpoints and downstream tasks

- Checkpoint `full-26-p2-checkpoint` after sequence `10`
- Task `full-26-p2-state-task` (`current_state_query`) at `full-26-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The subscription renewal schema contract uses silent retry.', 'scope': {'system': 'subscription-renewal-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-26-p2-source']}]}`; dependencies: `full-26-p2-source, full-26-p2-event`
- Task `full-26-p2-action-task` (`action_selection`) at `full-26-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-26-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-26-p2-source, full-26-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-26-p3-pair`

- Evaluated event: `full-26-p3-event`; context events: `full-26-p3-source`
- Candidate pool: `full-26-p3-pool`; hash: `66e8b56c2b6b555827f45d0a06387491a75fb4bdfd593a3820ada2509b19057e`; snapshots: `full-26-p3-snapshot-target, full-26-p3-snapshot-aux`
- Candidate snapshot: `full-26-p3-snapshot-target`; runtime item: `full-26-p3-runtime-target`; hash: `6c40f5608e72fc6fd36a65546b4b149462cde654d15aab8af4d9e8038a6b66be`
- Candidate source IDs: `full-26-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for subscription renewal authoring guidance is silent retry.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-26-p3-source, full-26-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-26_3

#### Checkpoints and downstream tasks

- Checkpoint `full-26-p3-checkpoint` after sequence `11`
- Task `full-26-p3-state-task` (`current_state_query`) at `full-26-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for subscription renewal authoring guidance is silent retry.', 'scope': {'system': 'subscription-renewal-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-26-p3-source']}]}`; dependencies: `full-26-p3-source, full-26-p3-event`
- Task `full-26-p3-action-task` (`action_selection`) at `full-26-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-26-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-26-p3-source, full-26-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-26-p4-pair`

- Evaluated event: `full-26-p4-event`; context events: `full-26-p4-source`
- Candidate pool: `full-26-p4-pool`; hash: `18730ccb860138bf0bf7490319ffe2e1ab7544ba8b1a8059beefae7025d9a62c`; snapshots: `full-26-p4-snapshot-target, full-26-p4-snapshot-aux`
- Candidate snapshot: `full-26-p4-snapshot-target`; runtime item: `full-26-p4-runtime-target`; hash: `f4bbc2c622fb0b814aedf245f4d0a537deaab8daf1e32427ef9ac4dfc0cb2c90`
- Candidate source IDs: `full-26-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change subscription renewal migration plan to review prompt.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-26-p4-source, full-26-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-26_4

#### Checkpoints and downstream tasks

- Checkpoint `full-26-p4-checkpoint` after sequence `12`
- Task `full-26-p4-state-task` (`commitment_query`) at `full-26-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The team committed to change subscription renewal migration plan to review prompt.', 'scope': {'system': 'subscription-renewal-migration-plan', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-26-p4-source', 'full-26-p4-event']}]}`; dependencies: `full-26-p4-source, full-26-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-27 — surface-family-07

- Record: [`../development.jsonl` line 19](../development.jsonl#L19)
- Partition: `pilot_development`
### Timeline and authority

- `full-27-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use manual review for merchant onboarding runtime behavior across ordinary cases.'
- `full-27-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only merchant onboarding runtime behavior variant uses risk tiers within low-volume sellers.'
- `full-27-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for merchant onboarding schema contract is manual review.'
- `full-27-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only merchant onboarding schema contract variant uses risk tiers within low-volume sellers.'
- `full-27-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to review merchant onboarding authoring guidance before 09:00 UTC.'
- `full-27-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only merchant onboarding authoring guidance variant uses risk tiers within low-volume sellers.'
- `full-27-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for merchant onboarding migration plan is manual review.'
- `full-27-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only merchant onboarding migration plan variant uses risk tiers within low-volume sellers.'
- `full-27-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'merchant-onboarding-runtime-behavior', 'audience': 'low-volume-sellers'}}`; content: 'For merchant onboarding runtime behavior, the compatibility review gives risk tiers as the value.'
- `full-27-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The migration review reports that merchant onboarding schema contract uses risk tiers.'
- `full-27-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `evaluator`; type `time_advance`; assert `false`; transition `true`; reason: evaluator clock event for lifecycle evaluation only; deletion targets: `none`; metadata: `{'advance_to': '2026-09-18T10:00:00Z'}`; content: None
- `full-27-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The ownership record records manual review for merchant onboarding migration plan.'

### Pair `full-27-p1-pair`

- Evaluated event: `full-27-p1-event`; context events: `full-27-p1-source`
- Candidate pool: `full-27-p1-pool`; hash: `2bd62f8d1fe63873eefc6c3a46afdb22be78e62eef8becf2b37f80bf5413b561`; snapshots: `full-27-p1-snapshot-target, full-27-p1-snapshot-aux`
- Candidate snapshot: `full-27-p1-snapshot-target`; runtime item: `full-27-p1-runtime-target`; hash: `09b32fc43d21b0944259e574126b17e29a5b1000714aa8587411060eb53382cd`
- Candidate source IDs: `full-27-p1-source`; counterevidence IDs: `none`
- Candidate proposition: Use manual review for merchant onboarding runtime behavior across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p1:target`; new: `semantic:p1:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-27-p1-source, full-27-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-27_1

#### Checkpoints and downstream tasks

- Checkpoint `full-27-p1-checkpoint` after sequence `9`
- Task `full-27-p1-state-task` (`current_state_query`) at `full-27-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'Use manual review for merchant onboarding runtime behavior across ordinary cases.', 'scope': {'system': 'merchant-onboarding-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-27-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:scoped', 'proposition': 'For merchant onboarding runtime behavior, the compatibility review gives risk tiers as the value.', 'scope': {'system': 'merchant-onboarding-runtime-behavior', 'audience': 'low-volume-sellers'}, 'status': 'active', 'evidence_ids': ['full-27-p1-event']}]}`; dependencies: `full-27-p1-source, full-27-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-27-p2-pair`

- Evaluated event: `full-27-p2-event`; context events: `full-27-p2-source`
- Candidate pool: `full-27-p2-pool`; hash: `fd74382fa2f50dc8385a7f5ef4c89aca7ddfa5d9c7c672dbb9967e51264e23bd`; snapshots: `full-27-p2-snapshot-target, full-27-p2-snapshot-aux`
- Candidate snapshot: `full-27-p2-snapshot-target`; runtime item: `full-27-p2-runtime-target`; hash: `4d21750ea1f4c3d8a69d9eabf4d1645f0a0bef861b272784064b88334d4350d6`
- Candidate source IDs: `full-27-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for merchant onboarding schema contract is manual review.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p2:target`; new: `semantic:p2:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-27-p2-source, full-27-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-27_2

#### Checkpoints and downstream tasks

- Checkpoint `full-27-p2-checkpoint` after sequence `10`
- Task `full-27-p2-state-task` (`current_state_query`) at `full-27-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target', 'semantic:p2:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The current value for merchant onboarding schema contract is manual review.', 'scope': {'system': 'merchant-onboarding-schema-contract', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-27-p2-source']}, {'semantic_item_ref': 'semantic:p2:target:replacement', 'proposition': 'The migration review reports that merchant onboarding schema contract uses risk tiers.', 'scope': {'system': 'merchant-onboarding-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-27-p2-event']}]}`; dependencies: `full-27-p2-source, full-27-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-27-p3-pair`

- Evaluated event: `full-27-p3-event`; context events: `full-27-p3-source`
- Candidate pool: `full-27-p3-pool`; hash: `fe951febc2cb9f055e90a796d40e77571dea8f0d522b7e7d0367c54d94fbcba0`; snapshots: `full-27-p3-snapshot-target, full-27-p3-snapshot-aux`
- Candidate snapshot: `full-27-p3-snapshot-target`; runtime item: `full-27-p3-runtime-target`; hash: `9e4c379f7e0655b28676596223b75d93ef9ff006ebc6b8922c92c431c942949a`
- Candidate source IDs: `full-27-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to review merchant onboarding authoring guidance before 09:00 UTC.
- Candidate validity: `2026-09-17T12:00:00Z` through `2026-09-18T09:00:00Z`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `expire`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-27-p3-source, full-27-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-27_3

#### Checkpoints and downstream tasks

- Checkpoint `full-27-p3-checkpoint` after sequence `11`
- Task `full-27-p3-state-task` (`commitment_query`) at `full-27-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The team committed to review merchant onboarding authoring guidance before 09:00 UTC.', 'scope': {'system': 'merchant-onboarding-authoring-guidance', 'audience': 'all'}, 'status': 'expired', 'evidence_ids': ['full-27-p3-source']}]}`; dependencies: `full-27-p3-source, full-27-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-27-p4-pair`

- Evaluated event: `full-27-p4-event`; context events: `full-27-p4-source`
- Candidate pool: `full-27-p4-pool`; hash: `25536d8f04d04fcb5daa45bc542fca9c01802d02a7f52ac407439a81fccb3582`; snapshots: `full-27-p4-snapshot-target, full-27-p4-snapshot-aux`
- Candidate snapshot: `full-27-p4-snapshot-target`; runtime item: `full-27-p4-runtime-target`; hash: `76ada1422925475cacca2850c6af7188716c36012571ffa31b575cb73a04d567`
- Candidate source IDs: `full-27-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for merchant onboarding migration plan is manual review.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `accept`
- Expected state effect: `reinforce`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-27-p4-source, full-27-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-27_4

#### Checkpoints and downstream tasks

- Checkpoint `full-27-p4-checkpoint` after sequence `12`
- Task `full-27-p4-state-task` (`current_state_query`) at `full-27-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The accepted preference for merchant onboarding migration plan is manual review.', 'scope': {'system': 'merchant-onboarding-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-27-p4-source', 'full-27-p4-event']}]}`; dependencies: `full-27-p4-source, full-27-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-28 — surface-family-08

- Record: [`../development.jsonl` line 20](../development.jsonl#L20)
- Partition: `pilot_development`
### Timeline and authority

- `full-28-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The accepted preference for privacy export runtime behavior is email archive.'
- `full-28-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Validation policy requires investigation of an authorized transition whose validity interval ends before it begins.'
- `full-28-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for privacy export schema contract is email archive.'
- `full-28-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only privacy export schema contract variant uses download center within large accounts.'
- `full-28-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for privacy export authoring guidance is email archive.'
- `full-28-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only privacy export authoring guidance variant uses download center within large accounts.'
- `full-28-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for privacy export migration plan is email archive.'
- `full-28-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only privacy export migration plan variant uses download center within large accounts.'
- `full-28-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'valid_from': '2026-10-01T00:00:00Z', 'valid_until': '2026-09-01T00:00:00Z'}`; content: 'For privacy export runtime behavior, the architecture note gives email archive as the value.'
- `full-28-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'That choice belongs to the case the previous entry described, though the entry itself is not identified here.'
- `full-28-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The selected arrangement depends on which request is meant; the current note gives no distinguishing detail.'
- `full-28-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'For privacy export migration plan, the incident follow-up gives download center as the value.'

### Pair `full-28-p1-pair`

- Evaluated event: `full-28-p1-event`; context events: `full-28-p1-source, full-28-p1-aux`
- Candidate pool: `full-28-p1-pool`; hash: `45ed3e09eb3b94d40730b82488805dbd665cf1709e1382b0a75fa9c251853ccb`; snapshots: `full-28-p1-snapshot-target, full-28-p1-snapshot-aux`
- Candidate snapshot: `full-28-p1-snapshot-target`; runtime item: `full-28-p1-runtime-target`; hash: `e5b5a955daf043dca495d0003de20381f91d07e2cb9a659ad6da579fe3ad8411`
- Candidate source IDs: `full-28-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The accepted preference for privacy export runtime behavior is email archive.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supports`
- Transition disposition: `reject_invalid`
- Expected state effect: `none`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `investigate`; action-selection task present: `true`
- Required evidence IDs: `full-28-p1-source, full-28-p1-aux, full-28-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-28_1

#### Checkpoints and downstream tasks

- Checkpoint `full-28-p1-checkpoint` after sequence `9`
- Task `full-28-p1-state-task` (`current_state_query`) at `full-28-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The accepted preference for privacy export runtime behavior is email archive.', 'scope': {'system': 'privacy-export-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-28-p1-source']}]}`; dependencies: `full-28-p1-source, full-28-p1-aux, full-28-p1-event`
- Task `full-28-p1-action-task` (`action_selection`) at `full-28-p1-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-28-p1-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'investigate'}`; dependencies: `full-28-p1-source, full-28-p1-aux, full-28-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-28-p2-pair`

- Evaluated event: `full-28-p2-event`; context events: `full-28-p2-source`
- Candidate pool: `full-28-p2-pool`; hash: `c7c91651931bc3cecfc8c0521a56adbc144c2e308981388f6b3727d41d4a6cbb`; snapshots: `full-28-p2-snapshot-target, full-28-p2-snapshot-aux`
- Candidate snapshot: `full-28-p2-snapshot-target`; runtime item: `full-28-p2-runtime-target`; hash: `25717ce60bab9c180daa7a761b5a730afb6720230a8aa13e7dbe5ec800ffc280`
- Candidate source IDs: `full-28-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for privacy export schema contract is email archive.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-28-p2-source, full-28-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-28_2

#### Checkpoints and downstream tasks

- Checkpoint `full-28-p2-checkpoint` after sequence `10`
- Task `full-28-p2-state-task` (`current_state_query`) at `full-28-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The recorded value for privacy export schema contract is email archive.', 'scope': {'system': 'privacy-export-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-28-p2-source']}]}`; dependencies: `full-28-p2-source, full-28-p2-event`
- Task `full-28-p2-action-task` (`action_selection`) at `full-28-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-28-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-28-p2-source, full-28-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-28-p3-pair`

- Evaluated event: `full-28-p3-event`; context events: `full-28-p3-source`
- Candidate pool: `full-28-p3-pool`; hash: `bbfee575e7132b9ea65c8dec0b4af09162adc3e164d52a306b4943dd34c1df92`; snapshots: `full-28-p3-snapshot-target, full-28-p3-snapshot-aux`
- Candidate snapshot: `full-28-p3-snapshot-target`; runtime item: `full-28-p3-runtime-target`; hash: `006e32b0071d9816bb046877e3f0a3c2e5735805ff4be1095e8cac09159baa31`
- Candidate source IDs: `full-28-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for privacy export authoring guidance is email archive.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `uncertain`
- Transition disposition: `abstain`
- Expected state effect: `none`; affected: `semantic:p3:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-28-p3-source, full-28-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-28_3

#### Checkpoints and downstream tasks

- Checkpoint `full-28-p3-checkpoint` after sequence `11`
- Task `full-28-p3-state-task` (`current_state_query`) at `full-28-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The recorded value for privacy export authoring guidance is email archive.', 'scope': {'system': 'privacy-export-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-28-p3-source']}]}`; dependencies: `full-28-p3-source, full-28-p3-event`
- Task `full-28-p3-action-task` (`action_selection`) at `full-28-p3-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-28-p3-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-28-p3-source, full-28-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-28-p4-pair`

- Evaluated event: `full-28-p4-event`; context events: `full-28-p4-source`
- Candidate pool: `full-28-p4-pool`; hash: `40b377fb05c8b34650f041f099fd7fb2491ca8bf39c96abf50466c86fb7b605f`; snapshots: `full-28-p4-snapshot-target, full-28-p4-snapshot-aux`
- Candidate snapshot: `full-28-p4-snapshot-target`; runtime item: `full-28-p4-runtime-target`; hash: `c30757baa4f3b2b2ca24c87c41aef21e2d812f49ab55c73f90f27121ef0275b3`
- Candidate source IDs: `full-28-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for privacy export migration plan is email archive.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p4:target`; new: `semantic:p4:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-28-p4-source, full-28-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-28_4

#### Checkpoints and downstream tasks

- Checkpoint `full-28-p4-checkpoint` after sequence `12`
- Task `full-28-p4-state-task` (`current_state_query`) at `full-28-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target', 'semantic:p4:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The current value for privacy export migration plan is email archive.', 'scope': {'system': 'privacy-export-migration-plan', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-28-p4-source']}, {'semantic_item_ref': 'semantic:p4:target:replacement', 'proposition': 'For privacy export migration plan, the incident follow-up gives download center as the value.', 'scope': {'system': 'privacy-export-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-28-p4-event']}]}`; dependencies: `full-28-p4-source, full-28-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-29 — surface-family-09

- Record: [`../development.jsonl` line 21](../development.jsonl#L21)
- Partition: `pilot_development`
### Timeline and authority

- `full-29-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The device enrollment runtime behavior uses shared secret.'
- `full-29-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only device enrollment runtime behavior variant uses attestation within test devices.'
- `full-29-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The device enrollment schema contract uses shared secret.'
- `full-29-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only device enrollment schema contract variant uses attestation within test devices.'
- `full-29-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'Use shared secret for device enrollment authoring guidance across ordinary cases.'
- `full-29-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only device enrollment authoring guidance variant uses attestation within test devices.'
- `full-29-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for device enrollment migration plan is shared secret.'
- `full-29-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only device enrollment migration plan variant uses attestation within test devices.'
- `full-29-p1-event` — seq 9; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `deletion`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `full-29-p1-source`; metadata: `{}`; content: 'The event was recorded at the stated time.'
- `full-29-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{}`; content: 'The daily report records that the test laboratory was closed for routine cleaning.'
- `full-29-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'scope': {'system': 'device-enrollment-authoring-guidance', 'audience': 'test-devices'}}`; content: 'The listed device enrollment authoring guidance value is attestation, according to the compatibility review.'
- `full-29-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic observation with no precedence rank; deletion targets: `none`; metadata: `{}`; content: 'The listed device enrollment migration plan value is attestation, according to the migration review.'

### Pair `full-29-p1-pair`

- Evaluated event: `full-29-p1-event`; context events: `full-29-p1-source`
- Candidate pool: `full-29-p1-pool`; hash: `56abf9a92d38a820f6f66d2d8397b1b5dd71cedb19ec1a36896721f35fa17a1b`; snapshots: `full-29-p1-snapshot-target, full-29-p1-snapshot-aux`
- Candidate snapshot: `full-29-p1-snapshot-target`; runtime item: `full-29-p1-runtime-target`; hash: `2366431fb7c355ed03a2f38205ab23c8d0bb1e3a5539135ff4bd388266741b52`
- Candidate source IDs: `full-29-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The device enrollment runtime behavior uses shared secret.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `accept`
- Expected state effect: `invalidate`; affected: `semantic:p1:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-29-p1-source, full-29-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-29_1

#### Checkpoints and downstream tasks

- Checkpoint `full-29-p1-checkpoint` after sequence `9`
- Task `full-29-p1-state-task` (`deletion_query`) at `full-29-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The device enrollment runtime behavior uses shared secret.', 'scope': {'system': 'device-enrollment-runtime-behavior', 'audience': 'all'}, 'status': 'invalidated', 'evidence_ids': []}], 'invalidated_derivatives': [{'semantic_item_ref': 'semantic:p1:target', 'invalidated_by_event_id': 'full-29-p1-event', 'reason': 'sole_source_deleted'}]}`; dependencies: `full-29-p1-source, full-29-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-29-p2-pair`

- Evaluated event: `full-29-p2-event`; context events: `full-29-p2-source`
- Candidate pool: `full-29-p2-pool`; hash: `72200566081f52965cdad8b23213c7e442fe20701c7f19df08b1d6e3d5cde9b2`; snapshots: `full-29-p2-snapshot-target, full-29-p2-snapshot-aux`
- Candidate snapshot: `full-29-p2-snapshot-target`; runtime item: `full-29-p2-runtime-target`; hash: `cf58dcd7bc00fe8c5c1f1976cf744025d9eb5438715537b59b29b9f3266cdcb1`
- Candidate source IDs: `full-29-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The device enrollment schema contract uses shared secret.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `unrelated`
- Transition disposition: `no_op`
- Expected state effect: `none`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-29-p2-source, full-29-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-29_2

#### Checkpoints and downstream tasks

- Checkpoint `full-29-p2-checkpoint` after sequence `10`
- Task `full-29-p2-state-task` (`current_state_query`) at `full-29-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The device enrollment schema contract uses shared secret.', 'scope': {'system': 'device-enrollment-schema-contract', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-29-p2-source']}]}`; dependencies: `full-29-p2-source, full-29-p2-event`
- Task `full-29-p2-action-task` (`action_selection`) at `full-29-p2-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-29-p2-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-29-p2-source, full-29-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-29-p3-pair`

- Evaluated event: `full-29-p3-event`; context events: `full-29-p3-source`
- Candidate pool: `full-29-p3-pool`; hash: `6a286acff3aedb6dce77093d492c63ab0e0d14aaa19ec53e9eee00c1055d4037`; snapshots: `full-29-p3-snapshot-target, full-29-p3-snapshot-aux`
- Candidate snapshot: `full-29-p3-snapshot-target`; runtime item: `full-29-p3-runtime-target`; hash: `e6b945bf560966c588ba9498d2bfeb5ec3620e19aab084e28d5f27d745210fc4`
- Candidate source IDs: `full-29-p3-source`; counterevidence IDs: `none`
- Candidate proposition: Use shared secret for device enrollment authoring guidance across ordinary cases.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `narrows_scope`
- Transition disposition: `accept`
- Expected state effect: `add_scoped_item`; affected: `semantic:p3:target`; new: `semantic:p3:target:scoped`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-29-p3-source, full-29-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-29_3

#### Checkpoints and downstream tasks

- Checkpoint `full-29-p3-checkpoint` after sequence `11`
- Task `full-29-p3-state-task` (`current_state_query`) at `full-29-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:scoped']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'Use shared secret for device enrollment authoring guidance across ordinary cases.', 'scope': {'system': 'device-enrollment-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-29-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:scoped', 'proposition': 'The listed device enrollment authoring guidance value is attestation, according to the compatibility review.', 'scope': {'system': 'device-enrollment-authoring-guidance', 'audience': 'test-devices'}, 'status': 'active', 'evidence_ids': ['full-29-p3-event']}]}`; dependencies: `full-29-p3-source, full-29-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-29-p4-pair`

- Evaluated event: `full-29-p4-event`; context events: `full-29-p4-source`
- Candidate pool: `full-29-p4-pool`; hash: `1416b7449d9ca60cf5436ca9d6837c85b838cf398240eae70cb231a185107e0d`; snapshots: `full-29-p4-snapshot-target, full-29-p4-snapshot-aux`
- Candidate snapshot: `full-29-p4-snapshot-target`; runtime item: `full-29-p4-runtime-target`; hash: `c786adecd503a7cbd8a5e7783cb31fc34eb3779c5d01d8482dbf270542951242`
- Candidate source IDs: `full-29-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for device enrollment migration plan is shared secret.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `abstain`
- Expected state effect: `preserve_conflict`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `clarify`; action-selection task present: `true`
- Required evidence IDs: `full-29-p4-source, full-29-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-29_4

#### Checkpoints and downstream tasks

- Checkpoint `full-29-p4-checkpoint` after sequence `12`
- Task `full-29-p4-state-task` (`current_state_query`) at `full-29-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for device enrollment migration plan is shared secret.', 'scope': {'system': 'device-enrollment-migration-plan', 'audience': 'all'}, 'status': 'disputed', 'evidence_ids': ['full-29-p4-source']}]}`; dependencies: `full-29-p4-source, full-29-p4-event`
- Task `full-29-p4-action-task` (`action_selection`) at `full-29-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-29-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'clarify'}`; dependencies: `full-29-p4-source, full-29-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:

## full-30 — surface-family-10

- Record: [`../holdout.jsonl` line 9](../holdout.jsonl#L9)
- Partition: `pilot_holdout`
### Timeline and authority

- `full-30-p1-source` — seq 1; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for audit event runtime behavior is free-form payload.'
- `full-30-p1-aux` — seq 2; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only audit event runtime behavior variant uses typed payload within migration windows.'
- `full-30-p2-source` — seq 3; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `user`; type `message`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The team committed to change audit event schema contract to typed payload.'
- `full-30-p2-aux` — seq 4; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only audit event schema contract variant uses typed payload within migration windows.'
- `full-30-p3-source` — seq 5; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The current value for audit event authoring guidance is free-form payload.'
- `full-30-p3-aux` — seq 6; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only audit event authoring guidance variant uses typed payload within migration windows.'
- `full-30-p4-source` — seq 7; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'The recorded value for audit event migration plan is free-form payload.'
- `full-30-p4-aux` — seq 8; occurred `2026-09-17T12:00:00Z`; recorded `2026-09-17T12:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic source; deletion targets: `none`; metadata: `{}`; content: 'A preview-only audit event migration plan variant uses typed payload within migration windows.'
- `full-30-p1-event` — seq 9; occurred `2026-09-16T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized source with explicit precedence; deletion targets: `none`; metadata: `{'precedence_rank': 1}`; content: 'Late report, effective 2026-09-16: The registry audit records typed payload for audit event runtime behavior.'
- `full-30-p2-event` — seq 10; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed audit event schema contract value is typed payload, according to the release checklist.'
- `full-30-p3-event` — seq 11; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `system`; type `observation`; assert `true`; transition `true`; reason: authorized synthetic repository observation; deletion targets: `none`; metadata: `{'effective_from': '2026-09-18T10:00:00Z'}`; content: 'The listed audit event authoring guidance value is typed payload, according to the architecture note.'
- `full-30-p4-event` — seq 12; occurred `2026-09-18T10:00:00Z`; recorded `2026-09-18T10:00:00Z`; actor `external`; type `observation`; assert `false`; transition `false`; reason: context-only imported artifact without update authority; deletion targets: `none`; metadata: `{}`; content: 'The compatibility review records typed payload for audit event migration plan.'

### Pair `full-30-p1-pair`

- Evaluated event: `full-30-p1-event`; context events: `full-30-p1-source`
- Candidate pool: `full-30-p1-pool`; hash: `672e6dbdc10de7a740062ea503b42b738ec8b118f4397f7e8bd9728ec1d734ff`; snapshots: `full-30-p1-snapshot-target, full-30-p1-snapshot-aux`
- Candidate snapshot: `full-30-p1-snapshot-target`; runtime item: `full-30-p1-runtime-target`; hash: `af7656cf837bf569a0279a4dbfe04770dd0891acd8ac0ef54cb9747cbb840365`
- Candidate source IDs: `full-30-p1-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for audit event runtime behavior is free-form payload.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p1:target`; new: `semantic:p1:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-30-p1-source, full-30-p1-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-30_1

#### Checkpoints and downstream tasks

- Checkpoint `full-30-p1-checkpoint` after sequence `9`
- Task `full-30-p1-state-task` (`current_state_query`) at `full-30-p1-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p1:target', 'semantic:p1:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p1:target', 'proposition': 'The recorded value for audit event runtime behavior is free-form payload.', 'scope': {'system': 'audit-event-runtime-behavior', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-30-p1-source']}, {'semantic_item_ref': 'semantic:p1:target:replacement', 'proposition': 'Late report, effective 2026-09-16: The registry audit records typed payload for audit event runtime behavior.', 'scope': {'system': 'audit-event-runtime-behavior', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-30-p1-event']}]}`; dependencies: `full-30-p1-source, full-30-p1-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-30-p2-pair`

- Evaluated event: `full-30-p2-event`; context events: `full-30-p2-source`
- Candidate pool: `full-30-p2-pool`; hash: `c2d822f5e9cf69a256d2f6b32e38fe18103407d2023877460948669f093d89c5`; snapshots: `full-30-p2-snapshot-target, full-30-p2-snapshot-aux`
- Candidate snapshot: `full-30-p2-snapshot-target`; runtime item: `full-30-p2-runtime-target`; hash: `3eea96685086263c88929382bb6b024932b0e17d893ece5c8ecb2c5784d8d44a`
- Candidate source IDs: `full-30-p2-source`; counterevidence IDs: `none`
- Candidate proposition: The team committed to change audit event schema contract to typed payload.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `resolve`; affected: `semantic:p2:target`; new: `none`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-30-p2-source, full-30-p2-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-30_2

#### Checkpoints and downstream tasks

- Checkpoint `full-30-p2-checkpoint` after sequence `10`
- Task `full-30-p2-state-task` (`commitment_query`) at `full-30-p2-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p2:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p2:target', 'proposition': 'The team committed to change audit event schema contract to typed payload.', 'scope': {'system': 'audit-event-schema-contract', 'audience': 'all'}, 'status': 'resolved', 'evidence_ids': ['full-30-p2-source', 'full-30-p2-event']}]}`; dependencies: `full-30-p2-source, full-30-p2-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

### Pair `full-30-p3-pair`

- Evaluated event: `full-30-p3-event`; context events: `full-30-p3-source`
- Candidate pool: `full-30-p3-pool`; hash: `88d2fc52aee25cf09deddae4630442e52a342c6c7c1f3d1d8e516bbf21156fbd`; snapshots: `full-30-p3-snapshot-target, full-30-p3-snapshot-aux`
- Candidate snapshot: `full-30-p3-snapshot-target`; runtime item: `full-30-p3-runtime-target`; hash: `da657ec182a8a9ecdbe515772ca2718e431f194585903ee3f5d9e54a7c7944ce`
- Candidate source IDs: `full-30-p3-source`; counterevidence IDs: `none`
- Candidate proposition: The current value for audit event authoring guidance is free-form payload.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `supersedes`
- Transition disposition: `accept`
- Expected state effect: `close_and_replace`; affected: `semantic:p3:target`; new: `semantic:p3:target:replacement`
- Expected external action: `none`; action-selection task present: `false`
- Required evidence IDs: `full-30-p3-source, full-30-p3-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-30_3

#### Checkpoints and downstream tasks

- Checkpoint `full-30-p3-checkpoint` after sequence `11`
- Task `full-30-p3-state-task` (`current_state_query`) at `full-30-p3-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p3:target', 'semantic:p3:target:replacement']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p3:target', 'proposition': 'The current value for audit event authoring guidance is free-form payload.', 'scope': {'system': 'audit-event-authoring-guidance', 'audience': 'all'}, 'status': 'revoked', 'evidence_ids': ['full-30-p3-source']}, {'semantic_item_ref': 'semantic:p3:target:replacement', 'proposition': 'The listed audit event authoring guidance value is typed payload, according to the architecture note.', 'scope': {'system': 'audit-event-authoring-guidance', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-30-p3-event']}]}`; dependencies: `full-30-p3-source, full-30-p3-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: not required

### Pair `full-30-p4-pair`

- Evaluated event: `full-30-p4-event`; context events: `full-30-p4-source`
- Candidate pool: `full-30-p4-pool`; hash: `e21d15e276f10f4d1a9ccf8ca249001727b7a7786c34a004f10be30704bc010e`; snapshots: `full-30-p4-snapshot-target, full-30-p4-snapshot-aux`
- Candidate snapshot: `full-30-p4-snapshot-target`; runtime item: `full-30-p4-runtime-target`; hash: `b4d7e207c3420d2fffe145e4e92e42c701bc405980d9ac65df973590252c0f44`
- Candidate source IDs: `full-30-p4-source`; counterevidence IDs: `none`
- Candidate proposition: The recorded value for audit event migration plan is free-form payload.
- Candidate validity: `2026-09-17T12:00:00Z` through `null`
- Semantic relationship: `contradicts`
- Transition disposition: `reject_unauthorized`
- Expected state effect: `none`; affected: `semantic:p4:target`; new: `none`
- Expected external action: `silence`; action-selection task present: `true`
- Required evidence IDs: `full-30-p4-source, full-30-p4-event`
- Adjudication note: EVALUATOR_ONLY_CANARY_full-30_4

#### Checkpoints and downstream tasks

- Checkpoint `full-30-p4-checkpoint` after sequence `12`
- Task `full-30-p4-state-task` (`current_state_query`) at `full-30-p4-checkpoint`; scope: `{'mode': 'semantic_items', 'semantic_item_refs': ['semantic:p4:target']}`; request: `{'question': 'What state is operationally valid for this evaluated item?'}`; gold: `{'current_state': [{'semantic_item_ref': 'semantic:p4:target', 'proposition': 'The recorded value for audit event migration plan is free-form payload.', 'scope': {'system': 'audit-event-migration-plan', 'audience': 'all'}, 'status': 'active', 'evidence_ids': ['full-30-p4-source']}]}`; dependencies: `full-30-p4-source, full-30-p4-event`
- Task `full-30-p4-action-task` (`action_selection`) at `full-30-p4-checkpoint`; scope: `{'mode': 'pair', 'pair_id': 'full-30-p4-pair'}`; request: `{'question': 'What action, if any, should the system take for this evaluated pair?'}`; gold: `{'action': 'silence'}`; dependencies: `full-30-p4-source, full-30-p4-event`

Pair decision: [ ] approve  [ ] revise  [ ] reject
Pair reviewer notes:

Second review: [ ] required  [ ] complete

Reviewer checks:

- [ ] Semantic label ignores authority and policy.
- [ ] Disposition correctly applies authority and validation.
- [ ] State effect follows independently from disposition.
- [ ] External action is independently justified and `none`/`silence` is used correctly.
- [ ] Candidate snapshot, source IDs, timestamps, authority, and evidence are complete.
- [ ] Checkpoint and every downstream task are correct.
- [ ] Case wording does not trivially reveal the label.

History/checkpoint decision: [ ] approve  [ ] revise  [ ] reject

Notes:


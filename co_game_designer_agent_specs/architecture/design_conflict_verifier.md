# Design Conflict Verifier Agent

## Mission
Audit proposed Balatro joker designs for conflicts with core rules, existing jokers, and economy safeguards before production commits.

## Responsibilities
- Review orchestrator-selected concepts alongside supporting synergy and balance evidence.
- Compare effects against `co_game_designer_agent_specs/all_jokers.md` and core Balatro rules to prevent duplicates or illegal interactions.
- Identify rule, economy, or UX conflicts and recommend mitigations or block adoption when necessary.
- Document a standards checklist covering scoring math, shop economy, rarity expectations, and hand limits.
- Provide a clear handoff highlighting accepted elements and items requiring redesign.

## Inputs
- Candidate joker specification packet from the lead designer orchestrator.
- Delegate outputs from synergy and balance agents when available for cross-reference.
- Canonical references such as `all_jokers.md`, Balatro rules documentation, and experiment logs.

## Outputs
- Verification summary stating overall readiness and major risks.
- Structured conflict findings with severity, impacted systems, and concrete resolutions or blockers.
- Checklist results showing which policy areas passed, failed, or need attention.
- List of validated aspects that remain safe to move forward.
- Optional notes guiding follow-up work or further experimentation.

## Downstream Handoff
Returns conflict assessment to the orchestrator, enabling reruns of ideation or balance passes and preventing problematic designs from advancing.

## Collaboration Graph
- Receives dossiers from `lead_designer_orchestrator_agent` once candidate specs are drafted.
- References synergy and simulator data without directly invoking those agents.
- Feeds confirmed blockers back to the orchestrator, who may loop with `creativity_generator_agent` or retire concepts.

## Prompt & Schema Crosswalk
- Prompt requires explicit conflict categorization; schema captures this via `conflictFindings` with `conflictType`, `severity`, and `resolutionRecommendation`.
- Checklist instructions map to `policyChecklist`, storing `checkId`, `description`, `status`, and `notes` values.
- Approved elements appear in `validatedAspects` with identifiers aligning to orchestrator fields.
- Any blocked concept IDs populate `blockedItems`, providing a machine-readable filter for the orchestrator.
- Narrative recap aligns with `verificationSummary` and optional `validationNotes` array for supporting commentary.

## n8n Implementation Notes
- Agent definition will be stored at `co_game_designer_agent_specs/agent_definitions/design_conflict_verifier_agent.json`.
- System prompt resides in `prompts/design_conflict_verifier_agent.txt` with schema at `schemas/design_conflict_verifier_agent.json`.
- Workflow node should execute after the orchestrator drafts a spec and before final handoff, consuming orchestrator output plus delegate references.

## Manual Test Notes
1. Evaluate baseline, synergy-heavy, and busted scenario dossiers to confirm conflicts surface with appropriate severities.
2. Ensure `policyChecklist` covers scoring math, rarity, shop economy, and rule compliance; statuses must be `pass`, `fail`, or `attention`.
3. Confirm optional arrays (`validationNotes`, `blockedItems`, `validatedAspects`) default to `[]` and that at least one finding references a joker from `all_jokers.md` when overlap exists.

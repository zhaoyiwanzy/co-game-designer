# Lead Designer Orchestrator Agent

## Mission
Coordinate Balatro card-design sprints by translating a high-level brief into actionable tasks for specialist agents, fusing their analyses into a cohesive joker or deck feature specification ready for playtesting.

## Responsibilities
- Parse the product brief, distill success criteria, and flag scope assumptions.
- Sequence work for subordinate agents: solicit synergy scouting, statistical balancing, and risk validation reports.
- Reconcile conflicting recommendations, documenting rationale and trade-offs for stakeholders.
- Package the final design packet with follow-up work items and harness inputs for dry runs.

## Inputs
- Design brief describing gameplay goal, target deck archetype, or joker concept.
- Repository references such as prior joker specs, numerical constraints, or player feedback notes.

## Outputs
- Consolidated design dossier including user story, synergy highlights, balancing directives, and validation hooks.
- Delegation log that captures prompts sent to subordinate agents and how their outputs were consumed.
- Open questions or risks that require additional research or future automation.

## Downstream Handoff
Delivers the dossier to production-focused teams (e.g., implementation or QA) and archives tool prompts in `/experiments` when further tuning is required.

## Collaboration Graph
- Calls `joker_synergy_specialist_agent` to enumerate viable chip/multiplier combos and cross-archetype interactions.
- Calls `run_balance_simulator_agent` to stress-test recommended builds across baseline, synergy-focused, and busted runs.
- Optionally iterates with human designer feedback, updating constraints before re-querying specialists.

## Prompt & Schema Crosswalk
- Ensure every directive for subordinate usage is mirrored by `delegationLog` entries in the schema.
- Require the dossier sections (mission recap, synergy plan, balance plan, validation plan) that map to `designSummary`, `synergyPlan`, `balancePlan`, and `validationHooks` fields.
- Instruct the orchestrator to reference `packageId` values from the synergy specialist when populating `synergyPlan` decisions.
- Explicitly mention risk tracking in the prompt so the `openRisks` array is always considered.

## Manual Test Notes
1. Run harness dry-runs with baseline, synergy-heavy, and busted decks, verifying the orchestrator requests matching reports from both subordinate agents.
2. Confirm optional arrays such as `openRisks` default to `[]` when not populated.
3. Validate that the orchestrator’s summary references each subordinate output and adopted `packageId` by identifier to preserve traceability.

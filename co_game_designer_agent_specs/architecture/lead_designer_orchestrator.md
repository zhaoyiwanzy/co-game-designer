# Lead Designer Orchestrator Agent

## Mission
Coordinate Balatro card-design sprints by translating a high-level brief into actionable tasks for specialist agents, fusing their analyses into a cohesive joker or deck feature specification ready for playtesting.

## Responsibilities
- Parse the product brief, distill success criteria, and flag scope assumptions.
- Sequence work for subordinate agents: solicit synergy scouting, statistical balancing, and risk validation reports.
- Reconcile conflicting recommendations, documenting rationale and trade-offs for stakeholders.
- Finalize a concrete joker spec with pricing, rarity, and effect text anchored in delegate evidence.
- Package the final design packet with follow-up work items and harness inputs for dry runs.

## Inputs
- Design motivation, inspiration snippet, or an empty brief from stakeholders.
- Repository references such as prior joker specs, numerical constraints, or player feedback notes.

## Outputs
- Concrete joker specification with effect, rarity, economy tuning, and justification.
- Consolidated design dossier including user story, synergy highlights, balancing directives, and validation hooks.
- Delegation log that captures prompts sent to subordinate agents and how their outputs were consumed.
- Open risk log that records riskId, severity, owner, and notes for every outstanding concern.

## Downstream Handoff
Delivers the dossier to production-focused teams (e.g., implementation or QA) and archives tool prompts in `/experiments` when further tuning is required.

## Collaboration Graph
- Calls `joker_synergy_specialist_agent` to enumerate viable chip/multiplier combos and cross-archetype interactions.
- Calls `run_balance_simulator_agent` to stress-test recommended builds across baseline, synergy-focused, and busted runs.
- Optionally iterates with human designer feedback, updating constraints before re-querying specialists.

## Prompt & Schema Crosswalk
- Ensure every directive for subordinate usage is mirrored by `delegationLog` entries in the schema.
- Require the dossier sections (mission recap, synergy plan, balance plan, validation plan).
  Map them to `designSummary`, `synergyPlan`, `balancePlan`, `validationHooks`, and `jokerSpec` fields.
- Instruct the orchestrator to reference `packageId` values from the synergy specialist when populating
  `synergyPlan` decisions.
- Explicitly call for `openRisks` entries with severity, owner, notes, and `riskId` so follow-ups remain accountable.

## n8n Implementation Notes
- Agent definition: `co_game_designer_agent_specs/agent_definitions/lead_designer_orchestrator_agent.json`.
- System prompt ships with an embedded Balatro rules reference that matches the workflow's knowledge block.
- `responseFormat` enforces strict adherence to `lead_designer_orchestrator_agent.json`.
- `delegateAgents` field mirrors runtime calls to synergy and balance specialists for orchestration tooling.

## Manual Test Notes
1. Run harness dry-runs with baseline, synergy-heavy, and busted decks, verifying the orchestrator requests matching reports from both subordinate agents.
2. Confirm optional arrays such as `openRisks` default to `[]` when not populated.
3. Validate that the orchestrator’s summary references each subordinate output and adopted `packageId` by identifier to preserve traceability.
4. Ensure the `jokerSpec` block contains an effect sentence, economy tuning, and clear justification tied to delegate evidence.

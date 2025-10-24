# Lead Designer Orchestrator Agent

## Mission
Coordinate Balatro card-design sprints by translating a high-level brief into actionable tasks for specialist agents, fusing their analyses into a cohesive joker or deck feature specification ready for playtesting.

## Responsibilities
- Parse the product brief, distill success criteria, and flag scope assumptions.
- Orchestrate subordinate agents end-to-end: capture ideation seeds, run synergy scouting, balance simulations, and verification checks.
- Reconcile conflicting recommendations, documenting rationale and trade-offs for stakeholders.
- Finalize a concrete joker spec with pricing, rarity, and effect text anchored in delegate evidence.
- Package the final design packet with follow-up work items and harness inputs for dry runs.
- Close the loop with verification outcomes, ensuring blocked items feed back into ideation or balance reruns.

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
- Calls `creativity_generator_agent` to gather divergent concept seeds before selecting a primary direction.
- Calls `joker_synergy_specialist_agent` to enumerate viable chip/multiplier combos and cross-archetype interactions.
- Calls `run_balance_simulator_agent` to stress-test recommended builds across baseline, synergy-focused, and busted runs.
- Calls `design_conflict_verifier_agent` to block conflicting mechanics and populate verification follow-ups.
- Optionally iterates with human designer feedback, updating constraints before re-querying specialists.

## Workflow Representation
- `co_game_designer_agent_specs/workflows/co_designer_workflow_manifest.json` enumerates the orchestrator, delegate tools, and trigger nodes.
- Each agent entry declares the prompt path, schema path, model tuning, and downstream edges so updates stay version-controlled.
- The manifest feeds `scripts/export_n8n_workflow.py`, which composes the deployable `co-designer-workflow.json`.
- Regenerate the workflow json after manifest edits to keep the repository and the n8n deployment in sync.
- Document dry-run notes and handoff expectations here whenever delegate ordering or data contracts change.

## Prompt & Schema Crosswalk
- Ensure every directive for subordinate usage is mirrored by `delegationLog` entries in the schema.
- Require the dossier sections (mission recap, concept plan, synergy plan, balance plan, verification plan, validation plan).
  Map them to `designSummary`, `conceptPlan`, `synergyPlan`, `balancePlan`, `verificationPlan`, `validationHooks`, and `jokerSpec` fields.
- Instruct the orchestrator to reference `ideaId` values from the creativity generator and `packageId` values from the synergy specialist when populating
  `conceptPlan.selectedIdeas` and `synergyPlan` decisions.
- Explicitly call for `openRisks` entries with severity, owner, notes, and `riskId` so follow-ups remain accountable.
- Require `verificationPlan` to echo the verifier's status, blocked items, and follow-up actions.

## n8n Implementation Notes
- Agent definition: `co_game_designer_agent_specs/agent_definitions/lead_designer_orchestrator_agent.json`.
- System prompt ships with an embedded Balatro rules reference that matches the workflow's knowledge block.
- `responseFormat` enforces strict adherence to `lead_designer_orchestrator_agent.json`.
- `delegateAgents` field now lists creativity, synergy, simulation, and verification agents in execution order.
- Workflow wiring should place the creativity node upstream, funnel its output into the orchestrator, and branch to verification after the dossier is drafted.

## Manual Test Notes
1. Run harness dry-runs with baseline, synergy-heavy, and busted decks, verifying the orchestrator requests creativity, synergy, balance, and verification passes in order.
2. Confirm optional arrays such as `openRisks`, `conceptPlan.selectedIdeas`, and `verificationPlan.followUpActions` default to `[]` when not populated.
3. Validate that `conceptPlan` references generator `ideaId` values, `synergyPlan` references specialist `packageId` values, and `verificationPlan.blockedItems` mirrors verifier output.
4. Ensure the `jokerSpec` block contains an effect sentence, economy tuning, justification tied to delegate evidence, and that verification verdicts feed into updated risks.

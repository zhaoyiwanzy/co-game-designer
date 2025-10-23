# Joker Synergy Specialist Agent

## Mission
Surface the most compelling Balatro joker synergies for a proposed card concept, quantifying chip and multiplier trajectories while respecting rarity, economy, and hand-type constraints.

## Responsibilities
- Interpret the design brief and orchestrator context to scope relevant jokers, tarot, and planet interactions.
- Produce a ranked list of synergy packages with expected chip/multiplier deltas and enabling requirements.
- Flag incompatibilities or diminishing returns that the orchestrator should communicate downstream.

## Inputs
- Orchestrator-supplied design context including target archetype, desired player fantasy, and any banned components.
- Historical performance data or reference tables when provided via `/experiments`.

## Outputs
- Structured synergy report detailing packages, statistical expectations, and setup steps.
- Risk notes describing fragile combos, lock pieces, or balance watch-outs.
- References to supporting research or experiments for traceability.

## Downstream Handoff
Returns its report to the lead designer orchestrator, who integrates the ranking into the final design dossier and signals any required simulations.

## Prompt & Schema Crosswalk
- Require each synergy package to include `packageId`, `name`, `description`, `expectedChips`, `expectedMultiplier`, `enablingCards`, and `tuningNotes` so every schema field is covered.
- Explicitly mention the need for global observations and research references, tying to `globalObservations` and `supportingResearch` fields.
- Emphasize risk articulation in the prompt to fulfill the `risks` array.

## n8n Implementation Notes
- Agent definition: `co_game_designer_agent_specs/agent_definitions/joker_synergy_specialist_agent.json`.
- Strict JSON output is enforced via the embedded schema reference for workflow validation.
- No delegate agents are declared, aligning with direct request-response usage in n8n.

## Manual Test Notes
1. Feed baseline, synergy-heavy, and busted deck briefs to ensure ranking logic adapts to resource availability.
2. Verify that numeric estimates stay within Balatro limits and that optional arrays return `[]` when no data is available.
3. Confirm cross-agent traceability by checking that `packageId` values and `supportingResearch` identifiers align with orchestrator delegation logs.

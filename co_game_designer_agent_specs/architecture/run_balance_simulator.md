# Run Balance Simulator Agent

## Mission
Stress-test proposed Balatro joker or deck updates across multiple run archetypes, surfacing pacing issues, economy breaks, and failure points before implementation.

## Responsibilities
- Translate orchestrator directives into scenario setups covering baseline, synergy-focused, and busted draws.
- Estimate chip gain, multiplier growth, money flow, and survivability across ante milestones.
- Highlight probability spikes, variance, and degenerate loops that require balance mitigation.

## Inputs
- Orchestrator dossier extract specifying proposed joker effects, deck archetype, and synergy priorities.
- Relevant synergy reports or experimental datasets referenced by the orchestrator.

## Outputs
- Scenario-by-scenario metrics with recommended mitigation levers (e.g., price increases, rarity adjustments).
- Aggregate risk assessment with severity tags and suggested next steps.
- Simulation metadata capturing assumptions, RNG seeds (if provided), and gaps needing manual verification.

## Downstream Handoff
Sends the simulation digest back to the lead designer orchestrator and flags any high-severity risks that should loop the synergy specialist back in for adjustments.

## Prompt & Schema Crosswalk
- Ensure each scenario entry records `scenarioName`, `anteProgression`, `chipTrajectory`, `multiplierTrajectory`, `economySummary`, `probabilityEstimate`, and `riskNotes` per the schema.
- Require the prompt to gather global balance verdicts and mitigation ideas for `balanceVerdict` and `mitigationIdeas` fields.
- Mention simulation metadata explicitly so `simulationMetadata` is always populated with assumptions and tool versions.

## Manual Test Notes
1. Dry-run the agent with baseline, synergy-heavy, and busted setups, confirming metrics scale appropriately, probability labels make sense, and values stay within Balatro bounds.
2. Check that empty optional arrays (e.g., `mitigationIdeas`) default to `[]` when no actions are needed.
3. Validate cross-agent loop by ensuring high-severity risks trigger a note referencing the synergy specialist report ID.

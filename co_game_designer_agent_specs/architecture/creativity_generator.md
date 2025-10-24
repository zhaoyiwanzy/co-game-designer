# Creativity Generator Agent

## Mission
Surface divergent Balatro joker concept seeds that align with the current brief while avoiding overlap with the existing roster.

## Responsibilities
- Parse the lead designer brief to extract fantasy, constraints, and mechanical focus areas.
- Generate 3-5 distinct joker concepts with clear gameplay hooks and rarity targets.
- Cite adjacent entries from `co_game_designer_agent_specs/all_jokers.md` to show awareness of nearby mechanics.
- Flag novelty risks or prerequisite mechanics so downstream specialists can validate feasibility early.
- Hand off prepared notes that the orchestrator can feed into synergy, balance, and verification agents.

## Inputs
- High-level brief or design goal supplied by the orchestrator or human designer.
- Optional guardrails such as banned mechanics, rarity limits, or economy requirements.
- Repository references including `all_jokers.md`, prior design dossiers, or experiment notes.

## Outputs
- Ideation summary outlining the opportunity space and recommended direction of exploration.
- Structured list of idea seeds with identifiers, pitches, mechanical levers, and rarity expectations.
- Catalog of inspiration sources referencing joker precedents, design notes, or metagame observations.
- Open questions that need clarification before greenlighting deeper analysis.

## Downstream Handoff
Shares `ideaSeeds` and supporting context with the lead designer orchestrator, who selects candidates for deeper synergy, balance, and verification passes.

## Collaboration Graph
- Receives prompts from `lead_designer_orchestrator_agent` and returns structured ideation output.
- Provides seed identifiers referenced later by `joker_synergy_specialist_agent` and `design_conflict_verifier_agent`.
- Consults static knowledge such as `all_jokers.md` but does not call other agents directly.

## Prompt & Schema Crosswalk
- Prompt demands 3-5 concept seeds; schema enforces `ideaSeeds` array with required concept metadata and rarity.
- Instructed to cite adjacent jokers; schema captures these via `referenceJokers` within each seed and `inspirationSources` entries.
- Novelty callouts and open clarifications map to `noveltyHook`, `riskFlags`, and top-level `openQuestions` arrays.
- Handoff guidance is captured by `handoffNotes` on each seed for orchestrator planning.

## n8n Implementation Notes
- Agent definition will live at `co_game_designer_agent_specs/agent_definitions/creativity_generator_agent.json`.
- System prompt references `prompts/creativity_generator_agent.txt` and returns JSON per `schemas/creativity_generator_agent.json`.
- Node should precede synergy and balance specialists in `co-designer-workflow.json`, feeding its output into later branches.

## Manual Test Notes
1. Run baseline, synergy-heavy, and busted deck briefs to confirm 3-5 seeds with distinct `divergentAxes` coverage.
2. Verify optional arrays (`primaryMechanics`, `referenceJokers`, `riskFlags`, `openQuestions`) default to `[]` when empty.
3. Ensure each seed includes at least one citation or rationale tying back to `all_jokers.md` or documented experiments.

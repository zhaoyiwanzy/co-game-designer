# Repository Guidelines

## Project Structure & Module Organization
Treat `co_scientist_agent_specs/` as the reference pattern and mirror its layout inside `co_game_designer_agent_specs/`. Keep architecture notes in `architecture/` (one Markdown per agent, e.g., `architecture/joker_synergist.md`), prompts in `prompts/`, schemas in `schemas/`, and optional combo guidance in `playbooks/`. Park experimental assets such as mock cards or stat tables in `/experiments` outside the specs tree to avoid clutter.

## Architecture & Authoring Workflow
Update the architecture doc first to capture the agent mission, downstream handoff, and manual test notes. Write prompts in imperative, second-person voice with lines ≤120 characters and uppercase tool identifiers like `BALATRO_SYNERGY_LOOKUP`. Define schemas with two-space indentation, sorted property keys, descriptive camelCase fields (e.g., `expectedMultiplier`), and include sample values with validation rules. Crosswalk the prompt and schema so every output field is described in both before moving on.

## Build, Test, and Development Commands
Run `jq empty co_game_designer_agent_specs/schemas/*.json` before committing to guarantee valid JSON. Use `python -m json.tool < file.json` when you need a readable diff during reviews. `rg "joker" co_game_designer_agent_specs/prompts` keeps terminology consistent, and `rg "TODO"` highlights unfinished authoring work.

## Coding Style & Naming Conventions
Default to ASCII content and add succinct comments only when clarifying non-obvious logic. Name schema and prompt files with the agent scope plus `_agent` suffix (e.g., `hand_simulator_agent.json`) so handoffs stay traceable. Reserve uppercase strictly for tool identifiers and keep other identifiers in descriptive camelCase.

## Testing Guidelines
Dry-run every agent in the orchestration harness across baseline, synergy-heavy, and busted deck scenarios, confirming optional arrays default to `[]` and numeric outputs stay within Balatro limits. Validate that cross-agent handoffs satisfy the schema contract and record manual test coverage in the architecture note for future automation.

## Commit & Pull Request Guidelines
Write present-tense commit summaries such as `feat: outline joker evaluator agent`, bundling related architecture, prompt, and schema edits. PR descriptions should restate the gameplay goal, list impacted agents, link supporting Balatro research, and attach harness logs or screenshots validating key joker recommendations.

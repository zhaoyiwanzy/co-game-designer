# Repository Guidelines

## Project Structure & Module Organization
Treat `co_scientist_agent_specs/` as the reference implementation. New Balatro work belongs under `co_game_designer_agent_specs/`, mirroring the structure `prompts/`, `schemas/`, and optional `playbooks/` for combo notes. Store agent architecture drafts in `co_game_designer_agent_specs/architecture/`, one Markdown file per agent role (e.g., `joker_synergist.md`). Keep experimental assets—card mockups, statistical tables—in a separate `/experiments` folder outside the specs tree to prevent clutter.
The shared n8n workflow now lives at `co_game_designer_agent_specs/co-designer-workflow.json`; keep this file updated with the latest orchestration wiring.
Treat `co_game_designer_agent_specs/workflows/co_designer_workflow_manifest.json` as the canonical wiring description and regenerate the workflow json from it after any model, prompt, or agent linkage updates.

## Architecture & Authoring Workflow
For each proposed agent: 1) capture its mission and downstream handoff in an architecture doc; 2) draft the prompt with explicit Balatro context (chips, mult multipliers, synergies); 3) define an aligned JSON schema listing every expected field, sample values, and validation rules; 4) crosswalk the prompt and schema to confirm every output is described. When updating an existing agent, revise the architecture note first so project-wide diagrams stay accurate.

## Build, Test, and Development Commands
Run `jq empty co_game_designer_agent_specs/schemas/*.json` before committing to guarantee valid JSON. Use `python -m json.tool < file.json` for readable diffs during reviews. `rg "joker" co_game_designer_agent_specs/prompts` helps ensure consistent card terminology, while `rg "TODO"` surfaces unfinished authoring work.
Run `python scripts/export_n8n_workflow.py` after manifest changes to refresh the deployable workflow artifact.

## Coding Style & Naming Conventions
Keep prompts imperative, second-person, and capped at 120 characters per line. Reserve uppercase for tool identifiers (e.g., `BALATRO_SYNERGY_LOOKUP`). Schemas use two-space indentation, sorted property keys, and descriptive camelCase for field names (`expectedMultiplier`). Name files with the agent scope plus `_agent` suffix (`hand_simulator_agent.json`).

## Testing Guidelines
Dry-run each agent in the orchestration harness with at least three Balatro deck scenarios—baseline, synergy-heavy, and edge-case busted runs. Confirm optional arrays default to `[]`, numeric outputs stay within game limits, and cross-agent handoffs match schema contracts. Document manual test notes in the architecture file for future automation.

## Commit & Pull Request Guidelines
Write present-tense commit summaries such as `feat: outline joker evaluator agent`. Bundle architecture, prompt, and schema edits that belong together. PR descriptions should restate the gameplay goal, list affected agents, link to supporting Balatro research, and include harness logs or screenshots validating key joker recommendations.

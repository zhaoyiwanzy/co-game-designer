#!/usr/bin/env python3
import argparse
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any


UUID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "co-game-designer/auto-deployment")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text if text.endswith("\n") else text + "\n"


def uuid_for(*parts: str) -> str:
    name = "::".join(parts)
    return str(uuid.uuid5(UUID_NAMESPACE, name))


def add_connection(
    graph: Dict[str, Dict[str, List[List[Dict[str, Any]]]]],
    source: str,
    source_port: str,
    target: str,
    target_port: str,
) -> None:
    port_map = graph.setdefault(source, {})
    edge_sets = port_map.setdefault(source_port, [[]])
    edge_sets[0].append({"node": target, "type": target_port, "index": 0})


def ensure_expression(text: str) -> str:
    stripped = text.lstrip()
    return text if stripped.startswith("=") else f"={text}"


def build_positions(orchestrator_id: str, tool_order: List[str]) -> Dict[str, List[int]]:
    positions: Dict[str, List[int]] = {
        "trigger": [0, 0],
        f"{orchestrator_id}::agent": [320, 0],
        f"{orchestrator_id}::lm": [80, -120],
        f"{orchestrator_id}::parser": [560, 0],
    }
    for index, agent_id in enumerate(tool_order, start=1):
        y_base = index * 240
        positions[f"{agent_id}::lm"] = [80, y_base - 120]
        positions[f"{agent_id}::tool"] = [320, y_base]
        positions[f"{agent_id}::parser"] = [560, y_base]
    return positions


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export the co-designer workflow manifest into an n8n workflow json file.",
    )
    parser.add_argument(
        "--manifest",
        default="co_game_designer_agent_specs/workflows/co_designer_workflow_manifest.json",
        help="Path to the workflow manifest json.",
    )
    parser.add_argument(
        "--output",
        default="co_game_designer_agent_specs/co-designer-workflow.json",
        help="Destination path for the generated n8n workflow.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()

    manifest = load_json(manifest_path)
    agents: List[Dict[str, Any]] = manifest.get("agents", [])

    orchestrator = next(
        (agent for agent in agents if agent.get("type") == "orchestrator"), None
    )
    if orchestrator is None:
        raise ValueError("Manifest must declare an orchestrator agent.")

    tool_agents = {
        agent["id"]: agent for agent in agents if agent.get("type") == "tool"
    }

    delegate_order = orchestrator.get("delegateOrder", [])
    missing = [agent_id for agent_id in delegate_order if agent_id not in tool_agents]
    if missing:
        raise ValueError(f"Delegate order references unknown agents: {missing}")

    positions = build_positions(orchestrator["id"], delegate_order)

    credentials = manifest.get("credentials", {})
    openai_credentials = credentials.get("openAiApi")

    nodes: List[Dict[str, Any]] = []
    connections: Dict[str, Dict[str, List[List[Dict[str, Any]]]]] = {}

    def load_schema(schema_path: str) -> str:
        schema = load_json(Path(schema_path).resolve())
        return json.dumps(schema, indent=2)

    # Build tool nodes
    for agent_id in delegate_order:
        agent_manifest = tool_agents[agent_id]
        definition = load_json(Path(agent_manifest["agentDefinition"]).resolve())
        prompt_text = read_text(Path(agent_manifest["promptPath"]).resolve())
        schema_text = load_schema(agent_manifest["schemaPath"])
        lm_cfg = agent_manifest.get("languageModel", {})

        lm_node_name = f"lm__{agent_id}"
        parser_node_name = f"parser__{agent_id}"

        nodes.append(
            {
                "id": uuid_for(lm_node_name),
                "name": lm_node_name,
                "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
                "typeVersion": 1.2,
                "position": positions[f"{agent_id}::lm"],
                "parameters": {
                    "model": {
                        "__rl": True,
                        "mode": "list",
                        "value": lm_cfg.get("name", "gpt-5"),
                        "cachedResultName": lm_cfg.get("name", "gpt-5"),
                    },
                    "options": {
                        **(
                            {"reasoningEffort": lm_cfg["reasoningEffort"]}
                            if lm_cfg.get("reasoningEffort")
                            else {}
                        ),
                        **(
                            {"maxTokens": lm_cfg["maxTokens"]}
                            if "maxTokens" in lm_cfg
                            else {}
                        ),
                        **(
                            {"timeout": lm_cfg["timeoutMs"]}
                            if lm_cfg.get("timeoutMs")
                            else {}
                        ),
                    },
                },
                **(
                    {"credentials": {"openAiApi": openai_credentials}}
                    if openai_credentials
                    else {}
                ),
            }
        )

        nodes.append(
            {
                "id": uuid_for(parser_node_name),
                "name": parser_node_name,
                "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
                "typeVersion": 1.3,
                "position": positions[f"{agent_id}::parser"],
                "parameters": {
                    "schemaType": "manual",
                    "inputSchema": schema_text,
                },
            }
        )

        nodes.append(
            {
                "id": uuid_for(agent_id),
                "name": agent_id,
                "type": "@n8n/n8n-nodes-langchain.agentTool",
                "typeVersion": 2.2,
                "position": positions[f"{agent_id}::tool"],
                "parameters": {
                    "hasOutputParser": True,
                    "options": {},
                    "text": ensure_expression(prompt_text),
                    "toolDescription": definition.get(
                        "description",
                        f"{agent_id} generated via manifest.",
                    ),
                },
            }
        )

        add_connection(connections, parser_node_name, "ai_outputParser", agent_id, "ai_outputParser")
        add_connection(connections, lm_node_name, "ai_languageModel", agent_id, "ai_languageModel")
        add_connection(
            connections,
            agent_id,
            "ai_tool",
            orchestrator["id"],
            "ai_tool",
        )

    # Build orchestrator nodes
    orchestrator_prompt = read_text(Path(orchestrator["promptPath"]).resolve())
    orchestrator_schema = load_schema(orchestrator["schemaPath"])
    orchestrator_lm_cfg = orchestrator.get("languageModel", {})

    orchestrator_lm_name = f"lm__{orchestrator['id']}"
    orchestrator_parser_name = f"parser__{orchestrator['id']}"

    nodes.append(
        {
            "id": uuid_for(orchestrator_lm_name),
            "name": orchestrator_lm_name,
            "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
            "typeVersion": 1.2,
            "position": positions[f"{orchestrator['id']}::lm"],
            "parameters": {
                "model": {
                    "__rl": True,
                    "mode": "list",
                    "value": orchestrator_lm_cfg.get("name", "gpt-5"),
                    "cachedResultName": orchestrator_lm_cfg.get("name", "gpt-5"),
                },
                "options": {
                    **(
                        {"reasoningEffort": orchestrator_lm_cfg["reasoningEffort"]}
                        if orchestrator_lm_cfg.get("reasoningEffort")
                        else {}
                    ),
                    **(
                        {"maxTokens": orchestrator_lm_cfg["maxTokens"]}
                        if "maxTokens" in orchestrator_lm_cfg
                        else {}
                    ),
                    **(
                        {"timeout": orchestrator_lm_cfg["timeoutMs"]}
                        if orchestrator_lm_cfg.get("timeoutMs")
                        else {}
                    ),
                },
            },
            **(
                {"credentials": {"openAiApi": openai_credentials}}
                if openai_credentials
                else {}
            ),
        }
    )

    nodes.append(
        {
            "id": uuid_for(orchestrator_parser_name),
            "name": orchestrator_parser_name,
            "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
            "typeVersion": 1.3,
            "position": positions[f"{orchestrator['id']}::parser"],
            "parameters": {
                "schemaType": "manual",
                "inputSchema": orchestrator_schema,
            },
        }
    )

    orchestrator_node = {
        "id": uuid_for(orchestrator["id"]),
        "name": orchestrator["id"],
        "type": "@n8n/n8n-nodes-langchain.agent",
        "typeVersion": 2.2,
        "position": positions[f"{orchestrator['id']}::agent"],
        "parameters": {
            "promptType": "define",
            "text": orchestrator.get("inputTemplate", "=Design request:\\n\\n{{ $json.chatInput}}\\n"),
            "hasOutputParser": True,
            "options": {
                "systemMessage": orchestrator_prompt,
            },
        },
        "retryOnFail": True,
        "waitBetweenTries": 100,
    }
    nodes.append(orchestrator_node)

    add_connection(
        connections,
        orchestrator_parser_name,
        "ai_outputParser",
        orchestrator["id"],
        "ai_outputParser",
    )
    add_connection(
        connections,
        orchestrator_lm_name,
        "ai_languageModel",
        orchestrator["id"],
        "ai_languageModel",
    )

    # Trigger node
    trigger_manifest = manifest.get("trigger", {})
    trigger_node = {
        "id": uuid_for("chat_trigger"),
        "name": trigger_manifest.get("name", "When chat message received"),
        "type": "@n8n/n8n-nodes-langchain.chatTrigger",
        "typeVersion": 1.3,
        "position": positions["trigger"],
        "parameters": {"options": trigger_manifest.get("options", {})},
        "webhookId": trigger_manifest.get("webhookId"),
    }
    nodes.append(trigger_node)

    add_connection(
        connections,
        trigger_node["name"],
        "main",
        orchestrator["id"],
        "main",
    )

    workflow_meta = manifest.get("workflow", {})
    n8n_meta = workflow_meta.get("n8n", {})
    workflow_json = {
        "name": workflow_meta.get("name", "co-designer"),
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "active": False,
        "settings": {"executionOrder": "v1"},
        "versionId": n8n_meta.get("versionId"),
        "meta": {
            "templateCredsSetupCompleted": True,
            "instanceId": n8n_meta.get("instanceId"),
        },
        "id": n8n_meta.get("id"),
        "tags": [],
    }

    output_path.write_text(json.dumps(workflow_json, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

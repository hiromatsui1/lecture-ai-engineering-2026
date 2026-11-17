# Copilot instructions for AIE2026

## Project overview

This repository is the course repo for the AI Engineering practice lectures (AIE2026). It is intentionally small and learning-focused: most work happens in a few Python modules and JSON/Markdown course data rather than a large application framework.

Core structure:
- `app/`: executable lecture exercises and agent code.
  - `config.py`: shared configuration and API-key/model helpers; users should not hardcode secrets here.
  - `ask.py`: the Week 1 baseline script that sends one prompt to the Gemini model.
  - `tools.py`: tool implementations for glossary lookup and lecture summaries; the tool docstrings and type hints are part of the model contract.
  - `agent.py`: the Pydantic AI agent that wires tools into a model loop and optionally connects to MCP tools.
  - `mcp_server.py`: exposes the glossary/lecture tools through an MCP server.
  - `mcp_servers.json`: MCP client configuration in the standard `mcpServers` format.
- `data/`: course material used by the agent, especially `data/glossary.json` and `data/lectures/*.md`.
- `lectures/NN/`: per-lecture problem and answer files; most course assignments are written here.
- `tests/`: API-free validation of tool registration and MCP wiring by using `pydantic_ai.models.test.TestModel`.
- `scripts/`: helper scripts for dataset generation and related utilities.

The big-picture pattern is: course content lives in `data/` and `lectures/`, while `app/` is where the teaching agent is built and exercised. The agent behavior is intentionally tool-driven: glossary lookup and lecture summaries are the main “grounding” mechanisms.

## Setup and validation commands

Use `uv` for all project commands so dependency versions stay aligned with the locked environment.

```bash
# Install dependencies from the lockfile
uv sync --frozen

# Run the full test suite
uv run pytest -q

# Run one specific test file
uv run pytest tests/test_agent.py -q
uv run pytest tests/test_mcp_server.py -q

# Run a single test by name (when needed)
uv run pytest tests/test_agent.py -q -k glossary

# Run the baseline one-shot ask flow
uv run python -m app.ask "LoRAとは何ですか？"

# Inspect the agent's available tools without calling the real API
uv run python -m app.agent --list-tools

# Run the agent against the real Gemini API (requires GEMINI_API_KEY)
uv run python -m app.agent "AIE2026の講座で使う『lecNN-start タグ』とは何ですか？"

# Run the agent with MCP tools enabled
uv run python -m app.agent --mcp --trace "LoRAとは？"
```

There is no dedicated lint/format command configured in `pyproject.toml`; validation for this repo is primarily through `pytest` and the built-in app entrypoints.

## Key conventions

- Python 3.12 is the target runtime and the project is intentionally version-pinned via `uv.lock`; do not casually upgrade dependencies during the course.
- Secrets and model selection are environment-driven, not hardcoded. Use `GEMINI_API_KEY` and optionally `AIE_MODEL`.
- The code assumes `uv run ...` is the default execution model; avoid bare `python` unless you intentionally need a different environment.
- Tool discovery is model-facing: in `app/tools.py`, docstrings and type hints become the tool description that the model sees. If a tool description is wrong or vague, the agent behavior changes.
- The repository is designed to avoid real API calls during tests. `tests/` uses `TestModel`, and MCP tests verify tool exposure without live LLM calls.
- The MCP server config is intentionally kept in `app/mcp_servers.json` in the standard `mcpServers` shape, so the same tool setup can be reused by app code and external clients.
- The course encourages a “grounded answer” workflow: before answering lecture- or glossary-specific questions, the agent should prefer `search_glossary` / lecture summary tools rather than guessing from general knowledge.

## Safe editing guidance

- Keep lecture materials under `data/` and `lectures/` aligned with the course content; these are not generic app assets.
- If you add or change a tool function in `app/tools.py`, consider whether `app/mcp_server.py` and `app/agent.py` also need to reflect that change.
- When modifying the agent or tool behavior, prefer a small, traceable change and validate it with the relevant `tests/` entry or a focused CLI check.
- Do not commit API keys or raw secrets in code, config files, or logs.

## Relevant project files

When answering “how does this project work?” or making broad edits, read these together instead of isolated files:
- `README.md` for the course setup and environment expectations.
- `pyproject.toml` for the Python version and dependency constraints.
- `app/config.py` + `app/ask.py` for the baseline LLM call pattern.
- `app/tools.py` + `app/agent.py` for the actual agent/tool loop.
- `app/mcp_server.py` + `app/mcp_servers.json` for MCP wiring.
- `tests/test_agent.py` and `tests/test_mcp_server.py` for expected tool behavior.

# Sandbox runner

Offline starter code for two supervised agents, Eve and Edos. They plan, hand work to each other, and recover from failure inside a mock survival world. The default policy is a deterministic script. No model provider is called.

Real-game connection is disabled. The runner will not open a game client, read game memory, intercept packets, automate input, or touch game files. `sietch/guard.py` refuses any mode other than `sandbox`, and it still refuses if `REAL_GAME_CONNECTION_ENABLED` is flipped to true, because there is no connector behind that flag.

## Quickstart

From this directory, with Python 3.11 or newer:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m sietch.session --config configs/sandbox.yaml --operator-present
```

`pytest` runs the unit tests. The session command runs registered scenario v1 for 16 steps and writes a JSONL log under `sessions/`. That directory is gitignored. Passing `--operator-present` is required. It is how the caller confirms a human operator is at the session. The config file has to agree (`supervisor.human_present: true`). If either flag is missing, the process exits with status 2 and writes no log.

Compare the retry policy on the same world:

```bash
python -m sietch.session --config configs/sandbox-retry.yaml --operator-present
```

From the repository root, `python -m pytest` also works. The root `pytest.ini` adds `scripts/` to the import path.

## What a run does

1. The guard checks that the config mode is `sandbox` and that `real_game_connection` is false.
2. The supervisor checks that a human operator is present.
3. Eve starts with the goal `maintain`. The scripted policy can hand Edos a repair task, gather water, or scout.
4. A handoff is accepted only when the record includes the sender, receiver, goal, reason, world snapshot, open commitments, and failure history. Empty lists count as present. A missing field is rejected, the owner does not change, and the world takes a rest step.
5. At most one handoff is accepted on a given observation, so the two agents cannot bounce a task forever.
6. Actions named in `supervisor.approval_required` stop at the approval gate. The default decision is to deny them and take a rest step instead. The command-line runner has no "allow all" switch.
7. SIGINT arms the kill switch. The current decision finishes checking the switch, and the loop stops before the next environment step. The switch does not send input to a game.
8. The logger appends JSON objects, schema `sietch.session.v1`, and refuses fields such as email, phone, or API keys.

## Layout

| Path | Role |
| --- | --- |
| `sietch/guard.py` | Refuses a real-game connection |
| `sietch/env/interface.py` | Abstract environment API |
| `sietch/env/mock_world.py` | Deterministic mock survival world |
| `sietch/policies.py` | Scripted policies, plus an optional injected language-model plug |
| `sietch/supervisor.py` | Presence check, approval gate, kill switch |
| `sietch/orchestrator.py` | Two-agent loop, handoff, logging |
| `sietch/logging_jsonl.py` | JSONL writer and the event vocabulary |
| `sietch/evaluate.py` | Registered scenario v1 |
| `sietch/session.py` | Command-line entry |
| `configs/sandbox.yaml` | Replan condition |
| `configs/sandbox-retry.yaml` | Retry condition |
| `configs/agents.yaml` | Role card. The runner does not load it |
| `tests/` | Pytest suite |

## Language-model plug

`LLMPolicy` accepts an in-process client with a `complete(messages)` method. The command-line runner rejects `policy: llm` so a config edit cannot open a network call. Tests use a stub client. Do not commit API keys. `.env` files are gitignored.

## Tests

The suite covers the guard, world transitions, complete and incomplete handoffs, the approval gate, the kill switch, JSONL shape, personal-data rejection, deterministic traces, and the scenario v1 fingerprint. See [../methodology/evaluation.md](../methodology/evaluation.md) for what those counts mean and what they do not mean.

## License

Public domain under the Unlicense. See [../LICENSE](../LICENSE).

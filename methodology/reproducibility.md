# Reproducibility

How to regenerate the sandbox checks this plan relies on. The NeurIPS checklist answers, including the ones that are n/a, are in [../docs/reproducibility-checklist.md](../docs/reproducibility-checklist.md). The practical bar is the one described by Pineau et al. (2021): a reader should be able to rerun the code and see the same result. Citation: [../docs/references.md](../docs/references.md).

## Environment

- Python 3.11 or newer. The run that locked the fingerprint used Python 3.12.
- PyYAML 6 or newer, for the config files.
- pytest 8 or newer, for the tests.
- CPU only. No GPU, no network, no API key.
- The tests finish in seconds.

Install from `scripts/`:

```bash
python -m pip install -e ".[dev]"
```

`scripts/requirements.txt` lists the same two dependencies for a plain `pip install -r requirements.txt`.

## Commands

From `scripts/`:

```bash
python -m pytest
python -m sietch.session --config configs/sandbox.yaml --operator-present
python -m sietch.session --config configs/sandbox-retry.yaml --operator-present
```

From the repository root, `python -m pytest` uses `pytest.ini` so the package on `scripts/` is importable.

The session command prints one summary line. The fingerprint in [evaluation.md](evaluation.md) is asserted by the test, not by comparing log files by hand. Log lines include timestamps. The library path used by the test injects a fixed clock (`2026-09-24T00:00:00+00:00`) so two traces match. The command-line clock is the real time, so two CLI logs are not byte-identical, and the action trace still is, for a fixed seed.

## What is fixed

| Item | Where |
| --- | --- |
| Scenario parameters | `REGISTERED_SCENARIO_V1` in `scripts/sietch/evaluate.py` |
| Replan and retry configs | `scripts/configs/sandbox.yaml` and `sandbox-retry.yaml` |
| Metric implementation | `scripts/sietch/orchestrator.py` |
| Expected fingerprint | `scripts/tests/test_session.py` |
| Event vocabulary | `LOG_EVENTS` in `scripts/sietch/logging_jsonl.py` |

Change the scenario, the metric, and the test in the same commit. Note the change in [deviations.md](deviations.md) when it changes a hypothesis or a reported fingerprint.

## What is intentionally not fixed

- Calendar time of a run
- The random UUID in a command-line `session_id` when the config leaves `session_id` null
- Absolute log paths

## Secrets and local files

Do not commit `sessions/`, `*.jsonl`, `.env`, keys, or game files. Those paths are in `.gitignore`. The tests write logs under pytest's temporary directory.

## Game study

There is no reproducibility path for play in Dune: Awakening, because that play is not allowed yet and no connector exists. A procedure for a permitted session would be written after a written answer, and would include any conditions Funcom sets. **Proposed, pending Funcom review:** that later procedure would name the build of this repository, the protocol version, the operator attestation, and the log schema, and would still refuse memory editing, packet interception, and unauthorized clients.

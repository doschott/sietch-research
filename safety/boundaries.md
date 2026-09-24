# Safety boundaries

## The line the code keeps

`scripts/sietch/guard.py` is the boundary in software.

- `REAL_GAME_CONNECTION_ENABLED` is false.
- `assert_sandbox_only` allows the mode string `sandbox` only.
- If that flag is set true, the same function still raises `RealGameConnectionDisabled`. There is no connector waiting behind the flag.
- `connect_real_game()` always raises.
- `open_environment` returns `MockSurvivalWorld` only after the guard passes.
- Config YAML with `real_game_connection: true`, or with any other mode, is rejected before a session starts.
- The command-line runner rejects `policy: llm`, so a config edit cannot call a model provider.
- The log writer rejects secret and personal-data field names.

The tests in `scripts/tests/test_guard.py`, `test_session.py`, and `test_source_boundaries.py` check those refusals and scan the package for client-hook markers such as memory-reading APIs, input automation libraries, and packet libraries.

## What this repository does not contain

- game assets, client binaries, or server binaries
- screenshots or extracted game text
- a launcher, an injector, a packet parser, or an input automation path
- credentials, server passwords, or API keys

Contributors are asked not to add them. See [../CONTRIBUTING.md](../CONTRIBUTING.md).

## What "disabled until written permission" means

A written answer from Funcom is required before any agent acts in Dune: Awakening. A written answer that says no ends that aim. A written answer that says yes with conditions is followed, including conditions that are stricter than this folder.

A later pull request could add a connector only after that answer, only by a method the answer allows, and only with the guard changed in a reviewed diff that still refuses memory editing, packet interception, unauthorized clients, and anti-cheat circumvention. Those four are ruled out by the request itself, not only by the current code. This file does not design the connector. The connection method is an open question.

## Language-model calls

The default policy is local and scripted. `LLMPolicy` runs only when some caller passes a client object. That caller is responsible for what leaves the machine. **Proposed, pending Funcom review:** a client used in a future study must not be sent game files, personal data, or unpublished protocol text Funcom has asked to hold. Scenario v1 does not face that choice because no client is attached.

## Trademarks and files

Dune: Awakening is named so a reader can see where the requested research would take place. The name is not permission to ship the game's files. The Unlicense covers this repository's own text and code. It does not cover Funcom's or Dune's trademarks, assets, or game code.

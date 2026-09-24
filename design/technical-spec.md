# Technical specification

Reference for the sandbox in `scripts/sietch/`, version 0.1.0. If this text and the code disagree, the code and the tests are the source of truth, and this file should be corrected in the same change.

Real-game connection is disabled. See [../safety/boundaries.md](../safety/boundaries.md).

## Packages

| Module | Responsibility |
| --- | --- |
| `guard.py` | `assert_sandbox_only`, `connect_real_game` |
| `env/interface.py` | `Environment` abstract class: `reset`, `observe`, `step`, `available_actions` |
| `env/mock_world.py` | `WorldConfig`, `MockSurvivalWorld`, `open_environment` |
| `models.py` | Observations, handoff records, assignments, session reports |
| `policies.py` | `ScriptedPolicy`, `LLMPolicy` |
| `supervisor.py` | Presence, approval, kill switch |
| `logging_jsonl.py` | JSONL schema and `LOG_EVENTS` |
| `orchestrator.py` | `run_session` |
| `config.py` | YAML loader |
| `session.py` | Command-line `main` |
| `evaluate.py` | `REGISTERED_SCENARIO_V1` |

Python 3.11 or newer. Third-party runtime dependency: PyYAML. Tests need pytest.

## Environment API

`Environment.step` takes one action name and returns an `Observation`. `open_environment(mode, config)` calls the guard and, for `sandbox`, returns a `MockSurvivalWorld`. Any other mode raises `RealGameConnectionDisabled`.

### WorldConfig

| Field | Scenario v1 |
| --- | --- |
| `seed` | 7 |
| `water` | 4 |
| `base_integrity` | 3 |
| `storm_period` | 6 |
| `storm_length` | 2 |
| `max_water` | 8 |
| `max_base` | 10 |

`storm_period` must be at least 2. `storm_length` must be at least 1 and shorter than the period. A tick is in a storm when `tick % storm_period >= storm_period - storm_length`.

### Actions

| Action | Effect when it succeeds | Failure |
| --- | --- | --- |
| `gather_water` | Water increases by 2, then metabolism | `exposure` if unsheltered in a storm |
| `enter_shelter` | `sheltered` becomes true | `shelter_unavailable` if the shelter is still locked after this step's lock countdown |
| `leave_shelter` | `sheltered` becomes false | `exposure` if a storm is up |
| `repair_base` | Spend 1 water, base integrity increases by 2 | `exposure`, or `insufficient_water` |
| `scout` | Forecast is stored for one storm period | `exposure` |
| `rest` | No extra effect | `exposure` |
| `abandon_shelter` | Shelter locks for 5 ticks | `shelter_abandoned` (high-impact) |
| `discard_water` | Water becomes 0, metabolism skipped | `water_discarded` (high-impact) |

At the start of a step, a shelter lock above zero counts down by one and clears `sheltered`. Metabolism then subtracts 1 water, floored at 0, after every action except `discard_water`. If water is 0 afterward and the action failure is not `water_discarded`, `dehydration` is added. The observation's primary `failure` is the first name in that list.

An unknown action name is recorded as `unknown_action` after metabolism. It does not raise, so a bad policy cannot crash the loop. `LLMPolicy` refuses unknown names before they are sent.

`abandon_shelter` and `discard_water` are high-impact. The orchestrator will not send them unless the approver returns true.

### Observation

`tick`, `water`, `sheltered`, `storm`, `storm_in` (null until a scout is still in date), `base_integrity`, `shelter_locked`, `failure`, `failures`.

`snapshot()` returns those fields as a dictionary. Handoff records store that dictionary.

## Handoff record

Required before acceptance:

| Field | Rule |
| --- | --- |
| `from_agent` | Non-empty, distinct from the receiver |
| `to_agent` | Non-empty |
| `goal` | Non-empty |
| `reason` | Non-empty |
| `world_snapshot` | Dict containing `tick`, `water`, `sheltered`, `storm`, `base_integrity`, `failure` |
| `open_commitments` | List, may be empty |
| `failure_history` | List, may be empty |

`missing_fields()` returns the names that failed. The orchestrator rejects the record, writes `handoff_rejected`, and takes a rest step. A second handoff attempt on the same observation is rejected with missing reason `churn`.

Accepted handoffs update `Assignment` (owner, goal, commitments, history) and do not call `step`.

## Policies

`ScriptedPolicy(style="replan"|"retry", handoff_style="complete"|"minimal", max_repeats=4, force_action=None)`.

- Eve and Edos each get their own instance, so retry memory is not shared.
- `minimal` builds a record with an empty reason, a null snapshot, and null lists, which the orchestrator rejects. It exists for the mechanism test.
- `force_action` returns that action once. Tests use it to hit the approval gate.
- `LLMPolicy(client)` calls `client.complete(messages)` and parses `{"action": "<name>"}`. With `client=None` it raises `LLMClientNotConfigured`. The CLI never constructs it.

The scripted rules are documented in [../methodology/research-plan.md](../methodology/research-plan.md).

## Supervisor

`Supervisor(human_present=True, approver=None, approval_required=None, before_decision=None)`.

- `human_present=False` raises `OperatorAbsentError` inside the constructor.
- `run_session` also requires `operator_present=True` and `human_present=True` before it builds the supervisor.
- `approver` defaults to a function that returns false.
- `kill()` sets the flag. `poll()` increments `decisions_seen`, runs `before_decision`, and returns the flag.
- `review` logs `approval_requested` and then `approval_granted` or `approval_denied`.

## Session loop

`run_session` order:

1. Guard and operator checks.
2. `open_environment("sandbox")`, `reset`, open the log, write `session_start`.
3. Owner starts as Eve, goal `maintain`.
4. Until `max_steps` environment steps, or the kill switch: poll, ask the owner for a decision, accept or reject a handoff, or gate and apply an action.
5. Track failure episodes as defined in [../methodology/evaluation.md](../methodology/evaluation.md).
6. Write `session_end` with the report fields.

Return value: `SessionReport`.

## Log schema `sietch.session.v1`

Each line is one JSON object with `schema`, `ts`, `session_id`, and `event`. Events:

| Event | When |
| --- | --- |
| `session_start` | After the guard and the operator check |
| `decision` | Every policy output |
| `handoff_accepted` | Record applied |
| `handoff_rejected` | Missing fields or churn |
| `approval_requested` | High-impact action reaches the gate |
| `approval_granted` | Approver returned true |
| `approval_denied` | Approver returned false |
| `substituted_rest` | A denied action was replaced |
| `action_result` | After `step` |
| `kill_switch` | Loop stopped by the operator |
| `session_end` | Always, including after a kill |

`JsonlLogger.write` rejects forbidden field names before it appends. Unknown event names raise `ValueError` after that check, so a new event has to be added to `LOG_EVENTS` and to this table together.

## Config

`load_config` uses `yaml.safe_load`. Required shape is the templates in `scripts/configs/`.

| Key | Constraint |
| --- | --- |
| `mode` | `sandbox` |
| `real_game_connection` | false |
| `policy` | `scripted` for the CLI. `llm` loads but `run_from_config` raises |
| `policy_style` | `replan` or `retry` |
| `seed`, `max_steps` | Integers |
| `world.*` | Passed to `WorldConfig` |
| `supervisor.human_present` | Must be true or the session raises |
| `supervisor.approval_required` | List of action names |
| `logging.path` | Default `sessions/sandbox.jsonl` |
| `session_id` | Null in the templates. The CLI then generates `sandbox-` plus eight hex characters |

`configs/agents.yaml` is a role card for readers. `load_config` is not pointed at it by the runner.

## Command line

```bash
python -m sietch.session --config configs/sandbox.yaml --operator-present
```

| Exit | Meaning |
| --- | --- |
| 0 | Report printed |
| 2 | Operator absent |
| 3 | Guard failure, bad config, or LLM policy requested from the CLI |

`--steps`, `--log`, and `--seed` override the template for that process. SIGINT arms the kill switch.

## Out of specification

The following are not specified because the permission request leaves them open, and this code does not implement them:

- a game client protocol
- network ports, account login, or input devices
- persistence of agent memory across operating-system reboots, beyond the JSONL file the operator chooses to keep
- a high-impact list for the game

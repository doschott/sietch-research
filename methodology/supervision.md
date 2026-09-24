# Supervised-agent framework

The September 2026 request requires a human operator whenever an agent is in session. This file says how the sandbox enforces a version of that rule, and which parts would still have to be reviewed before any game session.

> Using the approval gate, the high-impact list, and the kill switch on a battlegroup is **proposed, pending Funcom review**. The sandbox behavior below is implemented now and does not connect to the game.

## Presence

A session starts only when both of these are true:

- `supervisor.human_present: true` in the YAML config
- the caller passes `--operator-present` (or the library call sets `operator_present=True`)

If either one is false, `run_session` raises `OperatorAbsentError`, the process exits with status 2, and no log file is created. The operator is not asked for a name. The log records the role `human_operator` and nothing more personal.

The flag is an attestation by the person who starts the process. The software cannot see the room. **Proposed, pending Funcom review:** on any future permitted session, the same attestation is required, and a session with no operator in the room is a stop, not a degraded mode.

## Approval gate

Before an environment action is applied, the supervisor checks it against `approval_required`. The sandbox templates list:

- `abandon_shelter`
- `discard_water`

Those two actions exist so the gate can be tested. The ordinary scripted policy never selects them. A test policy can force `discard_water`.

If the action is on the list, the logger writes `approval_requested` and calls the approver.

- The default approver returns false.
- A denial writes `approval_denied`, increments `approval_blocks`, and replaces the action with `rest`. The denied action is not applied.
- An approval writes `approval_granted` and the action is applied.
- Actions off the list are not sent to the approver.

The command-line runner does not offer an allow-all switch. Tests that need an approval inject a callback. An interactive prompt is not implemented. **Proposed, pending Funcom review:** if a game session ever needs a gate, the operator's decision is an explicit yes or no on that action, the default is no, and the list of gated actions is agreed in the protocol before the session. This repository does not guess that list for the game.

## Kill switch

`Supervisor.kill()` sets a flag. The orchestrator checks the flag at the start of each decision and again after an approval review. When the flag is set, the logger writes `kill_switch` with reason `operator` and the loop stops. `session_end` is still written so the file has a closing record. No further `action_result` lines are written.

From the command line, SIGINT calls `kill()` on the live supervisor. If the signal arrives before the supervisor exists, the process is interrupted. A sandbox step is a local function call, so "stop before the next step" is the guarantee this code can keep. Stopping halfway through a game animation is an open question, and this code does not try.

The kill switch does not send a keystroke, a packet, or a memory write. It only stops this process's loop.

**Proposed, pending Funcom review:** on a permitted session, the operator can end the session immediately, the log records that the stop was the operator's, and play does not resume in that session.

## What the operator is for

The operator is the person who can refuse an action and end the run. The operator is not a source of training labels in scenario v1, and the log does not store a transcript of the operator's speech. If a later study wanted to record operator comments, that would be personal data and would need the proposal in [data-handling.md](data-handling.md) to be accepted first. It is not part of scenario v1.

## Unattended runs

An unattended game session is outside the request. The sandbox can be started by a test suite because the tests pass `operator_present=True` as the stand-in for the harness, and the tests do not connect to a game. A scheduled job that launched agents into Dune: Awakening would violate the request. No such job is provided.

# Stop procedures

When a run ends. The sandbox controls are implemented. Everything about a game session is **proposed, pending Funcom review**, except the points the September 2026 request already states: a human is present, Funcom may pause or end the exception, and no play happens before a written answer.

## Sandbox, in force now

Stop the session, and do not take another environment step, when any of these is true:

- the operator arms the kill switch (`Supervisor.kill()` or SIGINT in the command-line runner)
- the operator is not attested, in which case the session does not start
- the config asks for a real-game connection or a non-sandbox mode, in which case the session does not start
- the process is about to log a forbidden personal-data field, in which case that record is refused

The loop writes `kill_switch` and then `session_end`. The log is kept as-is. Research failures such as `exposure` do not stop scenario v1. They are the thing the metric counts. An operator who wants those to stop the run can arm the kill switch. There is no hidden threshold that stops the mock world on its own.

The step cap (`max_steps`, 16 in scenario v1) ends a run in the ordinary way. That cap is an instrument setting. It is not a proposed length for a game session. Session length in the game is an open question.

## Game session, proposed

If a written answer allows agent sessions, stop and stay stopped for that session when:

- the operator is not present
- the operator uses the stop control
- Funcom refuses, pauses, or ends the exception
- the operator cannot confirm the server is still the single closed battlegroup described in the protocol
- the operator is unsure an action stays inside the request and any conditions Funcom attached
- a participant withdraws
- an incident in [../ethics/incidents.md](../ethics/incidents.md) has been declared

**Proposed:** there is no automatic resume. A new session needs a fresh operator attestation and a protocol that still matches Funcom's answer.

## Criteria the request left open

The request does not list numerical safety limits (time of day, duration, number of actions). This file does not invent them. If Funcom supplies limits, they are copied into the protocol before any session and they override this proposal.

## After the stop

Follow [../ethics/incidents.md](../ethics/incidents.md) when the stop was not a normal end of scenario v1. A normal end is the step cap on a sandbox run that stayed inside the mock world.

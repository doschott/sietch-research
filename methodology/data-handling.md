# Data handling

The September 2026 request offers Funcom session logs on request, and it does not say what a log contains, how long it is kept, where it lives, or how personal data is handled. Those four points are open questions. This file separates what the sandbox does today from proposals for a game session that does not yet exist.

Items in the proposal sections are **proposed, pending Funcom review**. They are not extra commitments. Funcom's written answer, if it sets different rules, wins.

## What the sandbox logs today

The runner appends JSONL, one object per line, schema `sietch.session.v1`. The event names are fixed in `LOG_EVENTS`:

`session_start`, `decision`, `handoff_accepted`, `handoff_rejected`, `approval_requested`, `approval_granted`, `approval_denied`, `substituted_rest`, `action_result`, `kill_switch`, `session_end`.

A typical line has `schema`, `ts` (UTC, ISO 8601), `session_id`, and `event`, plus event-specific fields such as the agent id (`eve` or `edos`), the action name, the mock world's water, shelter, storm, base integrity, and failure name, and the handoff's goal, reason, commitments, and failure history.

The sandbox log does not contain:

- a person's name, email, phone number, account id, or IP address
- a server password or an API key
- game memory, screenshots, or files from a game install
- free-text notes from the operator

The writer raises `PersonalDataRejected` if a field name is one of: `email`, `phone`, `phone_number`, `ip`, `ip_address`, `player_name`, `real_name`, `address`, `password`, `passwd`, `token`, `api_key`, `secret`, `credential`. The check walks nested objects. A rejected record is not written.

Default path: `sessions/*.jsonl`, gitignored, on the machine that ran the session. The tests use a temporary directory. There is no upload step.

`session_id` in the templates is null, and the command line then uses a random id of the form `sandbox-` plus eight hex characters. That id is a file label, not a personal identifier.

## Retention of sandbox logs

**Proposed, pending Funcom review**, and also a local default a contributor can follow today: delete sandbox logs when they are no longer needed to debug a run. Do not commit them. The repository does not run a deletion job. Keeping or deleting a local debug log is the operator's choice, because the request does not set a retention period.

## Proposals for a future game session

These apply only if Funcom gives written permission and a protocol for that session exists. Until then they are inactive.

**Log contents, proposed.** The same schema, plus a small header: protocol version, repository revision, battlegroup label chosen by the operator (not a public server address), and the attestation that the operator was present. Still no passwords. Still no memory dumps, packet captures, or screenshots of the game. If Funcom wants a different schema, that schema replaces this one.

**Retention, proposed.** Keep game-session logs until Funcom has had a chance to request them, and for no longer than the period Funcom states. If Funcom states no period, the open question remains open and the logs are not given a default sunset by this draft. Deletion, if it happens, is recorded in the research notes (date and session id only).

**Storage, proposed.** On storage the operator controls, separate from the git repository, with access limited to the research operator and to Funcom if Funcom asks. This draft does not name a vendor. Naming a vendor would pretend the request chose one.

**Providing logs to Funcom, proposed.** On request, using a channel Funcom specifies. The request already includes the offer. This draft does not invent a portal or a deadline.

**Personal data, proposed.**

- Do not log player names if a role label will do.
- If a human participant's name or account identifier is necessary to honor a consent record, store that record apart from the agent JSONL, with access limited to the operator.
- The consent record's contents are themselves an open question. A draft structure is in [../ethics/consent.md](../ethics/consent.md).
- Do not place personal data in this public repository, in an issue, or in a pull request.
- A participant can ask for their personal data to be removed from the operator's notes. Agent decisions already logged without personal identifiers would stay, because they do not identify the person. Whether game logs that incidentally contain a name can be redacted is part of the open question, and would follow Funcom's conditions if any are set.

**Training, out of scope.** The request rules out training a public model on Funcom assets. Sandbox logs are not Funcom assets. They are also not a training set in this plan. Scenario v1 does not train anything.

## Funcom's own data

This repository does not hold Funcom customer data, telemetry, or source code, and the proposals above are not a request for any of it.

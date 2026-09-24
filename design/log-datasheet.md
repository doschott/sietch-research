# Datasheet for sandbox session logs

Datasheets for datasets (Gebru et al. 2021) ask the creator to record why a dataset exists, what it contains, how it was collected, and how it should be used. This datasheet covers the JSONL files the sandbox can write. It does not cover a dataset of game sessions, because that dataset does not exist. Citation: [../docs/references.md](../docs/references.md).

Where the September 2026 request is silent, the answer is marked **proposed, pending Funcom review** or left as an open question.

## Motivation

The logs exist so a sandbox run can be checked: which agent acted, whether a handoff was accepted, whether a failure cleared, and whether the operator stopped the run. The permission request offers Funcom session logs on request if agent sessions are ever allowed. The sandbox schema is a concrete proposal for the shape of a log, not the agreed format.

## Composition

- **Instance type:** one JSON object per line, schema `sietch.session.v1`.
- **A session file:** the lines from `session_start` through `session_end` for one `session_id`.
- **Fields:** event name, timestamp, session id, agent id (`eve` or `edos`), action name, mock-world numbers (water, shelter, storm, base integrity, failure), and handoff text (goal, reason, commitments, failure history). The full event list is in [technical-spec.md](technical-spec.md).
- **People:** no names, emails, phone numbers, account ids, or IP addresses. The operator appears only as the role string `human_operator` on `session_start`.
- **Sensitive data:** the writer rejects a fixed set of field names covering contact details and secrets. See [../methodology/data-handling.md](../methodology/data-handling.md).
- **Subpopulations:** none. There are two agent roles and one operator role.
- **Size:** a 16-step scenario is a few dozen lines. The repository does not ship a sample log. The test regenerates the events.
- **External data:** none. The world is computed from the config.

Recommended split: there is no train or test split. The fingerprint test is a regression check, not a held-out sample of people.

## Collection process

- **How:** `JsonlLogger.write` during `run_session`.
- **Who:** the person who runs the command, attested with `--operator-present`.
- **When:** any time the tests or the CLI run. No schedule is claimed.
- **Ethical review:** not applicable to the sandbox. No human subjects are collected. See [../ethics/consent.md](../ethics/consent.md) for the open question about later participants.
- **Notice and consent:** the operator is the person who starts the process. No other person is recorded.
- **Time period of a future game dataset:** an open question. Not started.

## Preprocessing

None. Lines are appended and are not cleaned, clustered, or labeled by a second model. A hand check of recovery latency is described in [../methodology/threats-to-validity.md](../methodology/threats-to-validity.md).

## Uses

- **Intended:** debugging the sandbox, reviewing a run, locking scenario v1 in tests.
- **Not intended:** training a model, publishing player behavior, ranking people, or standing in for evidence about Dune: Awakening.
- **Repository policy:** do not commit the files. `sessions/` and `*.jsonl` are gitignored.

**Proposed, pending Funcom review:** if game-session logs are ever created, their use is limited to the research questions (planning, handoff, recovery), to the operator's own analysis, and to a copy for Funcom on request. They are not a public training set. The request already rules out training a public model on Funcom assets.

## Distribution

Sandbox logs are local. There is no download link. A future distribution to Funcom would follow the channel Funcom specifies. That channel is an open question. Public release of raw logs is not part of this draft. A public writeup, if one is published, would use aggregate or redacted descriptions, and Funcom would get a first look when the writeup discusses the game study. That first look is an offer in the request.

## Maintenance

- **Owner:** Daniel Schott, doschott@gmail.com.
- **Schema changes:** bump the `schema` string, update `LOG_EVENTS`, update [technical-spec.md](technical-spec.md), and add a row to [../methodology/deviations.md](../methodology/deviations.md) if a metric changes.
- **Retention:** sandbox debug logs can be deleted by the operator when the run is no longer needed. A retention period for game logs is an open question. A proposal is in the data-handling note.
- **Older versions:** none have been published.

## Legal and ethical notes

The logs are original output of this repository's code. They are not Funcom content. The Unlicense applies to the logger code. It is not a license to collect data from the game. No game data is collected. Personal data of participants is not part of scenario v1. If that changes, the consent proposal has to be accepted and the datasheet has to be rewritten first.

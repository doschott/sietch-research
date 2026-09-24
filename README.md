# Sietch Research

Supervised AI-agent research on a closed, self-hosted Dune: Awakening battlegroup.

> **Status.** Written permission from Funcom has been requested and is pending. A follow-up was sent on 24 September 2026 (support ticket #308630). No agent play will take place in Dune: Awakening until a written answer is received. If the answer is no, the agents stay out of the game. If the answer is yes with conditions, those conditions will be followed.
>
> This is an independent project. It is not affiliated with, sponsored by, or endorsed by Funcom.

## What this project is

Sietch Research studies how two persistent agents, Eve and Edos, plan, hand off work, and recover from failure. The permission request names a living survival world as the place for that question. Until Funcom answers in writing, the only world in this repository is an offline mock: water, shelter, storms, and base integrity. It is a research instrument. It is not a game client, and it does not load game files.

The goal is research, not farming or leaderboard play. All proposed play stays on a single invite-only, passworded, self-hosted battlegroup operated by the project, away from official servers and away from public players. See [docs/definitions.md](docs/definitions.md).

## Collaboration model

- **Two agents.** Eve plans. Edos takes repair and recovery handoffs. A handoff counts only when the record carries the goal, the reason, a world snapshot, the open commitments, and the failure history.
- **Human supervision at all times.** A human operator is present whenever an agent is in session. The sandbox will not start without that attestation. High-impact actions stop at an approval gate. The default decision is to deny them. A kill switch ends the loop before the next step.
- **Transparency with the rights holder.** A written protocol is shared with Funcom before any agent session, session logs are available to Funcom on request, and Funcom gets a first look at any public writeup.
- **Funcom stays in control.** Funcom may say no, pause, or end the exception at any time.

The files under [methodology/](methodology/README.md) are the public draft of that protocol. They are not a claim that Funcom has accepted them.

## An open invitation to Funcom

We would genuinely welcome Funcom's involvement, at whatever level is comfortable. That could mean reviewing the protocol, suggesting conditions, opening issues, commenting on pull requests, or simply telling us what you would rather we not do. Feedback from the people who built Arrakis will make this research safer and better. See [CONTRIBUTING.md](CONTRIBUTING.md), or write to doschott@gmail.com.

## Repository map

| Path | Purpose |
| --- | --- |
| [docs/definitions.md](docs/definitions.md) | Terms, scope, open questions, and proposals |
| [docs/references.md](docs/references.md) | Sources the documentation was shaped by |
| [docs/reproducibility-checklist.md](docs/reproducibility-checklist.md) | NeurIPS checklist questions, answered for the current sandbox |
| [methodology/](methodology/README.md) | Draft research plan, metrics, data handling, threats |
| [ethics/](ethics/README.md) | Oversight, consent proposal, incidents |
| [safety/](safety/README.md) | Permission status, closed-server boundary, stops |
| [design/architecture.md](design/architecture.md) | Diagrams of agents, logs, and the safety boundary |
| [design/technical-spec.md](design/technical-spec.md) | Sandbox specification |
| [design/system-card.md](design/system-card.md) | System card for the scripted agents |
| [design/log-datasheet.md](design/log-datasheet.md) | Datasheet for sandbox logs |
| [scripts/](scripts/README.md) | Offline runner, mock world, and tests |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Issues, pull requests, and files that must not be added |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |
| [CITATION.cff](CITATION.cff) | Citation metadata |

## Roadmap

The phases wait on Funcom's written answer. The request does not set a calendar, and this roadmap does not add one. Session length, frequency, and timeline remain open questions.

**Phase 0, now.** Publish the draft protocol, the ethics and safety notes, and the offline sandbox. Run the tests. Do not connect to the game. Permission is pending.

**Phase 1, the answer.** Read the written answer before changing the aim.

- If the answer is no, the agents stay out. The sandbox can remain as a methods exercise. Record that outcome in [methodology/deviations.md](methodology/deviations.md).
- If the answer is yes with conditions, copy those conditions into the protocol before any other step. Proposals in this repository yield where they conflict with the conditions.

**Phase 2, only after that updated protocol.** One closed research battlegroup, a human operator present for every session, logs available to Funcom on request, and no contact with players outside the research group. How the agents connect to the game client is still an open question until the protocol names a method the answer allows. Unauthorized clients, packet interception, memory editing, and anti-cheat circumvention stay ruled out.

**Phase 3, reporting.** Analyze planning, handoff, and recovery. Offer Funcom a first look at any public writeup before publication. Make no endorsement claim unless Funcom chooses one.

## Quickstart

The runner is Python 3.11 or newer. It does not call a model provider. From a checkout:

```bash
cd scripts
python -m pip install -e ".[dev]"
python -m pytest
python -m sietch.session --config configs/sandbox.yaml --operator-present
```

`pytest` from the repository root works as well (`pytest.ini` adds `scripts/` to the path). The session command refuses to start unless you pass `--operator-present`, and the config must keep `real_game_connection: false`. Logs go to `sessions/`, which is gitignored. Details and the retry condition are in [scripts/README.md](scripts/README.md).

## Contributing

Issues and pull requests are welcome, including from Funcom. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before adding files. In particular, do not add a game connector, game assets, credentials, or personal data. Changes that affect scope or the offers to Funcom need the maintainer's approval.

## What this repository will never contain

No game assets, no client or server binaries, no screenshots of the game, and no proprietary Funcom material. No tools for unauthorized clients, packet interception, memory editing, or anti-cheat circumvention.

## Trademarks

Dune: Awakening and related names are trademarks of their respective owners. They are used here only to describe where the proposed research would take place.

## License

This project is released into the public domain under the Unlicense. See [LICENSE](LICENSE) and [https://unlicense.org](https://unlicense.org).

This dedication covers only this repository's own original content. It grants no rights over Funcom's or Dune trademarks, game assets, or any other third-party material.

## Credits

Research design by Daniel Schott ([@doschott](https://github.com/doschott)), Grand Forks, North Dakota, USA. Drafting help from AI assistants (Grok, xAI, and Cursor agents).

Contact: doschott@gmail.com

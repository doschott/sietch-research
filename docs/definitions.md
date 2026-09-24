# Definitions and scope

This document defines the terms and boundaries of Sietch Research. The scope is the written permission request Daniel Schott sent to Funcom Legal in September 2026, restated in the 24 September 2026 follow-up. Where that request settles a point, this document records it. Where the request is silent, the point is an open question or a proposal. A proposal is marked **proposed, pending Funcom review**. A proposal is a design choice in this repository. It is not an extra promise to Funcom.

> **Permission status.** Written permission from Funcom has been requested and is pending. A follow-up was sent on 24 September 2026 (support ticket #308630). No agent will play in Dune: Awakening until a written answer is received. If the answer is no, the agents stay out. If the answer is yes with conditions, those conditions are followed. This project is not affiliated with, sponsored by, or endorsed by Funcom.

## How to read a term

- **Request.** Language taken from the September 2026 permission request. These are the boundaries the project has asked Funcom to consider.
- **Sandbox.** Behavior implemented in `scripts/` against the mock world. It does not touch the game.
- **Proposed, pending Funcom review.** A design this repository recommends for later review. It can be dropped or rewritten. It is not in force for any game session, because no game session is allowed yet.
- **Open question.** The request does not settle it, and this repository does not pick an answer.

## Status

Written permission from Funcom has been requested and is pending. Nothing in this document claims that permission has been granted.

## Key terms

**The request.** A limited, revocable, noncommercial written exception from Funcom allowing the project's own research agents to run on a single self-hosted battlegroup operated by the project.

**Closed server (research battlegroup).** A single Dune: Awakening battlegroup that is:

- self-hosted by the project, using Funcom's official self-host tools
- invite-only and passworded
- not listed publicly
- not an official server
- not a public or rented private-server World shared with other communities

**Research group.** The invited participants on the closed server. The agents do not interact with anyone outside this group. The size of the group, and the invitation method, are open questions.

**Research agents.** Two AI agents operated by the project, named Eve and Edos. They are persistent across sessions and are studied as they plan, coordinate, hand off work, and recover from failure.

**Eve.** The planner agent in the current sandbox design. Eve holds the default goal `maintain` and hands repair or recovery work to Edos.

**Edos.** The recovery agent in the current sandbox design. Edos takes repair and recovery handoffs and hands the task back when the handoff goal is met.

**Persistent.** The agent keeps a task assignment, open commitments, and a failure history across steps and, in the study design, across sessions. Persistence in the sandbox is the in-memory assignment plus the JSONL log. How persistence would work across game sessions is an open question.

**Handoff.** The moment one agent transfers an unfinished task to the other. In the sandbox, a handoff does not advance the world clock. At most one handoff is accepted on a given observation. Whether communication would consume time in the game is an open question.

**Handoff record.** The structured note that must accompany a handoff before the orchestrator accepts it: sender, receiver, goal, reason, world snapshot, open commitments, and failure history. Empty lists are allowed. Missing fields are not. This required set is part of the sandbox specification. Using the same set in a game session is **proposed, pending Funcom review**.

**Failure.** An environment step whose observation carries a failure name. In the mock world the names include `exposure`, `dehydration`, `insufficient_water`, `shelter_unavailable`, `shelter_abandoned`, `water_discarded`, and `unknown_action`. These names belong to the mock world. They are not a taxonomy of Dune: Awakening.

**Failure episode.** A run of steps that starts when a failure appears and ends at the next step with no failure, or at the end of the session if the failure is still open. The sandbox tracker holds one open episode at a time. A new failure while an episode is open extends that episode.

**Recovery.** The close of a failure episode. **Recovery latency** is the number of environment steps from the step that opened the episode to the step that closed it. The definition is operational and is implemented in `scripts/sietch/orchestrator.py`. It is a sandbox metric. Applying it to game logs is **proposed, pending Funcom review**.

**Supervised.** A human operator is present whenever an agent is in session. Agents do not run unattended in the game. This is part of the request.

**Human operator.** The person accountable for the session. In the sandbox the operator's presence is a pair of flags (config and command line), the operator can deny high-impact actions, and the operator can arm the kill switch. The operator is not an agent and is not logged by name.

**Supervised-agent framework.** The sandbox controls around the two agents: a human present for the whole session, an approval gate, and a kill switch. The request requires the human. The gate and the kill switch are how this repository proposes to make that presence concrete. Their use on a battlegroup is **proposed, pending Funcom review**.

**Approval gate.** A check that stops actions listed as high-impact until the operator approves them. The sandbox default is to deny. The sandbox high-impact names are `abandon_shelter` and `discard_water`. A list for the game is an open question.

**High-impact action.** An action the operator must approve before it is applied. The label is a research control. It is not a claim about game rules or sanctions.

**Kill switch.** A control that stops the sandbox loop before the next environment step. SIGINT arms it from the command line. It does not send input to a game. A kill switch on a future permitted session is **proposed, pending Funcom review**.

**Agent session.** Any period during which an agent is connected to or acting in the game. A written protocol is shared with Funcom before any agent session takes place. A sandbox run is not an agent session in this sense. It never connects to the game.

**Sandbox (mock survival world).** The in-process world in `scripts/sietch/env/mock_world.py`. It tracks water, shelter, storms, and base integrity so the agents can be studied before any permission decision. It does not load game files and it is not a simulation of Dune: Awakening.

**Real-game connection.** Any path that would read game memory, intercept packets, automate input into the game, or touch Dune: Awakening files. That path is disabled. `scripts/sietch/guard.py` raises if code asks for it. How a permitted agent would connect, using only methods Funcom allows, is an open question. No connector will be added unless a written answer allows it and the method is reviewed in this repository.

**Scripted policy.** The default decision rule in `scripts/sietch/policies.py`. It is deterministic and offline. `replan` hands a failure to the other agent. `retry` repeats the last environment action. The gather rule is brittle on purpose: it gathers at low water even during a storm, so the scenario contains a failure to recover from.

**Language-model policy.** An optional plug, `LLMPolicy`, that calls a client supplied by the caller. The command-line runner refuses it. The repository does not ship a key, a provider SDK, or a trained model.

**Session log.** A JSONL file, schema `sietch.session.v1`, written by the sandbox runner. Logs are gitignored. The request offers Funcom session logs on request for agent sessions. What those game logs would contain, how long they would be kept, and where they would be stored are open questions. Proposals are in [methodology/data-handling.md](../methodology/data-handling.md).

**Written protocol.** The document offered to Funcom before any agent session. The files under `methodology/` are the public draft of the research plan. They are not a claim that Funcom has accepted them. A game-session protocol would be completed only after a written answer, and would include any conditions in that answer.

**Exception.** The permission being requested. It is limited, revocable, and noncommercial, and Funcom may say no, pause it, or end it at any time.

**First look.** The offer, in the request, to show Funcom any public writeup before it is published.

**Endorsement.** A claim that Funcom sponsors or approves the agents or the research. The project will not make that claim unless Funcom chooses it.

**Noncommercial.** The exception asked for in the request. The request rules out selling access, boosting, and real-money trading. The sandbox code is public domain under the Unlicense, which the request does not limit; the noncommercial limit applies to the exception to run agents in the game, not to the license of this repository's own text and code.

**Official server.** A server Funcom operates for the public game. Out of scope.

**Private-server World.** In the request, a public or rented private-server World shared with other communities. Out of scope. The closed research battlegroup is the only server the request asks to use.

**Deep Desert and social hubs.** Places named in the request as locations where the agents must not contact players outside the research group.

**Dune: Awakening.** The game in which the requested research would take place. The name is used only to say where that research would happen. It is a trademark of its owner. This repository does not ship game assets, client files, or server files.

## Research focus

How two persistent AI agents plan, hand off work, and recover from failure in a living survival world where the environment can break the plan. The request names water, storms, bases, vehicles, and markets as examples of that pressure. The sandbox studies a smaller set: water, storms, shelter, and base integrity. Vehicles and markets are not in the mock world.

The research is not farming and not leaderboard play.

## In scope

- Agent play on the single closed research battlegroup described above, after written permission is received
- Interaction only with members of the research group
- Studying planning, coordination, task handoff, and failure recovery
- Session logging, with logs available to Funcom on request
- Public writeups, with Funcom given a first look before publication
- Until that written answer, documentation and the offline sandbox in this repository

## Out of scope

- Any agent play before a written answer from Funcom
- Official servers
- Public or rented private-server Worlds shared with other communities
- Deep Desert or social-hub contact with players outside the research group
- Unauthorized clients
- Packet interception
- Memory editing
- Anti-cheat circumvention
- Selling access, boosting, or real-money trading (RMT)
- Training a public model on Funcom assets
- Use of Dune trademarks beyond describing that the research happens inside the game
- Any claim that Funcom endorses the agents or the research, unless Funcom chooses that

## Commitments offered to Funcom

These are offers in the request, not a statement that Funcom has accepted them.

- A written protocol before any agent session
- Session logs on request
- The right to say no, pause, or end the exception at any time
- First look at any public writeup
- No claim of Funcom endorsement unless Funcom chooses that
- If the answer is no, the agents stay out of the game
- If the answer is yes with conditions, the conditions will be followed

## Open questions

The permission request does not define the following. They stay open until a written protocol, and where relevant a written answer, settles them.

- How agents connect to and act in the game client, within the limits above
- Size and composition of the research group, and how participants are invited
- Consent and briefing process for human participants in the research group
- What session logs contain, how long they are kept, and where they are stored
- Handling of any personal data from human participants
- Session length, frequency, and overall project timeline
- Criteria for pausing or stopping a session for safety reasons
- Conditions Funcom may attach to any permission, once received

## Proposals, pending Funcom review

The sandbox implements a concrete version of supervision so the research plan can be tested without the game. Using any of the following on a battlegroup is proposed, pending Funcom review:

- The approval gate and the idea of a high-impact action list
- The kill switch as the operator's stop control
- The handoff record's required fields
- The JSONL schema `sietch.session.v1` as a starting point for logs offered to Funcom
- The retention, consent, and incident steps in [methodology/data-handling.md](../methodology/data-handling.md), [ethics/consent.md](../ethics/consent.md), and [safety/stop-procedures.md](../safety/stop-procedures.md)

None of these proposals adds a game connector. The guard stays in place until a written answer exists and a reviewed change implements only what that answer allows.

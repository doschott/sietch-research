# Architecture

How the sandbox is put together, where logs go, and where a future game connection is refused. This describes the code in `scripts/`. It does not describe a live battlegroup. None is connected.

> **Permission status.** Written permission from Funcom has been requested and is pending. A follow-up was sent on 24 September 2026 (support ticket #308630). No agent will play in Dune: Awakening until a written answer is received. If the answer is no, the agents stay out. If the answer is yes with conditions, those conditions are followed. This project is not affiliated with, sponsored by, or endorsed by Funcom.

The module-level specification is [technical-spec.md](technical-spec.md). The agents are documented as a system card in [system-card.md](system-card.md). The logs are documented as a datasheet in [log-datasheet.md](log-datasheet.md).

## Collaboration

Eve and Edos never call the world directly. The orchestrator asks the agent who currently owns the task for a decision, asks the supervisor when a decision needs a person, and only then calls the mock world. A handoff changes the owner. It does not call the world.

```mermaid
flowchart TB
  operator[Human operator]
  supervisor[Supervisor]
  eve[Eve planner]
  edos[Edos recovery]
  orch[Orchestrator]
  world[Mock survival world]
  log[JSONL session log]

  operator -->|present, approve, or kill| supervisor
  supervisor --> orch
  eve -->|decision| orch
  edos -->|decision| orch
  orch -->|accepted handoff| eve
  orch -->|accepted handoff| edos
  orch -->|environment action| world
  world -->|observation| orch
  orch --> log
  supervisor --> log
```

Sequence for one handoff that then takes an action:

```mermaid
sequenceDiagram
  participant Operator
  participant Eve
  participant Orchestrator
  participant Edos
  participant World
  Eve->>Orchestrator: handoff record
  Orchestrator->>Orchestrator: require every field
  Orchestrator->>Edos: assignment
  Edos->>Orchestrator: environment action
  Orchestrator->>Operator: ask only if the action is high-impact
  Operator-->>Orchestrator: yes, or the default no
  Orchestrator->>World: allowed action, or rest if denied
  World-->>Orchestrator: observation
```

## Log flow

Sandbox logs stay on the machine that ran the session. They are not committed. The offer to give Funcom logs on request, and the offer of a first look at a public writeup, come from the permission request. They apply to the game study if it ever happens. They are not a claim that sandbox debug logs are shipped anywhere.

```mermaid
flowchart LR
  session[Sandbox session]
  jsonl[Local JSONL file]
  repo[Git repository]
  funcom[Funcom]
  writeup[Public writeup]

  session -->|schema sietch.session.v1| jsonl
  jsonl -.->|gitignored, not committed| repo
  jsonl -.->|on request, only for a future permitted agent session| funcom
  writeup -.->|first look offered before publication| funcom
```

Storage, retention, and personal data for those future logs are open questions. Proposals are in [../methodology/data-handling.md](../methodology/data-handling.md).

## Safety boundary

The guard sits in front of the only environment factory. The right-hand side is not implemented. The diagram is the refusal, not a roadmap of hooks to build.

```mermaid
flowchart LR
  subgraph currentBox [Running today]
    code[Research code]
    mock[Mock survival world]
    code --> mock
  end
  subgraph blockedBox [Refused until written permission]
    client[Game client]
    memory[Game memory]
    packets[Network packets]
    files[Game files]
  end
  code -->|guard raises| client
  code -->|guard raises| memory
  code -->|guard raises| packets
  code -->|guard raises| files
```

A written answer that allows a session would still have to name a method. That method is an open question. The request already rules out unauthorized clients, packet interception, memory editing, and anti-cheat circumvention. Those stay ruled out on both sides of the diagram.

## Process shape

```mermaid
flowchart TD
  startNode[Load YAML]
  guard{Mode is sandbox and real_game_connection is false}
  human{Operator attested}
  refuse[Raise and write no log]
  loop{Steps left and kill switch is clear}
  decide[Owner agent decides]
  hand{Handoff}
  complete{Record complete and not churn}
  gate{High-impact action}
  approved{Operator approves}
  stepNode[Mock world step]
  restNode[Rest step]
  stopNode[Write session_end]

  startNode --> guard
  guard -->|no| refuse
  guard -->|yes| human
  human -->|no| refuse
  human -->|yes| loop
  loop -->|no| stopNode
  loop -->|yes| decide
  decide --> hand
  hand -->|yes| complete
  complete -->|no| restNode
  complete -->|yes| loop
  hand -->|no| gate
  gate -->|yes| approved
  approved -->|no| restNode
  approved -->|yes| stepNode
  gate -->|no| stepNode
  stepNode --> loop
  restNode --> loop
```

The command-line process also installs a SIGINT handler that arms the kill switch between decisions.

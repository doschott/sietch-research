# Research plan

Draft for the sandbox study. Game-session items the September 2026 request does not settle stay open, or are marked **proposed, pending Funcom review**.

## Title

How two persistent agents plan, hand off work, and recover from failure under human supervision.

## Who is accountable

Research design: Daniel Schott. The sandbox and these documents are maintained in this public repository. Contact: doschott@gmail.com.

## Background

The request asks to study two persistent agents, Eve and Edos, on one closed, self-hosted Dune: Awakening battlegroup. The battlegroup would be invite-only, passworded, and unlisted. Official servers, and public or rented private-server Worlds shared with other communities, are out of the request. A human operator would be present whenever an agent is in session. The scientific target is planning, handoff, and failure recovery. Farming and leaderboard play are out of scope.

That game study cannot start. Permission is pending, and the request says no agent play happens until a written answer. If the answer is no, the agents stay out. If the answer is yes with conditions, those conditions are followed.

The study that can proceed is a sandbox study. Eve and Edos run against an in-process mock world with water, shelter, storms, and base integrity. The world is a research instrument. It is not a model of the game, and the runner cannot connect to a game client. See [../scripts/README.md](../scripts/README.md) and [../safety/boundaries.md](../safety/boundaries.md).

Voyager (Wang et al. 2023) is a useful neighboring example: one embodied agent in a survival game, studied without a human in the loop. The questions below add a second agent, a required handoff record, and a human operator. Voyager's Minecraft results are not used as targets. Citation: [../docs/references.md](../docs/references.md).

## Questions

**RQ1. Recovery.** After a plan fails, does handing the other agent a structured failure record reduce recovery latency, compared with repeating the failed action?

**RQ2. Handoff.** What has to be in a handoff record before the receiving agent is allowed to take the task, and what happens when a field is missing?

**RQ3. Supervision.** Can a human approval gate block designated high-impact actions while ordinary survival actions still run, and can a kill switch end the session before the next environment step?

**RQ4. Game setting.** If written permission is granted, do RQ1 through RQ3 still describe what happens when Eve and Edos act on the single closed battlegroup? This question is not studied now. No hypothesis under RQ4 is confirmatory.

RQ1 through RQ3 are about the sandbox. A "yes" on those questions is not evidence about Dune: Awakening.

## Hypotheses

Confirmatory hypotheses are checks the tests already encode. They were specified by constructing the policies and the world, then locking the resulting fingerprint so later edits cannot silently change the metric. They are not discoveries about players or about the game. See [threats-to-validity.md](threats-to-validity.md).

**H1 (confirmatory, sandbox, scenario v1).** Under the registered world and the two scripted policies, the replan policy's total recovery latency is lower than the retry policy's, and the replan run ends with no open failure episode. The retry policy is allowed to end with an open episode. The locked fingerprint is in [evaluation.md](evaluation.md).

**H2 (mechanism, sandbox).** A handoff record missing a required field is rejected. The task owner does not change. A complete record is accepted and the receiver becomes the owner.

**H3 (mechanism, sandbox).** An action in the high-impact set is applied only when the operator's approver returns true. The default approver returns false, and the denied action is replaced with rest. A session whose operator flag is false does not start. After the kill switch is armed, the loop writes `kill_switch` and stops before further environment steps.

**H4.** No confirmatory hypothesis about play in Dune: Awakening is registered.

Exploratory notes are anything noticed after reading a log that was not in H1 through H3. They will be labeled exploratory if they are ever reported. The same log will not be used both to invent a comparison and to confirm it.

## Design

### Agents

Two agents share one mock world.

- Eve starts as owner of the goal `maintain`. Her scripted rules hand off repair when base integrity is low and water is sufficient, gather when water is at or below 2, enter shelter in a storm only when water is above that line, and scout when no storm forecast is stored.
- Edos accepts `repair_base`, `recover`, and `hold_shelter`. He repairs when water is at least 3, asks Eve to refill when it is not, and on `recover` enters shelter during a storm before gathering.
- The gather-at-low-water rule ignores storms. That brittleness is part of the instrument: scenario v1 needs a failure. It is not a claim that a careful policy should act this way.
- `style: replan` responds to a failure by handing Edos a complete record. `style: retry` repeats the last environment action up to four times, then falls through to the planner rules.
- `LLMPolicy` is a plug for an injected client. It is off in scenario v1 and the command-line runner rejects it.

Roles are also written, for readers, in `scripts/configs/agents.yaml`. The runner does not load that file.

### World

Registered scenario v1, frozen in `scripts/sietch/evaluate.py`:

| Parameter | Value |
| --- | --- |
| Seed | 7 |
| Steps | 16 |
| Starting water | 4 |
| Starting base integrity | 3 |
| Storm period | 6 |
| Storm length | 2 |
| Water cap | 8 |
| Base cap | 10 |

Storms are on when `tick % 6 >= 4`, so ticks 4, 5, 10, 11, and 16 fall inside a storm. A forecast exists only after `scout`, and the baseline policy does not use it to avoid the storm. Each environment step spends 1 water after the action. A successful `gather_water` adds 2 first, for a net gain of 1, unless the agent is unsheltered in a storm, in which case the gather fails as `exposure` and only the 1 water cost applies.

A handoff does not spend a world step. A second handoff on the same observation is rejected as churn, and a rest step follows. This is a sandbox simplification. Whether a conversation would take time in the game is an open question.

### Supervision

Every run requires a human operator. The approval gate and the kill switch are specified in [supervision.md](supervision.md).

### Conditions

Two conditions, same world, same step cap, same seed:

1. Replan (`configs/sandbox.yaml`)
2. Retry (`configs/sandbox-retry.yaml`)

There is no human-subject condition. There is no game condition.

## Sample, stopping, and exclusions

Scenario v1 is one deterministic episode per condition. The sample size is 1 per policy because the output does not change when the seed, the code, and the config stay fixed. Repeating it estimates nothing statistical. It checks that the metric code still matches the fingerprint.

Stopping rule: 16 environment steps, or sooner if the kill switch is armed. H1 uses runs that are not killed.

Exclusions:

- A run that refuses to start because the operator is absent is not a sample. It is a passed safety check.
- A run stopped by the kill switch is reported separately and is not pooled into H1.
- A run with `real_game_connection: true` cannot start. It is not a sample.

No game sessions are included, whatever their outcome, until a written answer allows them and a protocol for them exists.

A future game study's number of sessions, session length, and participant count are open questions. This plan does not pick numbers for them. **Proposed, pending Funcom review:** choose those numbers in a short addendum, and freeze that addendum before the first agent session, after any conditions from Funcom are copied in.

## Analysis

For H1, compute total recovery latency (the sum of the episode latencies) and the unrecovered-episode flag, using the definitions in [evaluation.md](evaluation.md). The expected relationship is the fingerprint locked by the test. No p-value, confidence interval, or normality assumption is used. The policies are deterministic, so a significance test would be theater.

For H2 and H3, the analysis is a pass or fail on the mechanism tests in `scripts/tests/`.

Missing data: if a session ends with an open failure episode, `unrecovered_failures` is 1 and that episode contributes no latency. It is not imputed.

Multiple comparisons: the only confirmatory ordering is replan versus retry on scenario v1. Extra slices of the log are exploratory.

## Reporting

Sandbox results, if written up, will say they are properties of these policies in the mock world. They will point at the test that locks the fingerprint. They will not be described as player behavior or as findings about Dune: Awakening.

Any public writeup that discusses the game study, if that study ever happens, is covered by the offer in the request: Funcom gets a first look before publication. That offer is not a claim that a writeup is scheduled. Timeline is an open question.

## What would change the plan

A written answer from Funcom. Conditions in that answer replace conflicting proposals in this draft. A refusal ends the game aim. The sandbox can remain as a methods exercise either way. Record the change in [deviations.md](deviations.md).

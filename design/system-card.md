# System card

A model card, in the sense of Mitchell et al. (2019), reports intended use, evaluation conditions, and limits for a released model. Hugging Face's model-card guide asks for the same kind of human-readable sections. This file uses that shape for the sandbox agents. There is no trained model, no weight file, and no Hub upload. Citation: [../docs/references.md](../docs/references.md).

> **Permission status.** Written permission from Funcom has been requested and is pending. These agents do not play Dune: Awakening.

## Model details

- **Name:** Sietch sandbox agents, Eve and Edos, version 0.1.0.
- **What it is:** Two rule-based policies and an orchestrator. `ScriptedPolicy` is the default. `LLMPolicy` is an empty plug.
- **What it is not:** A neural network, a fine-tune, or a model trained on game data.
- **Developer:** Daniel Schott, with drafting help credited in the README.
- **License:** Unlicense for this repository's code and text. No rights are granted in Funcom or Dune trademarks or game assets.
- **Language:** Action names and log fields are English identifiers. The policies do not take free-form player chat in scenario v1.

## Intended use

- Run the registered sandbox scenario and the unit tests.
- Inspect how a complete handoff record differs from a rejected one.
- Inspect how an approval gate and a kill switch wrap a two-agent loop.
- Give a reader a concrete design to comment on while permission is pending.

## Out of scope

- Acting in Dune: Awakening, or in any other game client.
- Unattended operation.
- Farming, boosting, real-money trading, or leaderboard play.
- Training a public model on Funcom assets.
- Contact with players outside a research group. There is no research group in the sandbox, and there is no network session.
- Decisions about real people, accounts, or moderation.

## Factors and limitations

The behavior depends on hand-written thresholds: gather at water 2 or below, repair only at water 3 or above, storms on two ticks out of six, handoffs that cost no world time. Changing a threshold changes the fingerprint. The policies ignore the storm forecast that `scout` stores. That is deliberate brittleness, documented in [../methodology/threats-to-validity.md](../methodology/threats-to-validity.md).

The system has no demographic factors. It does not see a person. Fairness claims across groups of people are not applicable. The ethical limit is about where the agents are allowed to run, not about a classifier's error rates.

## Metrics

Defined in [../methodology/evaluation.md](../methodology/evaluation.md): handoffs accepted and rejected, failure episodes, recovery latency, unrecovered episodes, approval blocks, kill-switch stops.

Scenario v1 fingerprint (seed 7, 16 steps), locked by the test:

| | Replan | Retry |
| --- | --- | --- |
| Handoffs accepted | 4 | 2 |
| Failures | 1 exposure | 5 exposure |
| Recovery latencies | [1] | [2, 2] |
| Unrecovered | 0 | 1 |

These numbers describe the scripted policies in the mock world.

## Evaluation data

The world is generated from `WorldConfig`. No external dataset is used. No human subjects are used. Logs produced during a run are local artifacts, described in [log-datasheet.md](log-datasheet.md).

## Training data

None. Nothing is optimized. `LLMPolicy`, if a caller later injects a client, would send the observation JSON and read back an action name. That path is off. It must not be used to ship game files to a provider. See [../safety/boundaries.md](../safety/boundaries.md).

## Ethical considerations

The reason this card exists is the permission request: two persistent agents under human supervision, on one closed server, only after Funcom says so in writing. The released system stays on the safe side of that request by refusing a game connection. Misuse would be editing the guard to attach a client without written permission, or using the agents to sell access or to boost. Both are out of scope and against [../CONTRIBUTING.md](../CONTRIBUTING.md).

## Caveats and recommendations

- Quote the fingerprint only with the unit "mock world step" and with the threats file.
- Do not describe Eve or Edos as ready to play the game.
- Do not add a connector in a pull request while permission is pending.
- If a written answer arrives, update this card before any session, including any conditions Funcom sets. That update is **proposed, pending Funcom review** as a maintenance rule.

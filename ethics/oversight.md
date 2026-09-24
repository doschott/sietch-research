# Oversight

## Who is responsible

Daniel Schott is responsible for this repository and for any session started under the permission request. The operator of a sandbox run is the person who passes `--operator-present`. In the current design that person is the same researcher, unless a later protocol names someone else. Naming additional operators is an open question.

The agents are not responsible parties. Eve and Edos do not accept terms, do not hold accounts in this sandbox, and do not outrank the operator.

## What oversight requires today

- The operator is present for the process they start. "Present" means able to deny a gated action and able to arm the kill switch. The software records the attestation. It does not record a video of the operator.
- High-impact sandbox actions default to denied.
- The operator can stop the loop with SIGINT or `Supervisor.kill()`.
- The operator does not point the runner at a game client. The guard is the technical half of that duty. The duty remains if the guard is ever edited. A pull request that adds a connector before a written answer from Funcom is out of scope and should be closed. See [../CONTRIBUTING.md](../CONTRIBUTING.md).

## What oversight would require later

**Proposed, pending Funcom review.** If a written answer allows agent sessions:

- The operator is in the room for the whole session, as the request already requires.
- The session stops when the operator leaves, when the kill switch is used, or when Funcom pauses or ends the exception.
- The written protocol for that session, including any conditions Funcom sets, is the procedure the operator follows. This ethics note does not replace those conditions.
- The agents still do not interact with players outside the research group, including in the Deep Desert and social hubs.

## What the agents are not allowed to become

The request rules out selling access, boosting, and real-money trading. Oversight includes refusing any use of the agents for those purposes, on the sandbox and on any future server. The sandbox has no market and no currency. A contribution that adds either one, aimed at the game, is out of scope.

The request also rules out training a public model on Funcom assets. Oversight includes keeping game files and game output out of training corpora. Scenario v1 does not train a model.

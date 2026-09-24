# Threats to validity

Limitations of the sandbox study. The NeurIPS checklist's limitations question is answered by this file together with the system card. A limitation that is written down is part of the plan, not a defect to be smoothed over.

## The scenario was built to fail in a particular way

Eve gathers when water is at or below 2, including in a storm, and she does not use the scout forecast to get to shelter first. Edos, once handed `recover`, does take shelter. The replan policy therefore has a recovery move that the retry policy, which repeats the gather, does not use until several repeats are spent.

H1's ordering is a property of that construction. It shows that the metric can tell the two policies apart. It does not show that "replan" is a good general strategy, that the same gap would appear for other policies, or that a language model would behave like either script. A reader who quotes the latency numbers without this paragraph is misreading the study.

## Construct

The mock world uses the words water, storm, shelter, and base because the request names survival pressures of that kind. The numbers are invented thresholds (water at most 8, storms on two ticks out of six). Vehicles, markets, other players, and the game's actual rules are absent. A handoff that works on this API can still be the wrong shape for a game client. The API is abstract on purpose: it keeps the repository away from game memory, packets, and files.

Recovery latency treats any step with a null failure as recovery, including a step that only got lucky because the storm ended. The retry fingerprint includes closed episodes of length 2 as well as an episode that is still open at step 16. Those are different outcomes. The total-latency comparison ignores that difference except for the separate unrecovered flag. Reports should keep both numbers.

One open episode at a time means overlapping failures do not each get a latency. That matches the code. It is a coarse definition.

Handoff cost is zero world-time, with a churn cap of one accepted handoff per observation. A game in which talking takes time would change both the latency and the churn result. That timing is an open question.

The approval list (`abandon_shelter`, `discard_water`) was chosen so a test can force a gated action. It is not a risk assessment of the game.

## Internal

The policies, the world, and the metric live in one process and share the observation object. There is no separation between the agent and a real environment beyond a Python method call. Bugs in the metric can agree with bugs in the policy and still pass. The fingerprint test catches changes. It does not prove the definitions are the right ones. Two people reading [evaluation.md](evaluation.md) can recompute the replan latency from the log by hand: exposure at tick 4, close on the next clean step, latency 1. That hand check is the protection against a metric that only passes because it is circular.

The operator flags are booleans. They do not measure whether a person was watching. Tests set the flag true. That shows the software refuses a false flag. It does not show human supervision of a game.

## External

Nothing in scenario v1 generalizes to Dune: Awakening, to other games, to other group sizes, or to unsupervised agents. The request is about one closed battlegroup and two named agents with a human present. Even a future permitted study would be a single-server case study. A refusal from Funcom leaves the sandbox as a methods exercise with the same external limit.

The scripted policies are not the agents that would eventually play, if permission were granted and a reviewed connector existed. Results would have to be collected again under that protocol. H4 is intentionally empty.

## Reporting

Deterministic code invites false precision. "Latency 1" means one world step in this mock, not one second and not one game tick of Dune: Awakening. Writeups should keep the unit attached to the number.

Exploratory comments added after reading logs are not confirmatory. [deviations.md](deviations.md) is where a changed hypothesis goes.

## What would reduce these threats

A second scenario written before it is run, with a policy that uses the forecast, would test whether H1 is only the brittle gather rule in disguise. That scenario is not registered yet. Adding it later is a deviation or a new study, not a silent edit to v1.

A permitted game study would need its own protocol, its own metrics, and Funcom's conditions. The sandbox threats would still apply to the sandbox. They would not be cured by going into the game. The game study would add threats of its own: a single operator, a single server, and a connection method that is still an open question.

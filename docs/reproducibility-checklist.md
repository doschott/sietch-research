# Reproducibility checklist

This file answers the questions in the NeurIPS Paper Checklist Guidelines (https://neurips.cc/public/guides/PaperChecklist), which were read on 24 September 2026. The guidelines say a "no" or "n/a" is acceptable when the justification is honest. This repository has not been submitted to NeurIPS. The answers describe the sandbox study as it stands.

1. **Claims.** Yes. The README and [definitions.md](definitions.md) state that the implemented work is an offline sandbox, that permission to enter Dune: Awakening is pending, and that scenario v1 is a property of two scripted policies in a mock world.

2. **Limitations.** Yes. See [methodology/threats-to-validity.md](../methodology/threats-to-validity.md) and the caveats in [design/system-card.md](../design/system-card.md). The scenario was built so that a brittle gather rule fails in a storm. The ordering between replan and retry is a property of that construction.

3. **Theory, assumptions, and proofs.** N/A. The repository states no theorems.

4. **Experimental result reproducibility.** Yes for the sandbox. Scenario v1 is fixed in `scripts/sietch/evaluate.py` and locked by `scripts/tests/test_session.py`. N/A for play in Dune: Awakening, because that play has not happened and will not happen without written permission.

5. **Open access to data and code.** Yes for the sandbox code, the config, and the test command. There is no game dataset. Session logs produced on a local machine are gitignored because they are run artifacts, and the test regenerates the fingerprint without committing a log file.

6. **Experimental setting.** Yes for the sandbox. Seed 7, 16 steps, the world parameters in `REGISTERED_SCENARIO_V1`, and the command line are in [methodology/reproducibility.md](../methodology/reproducibility.md). There are no trained-model hyperparameters.

7. **Statistical significance.** N/A. The world and the scripted policies are deterministic. The plan does not report p-values. A future stochastic setup would need its own pre-registered analysis. That setup is not part of scenario v1.

8. **Compute.** Yes. The tests and the 16-step session are CPU-only and finish in well under a minute on a laptop-class machine. No GPU, cluster, or paid API is required. The checked run used Python 3.12.

9. **Code of ethics.** N/A as a NeurIPS submission question, because there is no submission. The project's own oversight, consent proposals, and stop rules are in [ethics/](../ethics/README.md) and [safety/](../safety/README.md). The NeurIPS Code of Ethics was not a document this checklist claims to have applied item by item.

10. **Broader impacts.** Yes, at the scale of this project. The work asks to put automated agents in a commercial game. The request limits that to one closed, invite-only battlegroup, with a human present, and rules out unauthorized clients, packet interception, memory editing, anti-cheat circumvention, selling access, boosting, real-money trading, and training a public model on Funcom assets. The sandbox exists so those questions can be studied without touching the game. Misuse of a later connector would matter; the guard and the permission gate are the current mitigations. See [safety/boundaries.md](../safety/boundaries.md).

11. **Safeguards.** Yes for what is released. No model weights and no game assets are released. The language-model plug is inert unless a caller injects a client, and the command-line runner refuses that policy. The environment factory refuses every mode except `sandbox`.

12. **Licenses.** Yes. This repository's text and code are under the Unlicense. Third-party names are used only to say where the requested research would take place, and the Unlicense does not grant rights in those trademarks or in game assets. The sources in [references.md](references.md) are cited. No third-party game code is vendored.

13. **New assets.** Yes for the sandbox code and the log schema, documented in [design/technical-spec.md](../design/technical-spec.md), [design/system-card.md](../design/system-card.md), and [design/log-datasheet.md](../design/log-datasheet.md). No dataset of human subjects is released.

14. **Crowdsourcing and human subjects.** N/A for the sandbox. No participants have been run. Instructions, compensation, and screenshots do not exist yet. If a later study involves people, those materials would have to be written first. Consent is an open question; a proposal is in [ethics/consent.md](../ethics/consent.md).

15. **IRB approvals.** N/A for the sandbox, which has no human subjects. Whether a future study on the battlegroup needs institutional review or another ethics review is an open question. This repository does not claim that an IRB has approved anything.

16. **Declaration of LLM usage.** The sandbox's default method does not use an LLM. Drafting help for the prose is credited in the README (Grok, xAI, and Cursor agents). `LLMPolicy` is an optional plug and is not on the default path. If a later study uses an LLM as part of the agent, that use would be reported as part of the method.

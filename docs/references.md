# References

These are the sources used to shape this repository's documentation. Each one was opened while the documents were drafted, on 24 September 2026. Nothing here is a claim that Sietch Research follows a standard it has not implemented, or that a venue has reviewed the project.

## Documentation and reproducibility

NeurIPS. "NeurIPS Paper Checklist Guidelines." https://neurips.cc/public/guides/PaperChecklist

The checklist asks authors to match claims to evidence, discuss limitations, provide a path to reproduce experiments, and answer questions on ethics, safeguards, assets, and human subjects. [docs/reproducibility-checklist.md](reproducibility-checklist.md) answers those questions for this repository's current state. This repository has not been submitted to NeurIPS.

Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d'Alché-Buc, F., Fox, E., and Larochelle, H. 2021. "Improving Reproducibility in Machine Learning Research: A Report from the NeurIPS 2019 Reproducibility Program." *Journal of Machine Learning Research* 22(164): 1-20. https://jmlr.org/papers/v22/20-303.html

The report describes the NeurIPS 2019 program: a code-submission policy, a reproducibility challenge, and the Machine Learning Reproducibility Checklist. The sandbox follows the practical part of that bar: fixed seeds, a documented metric, and a test that reruns the registered scenario.

## Model and data documentation

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., and Gebru, T. 2019. "Model Cards for Model Reporting." In Proceedings of the Conference on Fairness, Accountability, and Transparency, 220-229. https://doi.org/10.1145/3287560.3287596

Model cards ask for intended use, factors, metrics, evaluation data, training data, and ethical considerations. [design/system-card.md](../design/system-card.md) uses that shape for the scripted agents. There is no trained model in this repository.

Hugging Face. "Model Cards." https://huggingface.co/docs/hub/en/model-cards

The Hub's model-card guide is a practical checklist (model, intended use, limitations, training data, evaluation) that points back to the Mitchell et al. work. The system card follows the human-readable sections, not the Hub's YAML metadata, because this repository does not publish a hosted model.

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., and Crawford, K. 2021. "Datasheets for Datasets." *Communications of the ACM* 64(12): 86-92. https://doi.org/10.1145/3458723

Datasheets group questions into motivation, composition, collection, preprocessing, uses, distribution, and maintenance. [design/log-datasheet.md](../design/log-datasheet.md) answers those questions for the sandbox logs. Game-session logs are not collected. Where the September 2026 permission request is silent, the datasheet marks the item as proposed, pending Funcom review.

## Research plans

Center for Open Science. "Preregistration." https://www.cos.io/initiatives/prereg

Preregistration means writing the plan before looking at the study data, so confirmatory checks stay distinct from exploratory ones. The Center's guidance also says a preregistration is a plan, and deviations should be reported rather than hidden. [methodology/research-plan.md](../methodology/research-plan.md) is written in that spirit. It has not been deposited on OSF. Depositing it is a possible later step, not a commitment in the permission request.

Center for Open Science. "Welcome to Registrations & Preregistrations." OSF Help, article 330. https://help.osf.io/article/330-welcome-to-registrations

Used for the distinction between a registration (a frozen record) and ongoing project files. This repository's scenario fingerprint is frozen in tests. The prose can still be edited, and edits that change a metric or a hypothesis belong in [methodology/deviations.md](../methodology/deviations.md).

## Risk management

Tabassi, E. 2023. *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1. National Institute of Standards and Technology. https://doi.org/10.6028/NIST.AI.100-1

The AI RMF is a voluntary framework. Its core functions are Govern, Map, Measure, and Manage. [safety/README.md](../safety/README.md) uses those four names as section headings. That is an organizational aid. It is not a claim of NIST conformance or certification.

## Related agent research

Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., and Anandkumar, A. 2023. "Voyager: An Open-Ended Embodied Agent with Large Language Models." arXiv:2305.16291. https://arxiv.org/abs/2305.16291

Voyager is a single embodied agent in Minecraft, built from a curriculum, a skill library, and iterative prompting, and the paper studies it without a human operator in the loop. It is cited as an example of an agent study in a survival game. Sietch Research asks a different question: how two persistent agents hand off work and recover from failure while a human operator is present. Voyager's Minecraft measurements are not targets for this project.

## Citation metadata

Citation File Format schema 1.2.0. https://github.com/citation-file-format/citation-file-format

The schema guide (reviewed from the 1.2.0 document) is why [CITATION.cff](../CITATION.cff) uses `cff-version: 1.2.0` and the keys `message`, `authors`, `title`, `version`, `date-released`, `license`, and `repository-code`.

## What this list leaves out

The permission request itself is the scope authority for anything about Dune: Awakening. It is summarized in [definitions.md](definitions.md). It is not a published paper, so it is not given a bibliographic entry here.

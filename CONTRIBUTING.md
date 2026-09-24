# Contributing to Sietch Research

Thank you for your interest. Outside contributors are welcome, and contributions, reviews, and feedback from Funcom are especially welcome. If you work at Funcom and want to review the protocol, suggest conditions, or flag a concern, please open an issue or email doschott@gmail.com. We will treat that input as a priority.

## Project status

Written permission from Funcom has been requested and is pending. Until a written answer is received, this repository contains the draft protocol, ethics and safety notes, and an offline sandbox. No agent play takes place in Dune: Awakening. The sandbox refuses a real-game connection. See [safety/boundaries.md](safety/boundaries.md).

## What must never be committed

To respect Funcom's rights and keep this project clean, do not commit any of the following:

- Game assets of any kind (art, audio, models, maps, text, or extracted data)
- Game client or server binaries, or files derived from them
- Proprietary Funcom material of any kind
- Tools or code for unauthorized clients, packet interception, memory editing, or anti-cheat circumvention
- A connector to the game client, including while permission is described as "almost" granted. Wait for the written answer, then follow its conditions.
- Secrets, credentials, server passwords, API keys, or personal data
- Raw session logs (`sessions/`, `*.jsonl`)

Pull requests that include any of the above will be closed, and the content removed.

## Opening an issue

1. Search existing issues first to avoid duplicates.
2. Open a new issue with a clear title and a short description.
3. For questions about scope or boundaries, reference [docs/definitions.md](docs/definitions.md).
4. For methodology suggestions, reference the relevant section of [methodology/README.md](methodology/README.md).
5. For safety or scope questions, reference [docs/definitions.md](docs/definitions.md) and [safety/README.md](safety/README.md).

## Opening a pull request

1. Fork the repository and create a branch from `main`.
2. Keep changes focused. One topic per pull request is easiest to review.
3. Write in plain, professional English.
4. Explain what the change does and why in the pull request description.
5. Be ready for review feedback. Changes that affect scope or commitments to Funcom need the maintainer's approval.
6. For code under `scripts/`, run `python -m pytest` from the repository root or from `scripts/` and include the result in the pull request. Keep the default path offline. Do not add a network call, a provider SDK, or a key.
7. If you change scenario v1, the metric, or the fingerprint test, update [methodology/evaluation.md](methodology/evaluation.md) in the same pull request and add a row to [methodology/deviations.md](methodology/deviations.md).

## License

This project is released into the public domain under the [Unlicense](LICENSE). By contributing, you agree that your contributions are dedicated to the public domain under the same terms.

## Code of Conduct

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

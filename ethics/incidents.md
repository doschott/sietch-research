# Incidents

**Proposed, pending Funcom review**, except where a step simply repeats the September 2026 request. No game session is active, so this procedure has not been used.

## What counts as an incident

- the operator is no longer present while a process is still acting
- a sandbox run is found writing somewhere other than the mock world
- any attempt to read game memory, intercept packets, automate input into the game, or open game files
- a log that contains personal data or a secret
- a participant says they did not agree to be in the session
- Funcom asks for a pause or an end to the exception
- the operator is unsure whether an action is inside the request

A failed gather in the mock world is a research event, not an incident. It belongs in the session log.

## Steps

1. Stop. Arm the kill switch, or end the process if the switch is not the fastest way. Do not resume in the same session.
2. Leave the log file intact. Do not edit lines after the fact. A later note can explain the stop. The note goes in research notes, not by rewriting JSONL.
3. If the event touched the game, or might have, tell Funcom and include the session id and the log. The request already offers logs on request and recognizes Funcom's right to pause or end the exception. The contact channel is the one Funcom uses for the request, unless Funcom names another. This draft does not publish a private legal address beyond the request's existing correspondence.
4. If personal data landed in a file, remove that file from any place it was copied, keep one copy long enough to fix the bug, and record the deletion date.
5. If a participant is involved, follow [consent.md](consent.md) and the Code of Conduct. Harassment reports still go to doschott@gmail.com.
6. Write a short public note in this repository when the incident changes the protocol or the code. Leave out personal data and leave out anything Funcom asks to keep private. If there is a conflict between a public note and Funcom's conditions, the conditions win.

## After a stop

The session stays stopped. A new session, sandbox or otherwise, waits until the operator can say why the stop happened and what changed. A game session also waits on the written exception still being in force.

## Sandbox drills

The tests are the drill for this codebase: operator absent, kill switch, denied high-impact action, personal-data field rejected, real-game mode rejected. A failing test of that kind is treated as a product defect, fixed before further scenario work.

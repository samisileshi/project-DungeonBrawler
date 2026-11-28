# Dungeon Brawler

## The application

We're creating a 2-player, local or online turn-based dungeon crawler. Players will compete to collect loot, level up, and raise their score to increase the chances of finding an Escape Sigil before their opponent, or before the timer runs out.

## The team

| Full name               | GitHub username       |
|-------------------------|-----------------------|
|Samuel Sileshi Nemomissa | @samisileshi          |
|Youssouf Tive Madi       | @youss1234            |
|Ibrahim Waqar Mian       | @IbrahimMain08        |
|Wilson Huang             | @Willyfrys    |
|Obaidullah Ahmad         | @obaidullahahmad-maker|


Note:  Be sure to [add all of the group members to as collaborators on this repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository).

<!-- Fill this in at Milestone 0. Teams of four: delete the fifth row.
     The GitHub username must be the one that authors your commits, so your work in the
     history can be matched to you - check yours with:  git log --format='%an <%ae>'
     Who owns which slice, and what each member contributed, go in CONTRIBUTIONS.md. -->

## Running it

```
python main.py
```

## Design

<Leave this until Milestone 3. Then add, in about a page: how the pieces fit together
(server, client, engine, storage), and a short **Big-O note** for the algorithm your team
implemented - what it does, its complexity, and why that is fast enough here.>

### F15 Special Dungeon Events (Obaidullah Ahmad)

- **Data structure - queue.** `EventQueue` in `surprises.py` is a linked-list queue of the
  surprise events planned for the dungeon. Events are drawn first in, first out, so players
  get them in the order they were planned. `enqueue` and `dequeue` are both O(1).
- **Algorithm - greedy difficulty balancer.** `SurpriseDeck.balance_events(difficulty, n)`
  plans `n` events whose total damage gets close to the difficulty's damage budget
  (easy 15, normal 35, hard 60) without going over it. For each slot it greedily takes the
  most damaging event that still fits, with each type used at most `n // 2` times, then
  shuffles the plan into the queue.
  **Big-O:** sorting the `k` event types is O(k log k), and each of the `n` slots scans at
  most `k` types, so O(n * k). With only k = 4 event types, that is O(n). A batch is 6 events,
  so this is instant.
- **Sockets + concurrency.** `surprises_net.py` runs a `ThreadingTCPServer` (one thread per
  client). Clients send JSON lines (`join`, `surprise_step`), and the server replies with
  `surprise_result` or `error`. All players share one deck, and a `threading.Lock` makes
  sure two threads never dequeue at the same time.
  Run: `python surprises_net.py server --difficulty hard`, then in two other terminals
  `python surprises_net.py client --name A` and `--name B`.

## Required Files

| File | What it is |
|------|------------|
| [`MILESTONES.md`](MILESTONES.md) | **the project requirements** - all four milestones, what's due when |
| [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) | who owns which slice, and which commit proves each member did each topic |
| [`AI-USAGE.md`](AI-USAGE.md) | the AI policy, and your team's disclosure |
| [Team planning doc](https://docs.google.com/document/d/18wfBg2EickYXuJv-wgNtfbcqCjU2-CmAEXHq6eLfEoc/edit) | full game design and the feature claim list for each milestone (Google Doc) |

> **This file is yours.** The sections above are part of your Milestone 0 write-up - fill
> them in together, and fill in the slices table in `CONTRIBUTIONS.md` at the same time.
> From Milestone 1 on, grow "The application" and "Running it" into a real README for your
> project, and keep the team table, the tech plan, and these pointers.

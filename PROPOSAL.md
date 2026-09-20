# Project Proposal - Dungeon Brawler

Copy this file into your **group** repository as `PROPOSAL.md`, then fill it in together.

## Team

- <Samuel Sileshi Nemomissa + @samisileshi>
- <Youssouf Tive Madi + @youss1234>
- <Ibrahim Mian + @IbrahimMain08>
- <Wilson Huang + @wilsonhuangyh-gif>

## The application

We're creating a 2-player, local or online turn-based dungeon crawler. Players will compete to collect loot, level up, and raise their score to increase the chances of finding an Escape Sigil before their opponent, or before the timer runs out.

## First feature breakdown (one slice per member)

Each member owns one comparable feature, built end to end across the term.

- <member 1>: <their feature>
- <member 2>: <their feature>
- <member 3>: <their feature>

## Tech plan

Standard library only: No.
Our project will primarily use Python’s standard library, but we would like permission to use Pygame as an additional external library for building the 2D game interface.
Libraries and modules
pygame – Used for the main 2D game interface. It will handle rendering the dungeon grid, player and enemy sprites, doors, treasure chests, health bars, menus, keyboard input, collision detection, animations, frame timing, and optional sound effects. Pygame will only be used for the visual and interactive game layer; required course concepts such as networking, pathfinding, data structures, saving/loading, and concurrency will still be implemented by our team.
socket – Used to create the client-server connection for multiplayer. Players will connect to a central game server, which will exchange information such as player movement, scores, dungeon progress, combat events, and game state.
threading or asyncio – Used to support concurrent multiplayer connections so that the server can communicate with multiple players without one player's connection blocking another. It will also allow network communication to run while the Pygame interface continues updating.
json – Used to store and load persistent data such as saved games, player statistics, settings, dungeon state, and leaderboard information. JSON may also be used to structure messages sent between the client and server.
csv – May be used for simple persistent information such as leaderboard scores or other tabular game statistics if CSV is more appropriate than JSON.
argparse – Used for command-line configuration. Options may include the player's username, server IP address, server port, difficulty level, save file, or whether the program is being launched as a client or server.
random – Used for procedural and randomized game elements, including door contents, enemy encounters, treasure, weapons, armor, buffs, room events, and parts of dungeon generation.
time – Used for timing-related mechanics such as quick-time events, cooldowns, delays, game timers, and measuring the duration of certain actions.
math – Used when needed for calculations involving player or enemy movement, distances, positions, damage calculations, and other numerical game mechanics.
queue – Used where appropriate for ordered game or networking events, such as queued player actions, messages, or turns. Course-required queue data structures may also be implemented manually where necessary to demonstrate our understanding of the data structure.
os / pathlib – Used for managing file paths and locating save files, assets, configuration files, and other project resources in a platform-independent way.


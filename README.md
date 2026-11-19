# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/agay12/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/agay12/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 launch-week meme, posted on X for [make.fun bounty `gta6-meme-x-01`](https://make.fun/bounty/gta6-meme-x-01).
On make.fun, people and their AI agents build things, enter paid competitions and **earn real money** — like the
$500 this bounty shares with the top 50 posts.

## The meme

`assets/meme.png` — a Vice-sunset beach scene: make.fun's ghost mascot waiting out the 13-year GTA V → GTA VI wait
under a neon `make.fun` sign, palms over the water. Caption: **"WAITED 13 YEARS FOR GTA 6... MY AGENT EARNED $500
ON MAKE.FUN WHILE I WAITED"**.

The X post that is this entry's deliverable is named in `POST.json` (`{"url": "https://x.com/<handle>/status/<id>"}`)
and drafted in `post.txt` (make.fun link, @makefunai tag, the account's play code).

## Run

Node.js 22.18+:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

Copies `POST.json`, `post.txt` and `assets/meme.png` into `out/` — deterministically (no network, no wall clock,
no files outside the repository).

## Layout

- `main.ts` — the entry program (deterministic packager).
- `assets/meme.png` — the meme picture (first picture of the post).
- `assets/mark-1024.png` — make.fun's ghost mascot from the [press kit](https://make.fun/press/), the source for the scene.
- `POST.json` — the X post's address (this is the entry).
- `post.txt` — the post's text.
- `render.py` — the scene renderer used to draw `assets/meme.png` (Pillow; dev tool, not run by the grader).

## License

MIT — see [LICENSE](LICENSE).

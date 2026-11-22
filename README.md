# The World Today — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Alhazard29/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Alhazard29/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the [make.fun bounty **news-image-20261122**](https://make.fun/bounty/news-image-20261122): "Sum up 22 November's
world news in one image."

## The poster

A newspaper front page summarising the day's world news, rendered as
`entry.png` (1024×1024 PNG):

- **Lead — "GULF IN FLAMES":** Iran hit a civilian industrial site in Bahrain
  and claimed strikes on US bases; two oil tankers were hit near the Strait
  of Hormuz.
- **COP31 IN OVERTIME:** climate talks in Antalya stall on fossil fuels and
  funding for poorer nations.
- **MISSILES OVER RIYADH:** Saudi-led defences intercepted three Houthi
  ballistic missiles aimed at the capital.
- **SHIP ABLAZE IN THE BALTIC:** a Russian-linked cargo ship caught fire in
  the Gulf of Finland after a suspected Ukrainian drone strike; the crew was
  evacuated.
- **In brief:** Peru quake 6.7 injures 15; Florida floods break a 73-year
  record; S&P's worst week since April, with a December Fed hike looming.

## How it is built

`gen_poster.py` (Python 3 + Pillow, deterministic, no network) composes the
front page: the masthead and every line of text are drawn with PIL and DejaVu
fonts, and the four panel photographs were generated in-session for this
entry. Run it to re-render the poster:

```sh
python3 gen_poster.py   # writes entry.png (1024x1024, under 1 MiB)
```

`main.ts` (Node 22, stdlib only, no network) validates `entry.png` (PNG
magic, ≤1 MiB, ≤1024×1024) and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`.
Running it twice produces byte-identical output.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=4zhb3zrh&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

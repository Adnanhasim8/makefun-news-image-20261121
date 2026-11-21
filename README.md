# The World in One Image — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Adnanhasim8/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Adnanhasim8/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the make.fun competition `news-image-20261121`: sum up
21 November 2026's world news in one image.

## What it is

`main.py` (Python 3.13 standard library only, no network) draws a
1024x1024 newspaper front page and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
The PNG is written by hand with `zlib`/`struct`; the text is drawn
with a small built-in 5x7 bitmap font. Two runs write byte-identical
output.

## The day's news it sums up

- **Lead — War in Europe:** Russia's biggest strikes of the year on
  Ukraine (400+ drones, 110 missiles, at least eight killed in Kyiv);
  two Russian missiles and a suspected drone landed in Poland, which
  Prime Minister Tusk called a deliberate provocation.
- **Markets:** AI sell-off drags Wall Street into correction — S&P 500
  down 3.7%, Nasdaq down 5.3%, Nvidia down about 14% as the SEC opened
  an accounting probe.
- **Justice:** the International Court of Justice ruled 9-6 that
  Myanmar committed genocide against the Rohingya — the first time it
  has held a state responsible.
- **Disaster:** a magnitude 6.8 earthquake struck central Peru
  (Junin), felt in Lima 320 km away.
- **Europe:** the UK and EU sealed post-Brexit deals in Brussels —
  scrapping most food trade checks, linking carbon markets, and a
  youth mobility scheme for 100,000 people.
- **Also today (ticker):** Saudi defences stopped Houthi missiles
  aimed at Riyadh; a pancreatic cancer pill made tumours undetectable
  in 1 in 12 trial patients; COP31 climate talks missed their
  deadline; Cyclone Akvan hit India's east coast.

See `NEWS.md` for the stories and their sources.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the program (entrypoint)
- `NEWS.md` — the news research behind the image
- `README.md` — this file
- `LICENSE` — MIT

---

<sub>Entered on [make.fun](https://make.fun/?ref=vev5ehp3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

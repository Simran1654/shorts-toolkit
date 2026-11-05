# shorts-toolkit

Small, dependency-free Python tools for packaging short-form videos (YouTube Shorts, TikTok,
Reels) **before** you publish them. Born in a real daily-upload pipeline and cleaned up for
anyone who posts short videos and wants a second pair of eyes on the parts that decide whether
anyone clicks: the title, the thumbnail text, and the first line out of the speaker's mouth.

No dependencies. Python 3.8+. Nothing here uploads, posts, or phones home — every tool reads
text and prints a verdict.

## What's inside

| Tool | What it does |
|---|---|
| `title.py` | Lints a title **and its thumbnail text as one unit** — length against the desktop (~60 char) and mobile (~40 char) cuts, vague-word and all-caps checks, and the most common packaging mistake: a thumbnail that just repeats the title. Can rank a whole file of candidate titles. |
| `hookscore.py` | Scores a spoken hook (the first ~10 seconds) on five properties — specificity, address, stakes, curiosity, brevity — with a weakest-link-weighted verdict, and classifies it against 21 known hook formulas (`hooks.json`). |
| `templates/description-template.md` | A description structure plus the rules behind it: first-two-lines discipline, the three-query test, honest tags, and a sane hashtag count. |

## Quick start

```bash
git clone https://github.com/Simran1654/shorts-toolkit.git
cd shorts-toolkit
python3 title.py --title 'I Fixed a Leaky Tap With a $1 Rubber Band' --thumb 'ONE RUBBER BAND'
python3 hookscore.py examples/hooks.txt
python3 -m unittest discover -s tests   # smoke tests
```

## title.py

```text
$ python3 title.py --title 'I Fixed a Leaky Tap With a $1 Rubber Band' --thumb 'ONE RUBBER BAND'

  "I Fixed a Leaky Tap With a $1 Rubber Band"
  41 chars   score 80/100
    x  mobile       a mobile feed shows about "I Fixed a Leaky Tap With a $1 Rubber..." - check the subject survives
    x  duplicate    thumbnail repeats the title on band, rubber - the thumbnail should say what the title does not
    ok              41 characters, inside the 60-character desktop cut
    ok              carries a concrete figure (1)
```

Both flags are real catches: on a phone the title is cut off right where the payoff starts, and
the thumbnail spends its three words repeating the title instead of adding something new.

Rank a batch of candidates (one per line) and keep the best:

```bash
python3 title.py examples/titles.txt
python3 title.py --title '...' --json    # machine-readable output
```

## hookscore.py

```bash
python3 hookscore.py --hook 'You are losing $40 a month to a subscription you forgot you had, and here is how to find it in 2 minutes.'
python3 hookscore.py hooks.txt           # one hook per line, ranked, winner called out
```

The verdict is 60% the mean of the five properties and 40% the weakest one — deliberately.
A hook with four strong properties and one dead one leaks at the dead one, and a plain average
hides that.

**Honest limits:** measured against real short-form hooks, this scorer separates deliberately
bad hooks from real ones well, and separates a creator's own hits from their own misses barely
at all. Treat a low score as a reason to look again — never a high score as a promise.

## templates/description-template.md

The description rules that pair with the tools: the first two lines are the only ones anyone
reads, the three search queries your video should win, and why a wall of tags is not a strategy.
Includes a fill-in template and a worked example.

## Contributing

Issues and pull requests are welcome — especially new vague-word candidates, hook formulas with
a worked example and a failure mode, and translations of the word lists. Keep the tools
dependency-free; that is the point of them.

## License

MIT — see [LICENSE](LICENSE).

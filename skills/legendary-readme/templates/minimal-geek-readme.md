<!-- Minimal Geek README Template — lightweight, Tone Spectrum level 2 (Friendly Nerd), for small utilities/libraries that don't need the full section set. Character over volume: one joke, not ten. -->

# husht

> Runs your noisy command. Says nothing unless it breaks.

[![npm](https://img.shields.io/npm/v/husht?color=blue)](https://www.npmjs.com/package/husht)
[![build](https://img.shields.io/badge/build-passing-brightgreen)](.)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

`husht` runs whatever command you give it and keeps its mouth shut — output
only shows up if the command actually fails. Most of what cron jobs,
pre-commit hooks, and CI steps print is noise you skim past anyway, right up
until the one time it isn't. Point it at anything that talks too much:

```bash
husht -- npm run build
```

## Installation

```bash
npm install -g husht
```

## Usage

```bash
husht -- ./deploy.sh
# silence... unless ./deploy.sh explodes, then you get the full log
```

```bash
husht --always -- npm test
# --always prints output on success too, for when you don't trust "quiet" yet
```

Two flags cover most of what people ask for:

- `--always` — print output even when the command succeeds
- `--tail N` — on failure, show only the last `N` lines instead of everything

`husht` exits with your command's real exit code either way, so it's safe to
chain into a pipeline or a CI step that checks for success.

<details>
<summary>🤫 Curious what husht prints when nothing goes wrong?</summary>

Nothing. That was the whole pitch.

</details>

## Contributing

Found a bug? Open an issue with the noisy command that broke it, so we can
reproduce the noise. PRs welcome — `npm test` should stay green, loudly,
since `husht` doesn't wrap its own test suite.

## License

[MIT](LICENSE)

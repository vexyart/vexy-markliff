---
this_file: WORK.md
---

# Current state

The documentation uses fly-january 0.2.1. The release guide now describes the GitHub Actions workflow that publishes the tagged wheel and source distribution. The PyPI owner must configure or confirm the trusted publisher listed in `CHANGELOG.md`.

## Latest local checks

- All 52 tests passed on Python 3.13. Package coverage was 76% with branch measurement enabled. CI requires 80%.
- All four installed CLI commands processed sample files. Markdown `# Heading` came back as `<p>Heading</p>`. The round-trip tests establish text recovery on their fixtures.
- `./build.sh docs` rebuilt 18 HTML pages in strict mode with zero warnings. `actionlint .github/workflows/release.yml` and `bash -n publish.sh` passed.
- Across ten fresh Python processes, package import took 4.74 ms at the median (3.73–16.15 ms). Starting the installed CLI with `--help` took 145.93 ms at the median, including interpreter startup.

`TODO.md` lists the remaining work. `PLAN.md` gives the next check for each item.

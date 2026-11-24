# FAIR data, reproducible analyses and AI

Lecture for BIO390 *Introduction to Bioinformatics* (UZH), 1 December 2026.
Course page: <https://compbiozurich.org/teaching/UZH-BIO390/>

Style and parts of the content are based on
[sib-swiss/reproducible-analysis-training](https://github.com/sib-swiss/reproducible-analysis-training).

## Files

- `slides.qmd`: revealjs slide deck (with speaker notes, press `s` in the browser)
- `custom.scss`: small SIB-style tweaks on top of the revealjs default theme
- `vevox_questions.md`: audience questions, grouped by the `Question` slide where they are asked
- `polls/polls.json`: the same questions as a Vevox import file, generated with `python3 vevox_to_json.py` (rerun after editing `vevox_questions.md`)
- `img/qr_vevox.svg`: **placeholder**. Replace with the QR code of your Vevox session, and set the session code on the "Questions!" slide

## Image sources

| File | Source | License / status |
|---|---|---|
| `img/fair_image.png`, `img/five_pillars.jpg`, `img/giant_shoulder.png` | [sib-swiss/reproducible-analysis-training](https://github.com/sib-swiss/reproducible-analysis-training) | see that repo |
| `img/papers/degregori2026_fig1_tiers.png`, `..._fig2.png` | Degregori et al. (2026) *iMeta* e70192, Fig. 1–2, <https://doi.org/10.1002/imt2.70192> | CC BY 4.0 |
| `img/papers/ziemann2016_fig1.png` | Ziemann et al. (2016) *Genome Biol* 17:177, Fig. 1, <https://doi.org/10.1186/s13059-016-1044-7> | CC BY 4.0 |
| `img/screens/*.png` | Screenshots of expasy.org, uniprot.org, chat.expasy.org, alphafold.ebi.ac.uk, nf-co.re, workflowhub.eu, glittr.org (19 Nov 2026) | website screenshots, attributed on the slides |

## Render

```bash
quarto render slides.qmd
# or live preview
quarto preview slides.qmd
```

(Quarto ships with Positron: `/Applications/Positron.app/Contents/Resources/app/quarto/bin/quarto`)

## Publish

`.github/workflows/publish.yml` renders `slides.qmd` on every push to `main` (or manually via *Actions → Run workflow*) and deploys it to GitHub Pages. Rendered files are not committed (see `.gitignore`).

One-time setup on GitHub: *Settings → Pages → Build and deployment → Source: GitHub Actions*.
The deck is then served at `https://<user-or-org>.github.io/<repo>/` (redirects to `slides.html`).

## Check that nothing runs off the slides

```bash
quarto render slides.qmd
python3 check_overflow.py
```

`check_overflow.py` opens the rendered deck in headless Google Chrome, steps through every slide and reports slides whose content
runs below the slide (`OVERFLOW`), into a bottom citation (`aside`), or into the footer area (`tight`). It exits with status 1 if any slide overflows.
The canvas is the revealjs default 1050×700; the base font size is set to 32px in `custom.scss`.

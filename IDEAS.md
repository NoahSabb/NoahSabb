# Profile README Idea List

Target repo: `NoahSabb/NoahSabb` (public, terminal-themed neofetch card already in place)

## How each type integrates
- **Study repo** — clone into `profile-inspiration/`, copy layout/snippets.
- **GitHub Action** — add `.github/workflows/*.yml` to NoahSabb/NoahSabb; runs on a schedule, commits an SVG.
- **Hosted embed** — paste one `<img>` URL into the README.

## Candidates

| Idea | Source | Type | External call at render | Status |
|------|--------|------|-------------------------|--------|
| Neofetch ASCII card | jeantimex/neofetch-profile (layout only) | Hand-authored block art | none (fenced code block in README) | In repo — chip motif |
| Pac-Man / arcade contribution graph | abozanona/pacman-contribution-graph | GitHub Action | none (self-hosted SVG) | Candidate — not yet wired up |
| 3D isometric contribution skyline | yoshi389111/github-profile-3d-contrib | GitHub Action | none (self-hosted SVG) | Added — candidate |
| Snake eating contribution grid | Platane/snk | GitHub Action | none (self-hosted SVG) | Candidate |
| Playable chess | timburgan/timburgan style | GitHub Action + issues | none | Candidate |
| Terminal-themed stats card | github-readme-stats (Dracula/Tokyonight) | Hosted embed | third-party Vercel | Candidate |
| Spotify now-playing | kittinan/spotify-github-profile | Hosted embed | third-party Vercel + Spotify auth | Candidate |

> Note: upstream `jeantimex/neofetch-profile` is a **hosted Vercel API** that converts your
> avatar to ASCII server-side (`![](https://neofetch-profile.vercel.app/api?username=...)`),
> so it *does* make an external call at render. Only its layout is borrowed here — the card
> in README.md is hand-authored Unicode Block Elements (U+2580–U+259F), no external call.

## Reference profile to study
- salesp07/salesp07 — typing header + snake + stats/streak + skillicons combo

## To browse later
- abhisheknaiidu/awesome-github-profile-readme — big curated gallery of profile READMEs; go through for more ideas

## Open placeholders to fill in README
- hobbies
- LinkedIn
- portfolio

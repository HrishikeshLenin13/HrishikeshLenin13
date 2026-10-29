# Hrishikesh Lenin — Interactive Engineering Portfolio

A self-contained 3D portfolio inspired by the exploratory interaction of Bruno Simon, the spatial systems metaphor of Merouane Bali, and the focused object interaction of modern React Three Fiber portfolios. This is an original implementation, not a fork or template.

## Why this approach

- **Actual real-time 3D projection:** a lightweight canvas engine constructs a 3D mesh, orbital rings, depth-sorted project satellites, camera controls, and perspective ground grid. No external JavaScript dependencies.
- **Usable without the animation:** all projects have readable HTML cards, keyboard-operable filters, and public source links when available.
- **Performance:** pixel ratio capped, animation pauses offscreen, reduced-motion preference honored, no external models or heavy assets.
- **Honest claims:** Helix and Atlas are labeled private; no fabricated award, company employment, adoption, or benchmark statistics.

## Try it

From this directory:

```sh
python3 -m http.server 8000
```

Visit http://localhost:8000.

## Deployment

This directory can be used as the Vercel Root Directory (`portfolio`) for the profile GitHub repo. Framework preset: Other. No build command, no Node dependencies. Vercel serves static files.

## Personalization

Project titles, summaries, tags, and source URLs live in `portfolio.js`. The visual geometry is in `scene.js`, with styling in `styles.css`.

## Accessibility and limitations

The 3D canvas is decorative/interactive, but not the only method of navigation; controls and content are normal HTML elements. Animations honor the visitor's reduced-motion preferences. For accessibility, project selection is also possible through buttons on the page and next/previous controls. This is a personal portfolio, not a claim of commercial deployment quality or validated project benchmarks.

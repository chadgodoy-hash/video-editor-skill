# Brand Kit for Video Graphics

Fill this in once. Claude loads it at the start of every edit. The values below are an example (navy + blue) — replace them with your own.

## Colors (CSS tokens)

```css
:root {
  --navy: #0b2058;   /* primary — panels, end card background */
  --navy2: #0e2a6e;  /* end-card decorative circles */
  --blue: #2563eb;   /* action — accent bars, number badges, fills */
  --light: #3882f6;  /* secondary accent — highlighted words, labels */
  --pale: #eaf3ff;   /* light fills, secondary text on dark */
  --white: #ffffff;
}
```

- Panels: primary color at 95% opacity over footage, 22px radius, left accent bar gradient light → blue.
- Highlighted words: `--light`.

## Typography

- **Poppins** 700/800 — headlines, numbers, wordmark, keywords in captions.
- **Montserrat** 500–700 — labels (uppercase, letter-spacing 0.16em), captions, small text.
- Font files ship in `assets/fonts/` (woff2). HyperFrames needs a local `@font-face` for every named font. Using other fonts? Add their woff2 files there.

## Brand lines

- Name (lower third + end card wordmark): **YOUR NAME**
- Role line: **e.g. Virtual Assistant & Creator**
- Site: **yoursite.com**
- Tagline (end card slams): **e.g. LEARN | BUILD | GROW**

## Logo

- Logo file: `assets/logos/<your-logo>.svg` (white version for dark backgrounds). If you don't have one, use the wordmark text — never redraw or approximate a logo.

## Voice on screen

- Tone: e.g. clear, practical, encouraging.
- Caption language: e.g. keep captions in the language you spoke; keep panel headlines in English.

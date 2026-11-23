---
name: openms-brand-guidelines
description: OpenMS corporate design rules (colours, hex/CMYK values, fonts and sizes, logo usage, clear space, accessibility and contrast, print). Use for any design decision in this repo, such as choosing a colour, font, backdrop or logo version, or checking a design against the brand, even if the user doesn't mention "brand" or "guidelines".
---

# OpenMS brand guidelines

Source: `OpenMS_CorporateDesign_current.pdf` (2025, 8 pages) in the repo root.
Machine-readable values are in `openms_logo/brand.py`; import them, don't retype them.
If a question isn't covered here, read the PDF (`pdftotext -layout` or render the pages)
before you answer. Don't guess.

## 1. Typography

| Use | Font | Weight / size |
|---|---|---|
| Titles, large headings | Montserrat | ExtraBold 26 pt |
| Chapters, headings | Montserrat | Bold 20 pt |
| Smaller headings | Montserrat | SemiBold 16 pt |
| Body text, secondary headings | Raleway | Regular. Text 11–14 pt, slides 18 pt, web ≥ 11 pt |
| Quotes, callouts, emphasis | JetBrains Mono | Thin, 1 pt smaller than body (Raleway 11 → JBM 10) |
| Logo-style or whimsical special use | Montserrat Alternates | matches the logo |
| Modern / tech special use | Chakra Petch | Bold, Latin |

- Raleway uses oldstyle numerals. Where numbers must share a baseline, set them in Montserrat Regular.
- Raleway is thin, so prefer the larger sizes for readability.
- All fonts are free (Google Fonts). `python scripts/fetch_fonts.py` downloads them.

## 2. Colours (RGB, for screen)

Tints and shades run lightest → darkest. **Bold** marks the logo colour.

| Hue | Values |
|---|---|
| Yellow | #ffe29e, **#ffcb4f**, #ffb401, #b27d00, #634600 |
| Orange | #ffca9e, #ffa04f, **#ff7501**, #b25100, #632d00 |
| Pink | #ffa0ec, #ff52db, **#ff03cb**, #b4008f, #660051 |
| Purple | #e3a0ff, #cc51ff, **#b503ff**, #7f00b4, #480066 |
| Blue | #bfcbf8, #7891f1, **#3157e9**, #1436b8, #0c2171 |
| Blacks | #000000 (pure), **#231f20** (logo black), #4d4446 |
| Greys | #76696c, #9d9094, #c2babc |
| Whites | **#ffffff** (pure), #f9f8f9 (grey off-white), #fff9ec (yellow off-white) |

The PDF names a few swatches: #b4008f is the "tetradic pink", #7f00b4 the "central purple", and #3157e9 the "analogous blue".
For extra tints or shades, derive them from these colours with a tool such as ColorHexa. Don't invent unrelated hues.

## 3. Print (CMYK)

Use these values rather than converting from RGB. Print at ≥ 300 dpi and follow the printer's specs.

| yellow | orange | pink | purple | blue |
|---|---|---|---|---|
| 0, 20, 59, 0 | 0, 52, 86, 4 | 0, 90, 40, 8 | 0, 78, 21, 29 | 100, 43, 0, 36 |

## 4. Logo

- Letters are Montserrat Alternates. The capital **M** is Montserrat. The PDF describes the weight as "SemiBold + 0.5 stroke". The official outlines measure as Regular + stroke; see AGENTS.md "Known discrepancies".
- The gradient runs yellow → orange → pink → purple → blue across the bars, left to right.
- **Standard logo**: letters #231f20, for light backdrops. **White logo**: letters #ffffff, for dark backdrops. The bars are the same in both.
- **Only the official files are valid** ("Do not use any other logo versions"). Generate them with `python -m openms_logo full`. Anything else you build is a *derived sublogo* that needs the brand owner's approval. Say so whenever you deliver one.
- Keep clear space around the logo (repo default `brand.CLEAR_SPACE` = half the M cap height), and don't use it below a readable size.
- Don't stretch, rotate, recolour, outline, add effects to, or re-typeset the logo. Don't rearrange the official bars inside the full logo.

## 5. Accessibility

- Contrast ≥ **4.5:1** for normal text, ≥ **3:1** for large text and graphics. Check it (formula below). Use the standard logo on light backdrops and the white logo on dark ones.
- Don't rely on colour alone. Add shape or texture (redundant encoding), and keep red-green colour blindness in mind (about 8 % of men). Simulate colour-vision deficiency for charts.
- Avoid flashing or fast animation, and respect reduced-motion settings.
- On the web, give images alt text (generated SVGs include a `<title>`), give media captions or transcripts, use large and well-spaced touch targets, support keyboard navigation, and write descriptive link text.
- Write in plain language and avoid jargon.

Contrast check:

```python
def lum(h):
    c = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
```

## 6. Examples in the PDF

Page 8 shows three examples:

- A dark roll-up banner: the white logo on a near-black backdrop, decorated with spectrum-like bars and peaks.
- A business-card front: the white logo on a dark backdrop, with faint mass-spectrum peaks behind it.
- A PowerPoint section header: a purple-to-magenta gradient band with white Montserrat text and a grey subtitle. The footer carries the date, the title and the small standard logo at the right.

The PDF's own chapter headers are dark-purple bars (#480066 family) with white Montserrat Bold text. Match these patterns when you make slides or print material.

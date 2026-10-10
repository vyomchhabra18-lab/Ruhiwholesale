# Ruhi Wholesale – clean-up and SEO changes (10 Oct 2026)

## Folder structure (deploy tree)
- `assets/images`, `assets/images/thumbs`, `assets/css` (pdp.css, site-extras.css), `assets/js` (firebase-cart.js), `docs/`, `tools/`
- Product pages (`indian-*`, `poly-*`, `imported-*`) now load one shared stylesheet and one shared Firebase cart script instead of ~14 KB of identical inline code each (pages are ~45% smaller).
- Removed from the deploy tree (kept in the separate archive zip, nothing deleted): duplicate `site/` mirror, duplicate `ruhi-wholesale-assets/`, raw WhatsApp originals, nested zip, unused JPEG/PNG copies, the hosting placeholder `index2.html`, `runtime-test.html`, and the retired `wholesale-ladies-tshirts.html` (its 301 stays in `.htaccess`).
- Fixed a stray `</div>` in `index.html`; removed an older conflicting Organization/WebSite schema block from `index.html`.

## Category rules
| Category | Shown on every page | Colour warning |
|---|---|---|
| Indian | Available Size: XL Only | never |
| Poly Cotton | Available Sizes: XL & XXL | never |
| Imported Tensils | Available Sizes: XL & XXL | bold red IMPORTANT NOTE (exact text) |
The warning also appears on the Tencel category page and the Imported gallery page.

## SEO
- One shared Organization + ClothingStore + LocalBusiness + WebSite JSON-LD graph (31 `alternateName` values, founder Ruhi Singh) on the homepage and every product page; `SCHEMA_ORG_JSONLD.json` is generated from it (`python3 tools/make_schema_json.py`).
- `python3 tools/generate_sitemap.py` rebuilds `sitemap.xml` from real, indexable, self-canonical pages with `<loc>`, `<lastmod>` (changes only when a page changes) and `<changefreq>`.
- Homepage title: "Ruhi Wholesale | RuhiWholesale – Ladies Clothing B2B Store, Delhi".
- Editorial footer on all indexable pages.

## Verify
`python3 tools/verify.py` runs 8 passes (structure, links, category rules, size data, JSON-LD, meta/canonicals, sitemap, code syntax).

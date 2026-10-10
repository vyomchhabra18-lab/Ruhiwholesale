# Ruhi Wholesale — Realistic Product Photography Prompt Guide

Use these prompts for product marketing concepts and internal mockups. Do not imply that generated people or scenes are real customers, and do not use generated images to misrepresent actual garment construction, size measurements, stock, or product colour. For final product listings, real product photos are preferred.

## 1) Midjourney — Indian adult apparel model (poly-cotton)

**Prompt**
```text
Photorealistic editorial e-commerce photograph of an adult Indian woman model (age 25–32) wearing a simple poly-cotton oversized ladies T-shirt, relaxed natural posture, realistic fabric weight and drape, visible natural skin texture and pores, natural uneven skin tone, fine flyaway hair, understated makeup, candid neutral expression, no beauty-filter look, authentic contemporary Indian home or small garment workshop in the background, morning window sunlight from camera-left, soft ambient shadows, neutral cream and indigo surroundings, 50mm lens, eye-level camera, true-to-life proportions, crisp fabric weave and seams, premium but believable wholesale catalogue photography, no text, no watermark, no brand logo unless supplied by the user --ar 4:5 --v 7 --style raw --s 70 --chaos 3 --q 1
```

**Recommended Midjourney parameters:** `--ar 4:5 --v 7 --style raw --s 70 --chaos 3 --q 1`. If the current account does not support `--v 7`, use the newest available model and keep the other settings. For less stylisation, reduce `--s` to `35`.

## 2) Flux — Indian adult apparel model (poly-cotton)

**Prompt**
```text
Photorealistic commercial product photograph, vertical 4:5 composition. An adult Indian woman, approximately 25–32 years old, wearing a plain poly-cotton ladies T-shirt. Show realistic pores, natural skin tones and tiny complexion variations, fine flyaway hairs, relaxed shoulders and a comfortable unposed stance. The shirt must have believable poly-cotton knit texture, accurate seam placement, natural folds around the waist and sleeves, and gravity-correct draping. Place her in a real-looking Indian home studio or garment workshop with a neutral wall, a folded-fabric shelf and subtle everyday details. Soft ambient morning/window sunlight, natural shadow falloff, 50mm lens perspective, realistic colour, sharp garment texture, editorial wholesale catalogue styling. No plastic skin, no excessive retouching, no distorted hands, no text, no watermark, no invented logos.
```

**Flux settings:** aspect ratio `4:5` (e.g. `1024×1280`); guidance/CFG `3.0–3.5` where exposed; 28–35 inference steps where exposed; seed `42173` for repeatable iterations; use the same seed and reference image when matching a set. Parameter names vary by Flux host, so enter these only where the UI exposes them.

## 3) Midjourney — Indian utensils (stainless steel / copper)

**Prompt**
```text
Photorealistic Indian wholesale product photograph of a neatly arranged set of real stainless-steel kitchen utensils and a small copper vessel on a lived-in Indian kitchen counter, visible fine brushed-metal grain, physically accurate reflections of a window and nearby room, realistic soft fingerprints and tiny manufacturing marks, true metal edges and handles, warm morning window sunlight, neutral cream stone surface, authentic home kitchen background softly out of focus, natural shadow contact, 50mm lens, accurate geometry and proportions, clean editorial catalogue composition, no people required, no text, no watermark, no extra handles or duplicated objects --ar 4:5 --v 7 --style raw --s 55 --chaos 2 --q 1
```

**Parameters:** `--ar 4:5 --v 7 --style raw --s 55 --chaos 2 --q 1`.

## 4) Flux — stainless steel and copper utensils

**Prompt**
```text
A high-resolution photorealistic product photograph of Indian kitchen utensils: stainless-steel bowls, plates and serving spoons beside one copper pot. Accurate metal reflectance with soft window-shaped highlights, fine brushed-steel grain, copper's warm reddish-brown reflection, realistic small surface marks, correct thickness and believable contact shadows. Morning daylight enters from a nearby window in an authentic Indian home kitchen or small utensils workshop. Cream and warm linen background, neutral colour balance, 50mm product-photography perspective, sharp details across the objects, no mirror-like CGI chrome, no warped rims, no duplicated utensils, no text, no watermark.
```

**Flux settings:** aspect ratio `4:5` (`1024×1280`); guidance/CFG `3.0–3.5`; 28–35 steps; seed `42173` for repeatable revisions where supported.

## 5) Natural workshop / fabric detail scene

**Flux prompt**
```text
Photorealistic close-up editorial photograph inside a small Indian garment workshop in the morning. Adult worker hands gently arranging folded poly-cotton T-shirts on a clean worktable, natural fabric drape, visible knit texture, believable seams and stitching, loose fibres and small real-world imperfections, ambient sunlight through a side window, shelves and folded garments in the soft-focus background, natural colour response, documentary realism, no staged luxury showroom, no readable text, no watermark, no fake labels.
```

## Authenticity checklist
- Preserve the actual uploaded product design, colour and print; use image/reference conditioning when supported.
- Keep the model clearly adult. Prefer candid, comfortable poses and everyday Indian environments.
- Request pores, skin-tone variation, flyaway hair and natural folds; avoid “flawless”, “porcelain”, “perfect skin” or aggressive beauty retouching.
- For poly-cotton, describe knit texture, seam placement and gravity-correct drape. For utensils, specify physically accurate stainless-steel and copper reflections.
- Check hands, garment seams, print spelling, metal rims and duplicated objects at 100% zoom.
- Do not generate false product measurements, logos, testimonials or stock evidence. Never use an AI image as proof of the exact item shipped.


## 6) Realistic imported Tensils colour-preview photography

Use the supplied garment photos as the source of truth. Keep the garment design, print placement, seams, fit, and fabric texture identical to the reference. Generate one image per genuinely documented shade only; do not invent stock colours or imply customers can select a specific shade when the item is sold as a random mixed-colour bulk lot.

**Prompt**
```text
Create a photorealistic wholesale e-commerce product photograph based strictly on the supplied reference image. Preserve the exact T-shirt silhouette, graphic artwork, print placement, stitching, fabric texture, and proportions. Show an adult Indian model aged 25–35 wearing the garment in a neutral catalogue pose against a clean light-grey studio background, soft even commercial lighting, realistic fabric folds and skin texture, accurate colour reproduction, sharp garment detail, full garment visible, no text, no watermark, no invented logo, no additional design elements. The result must look like a real apparel catalogue photograph, not an illustration.
```

**Important:** Treat generated images as mockups unless the garment and shade have been verified against real stock. Never fabricate chest/height measurements, sizes, product availability, or exact colour claims. For Imported Tensils, display the notice that colours are mixed randomly in whole bulk orders and specific colour selection is unavailable.

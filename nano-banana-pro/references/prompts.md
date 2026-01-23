# Prompt Engineering Reference

Extended examples and templates for Nano Banana Pro image generation.

## Prompt Structure Template

```
[Medium/Style] of [Subject] [doing action] in [Setting/Context],
[Lighting description], [Camera/perspective details],
[Quality modifiers], [Style-specific details]
```

## Category Examples

### Photorealistic Photography

```
A professional product photograph of a vintage brass compass
on a weathered wooden table, natural window light from the left,
shallow depth of field with creamy bokeh, shot with 85mm portrait lens,
4K resolution, studio quality.
```

```
An editorial fashion photograph of a woman wearing a flowing red dress
walking through a misty forest at dawn, golden hour backlighting,
captured with a Canon 5D Mark IV, 24-70mm lens at f/2.8,
cinematic color grading, high-end magazine quality.
```

### Digital Illustration

```
A detailed digital illustration of a steampunk airship
hovering above Victorian London rooftops at sunset,
warm orange and purple sky, brass and copper metal details,
gears and steam pipes visible, isometric perspective,
high-quality game asset style.
```

```
A whimsical watercolor illustration of a cozy bookshop interior
with floor-to-ceiling shelves, a cat sleeping on a reading chair,
warm lamplight, soft pastel colors with ink outlines,
children's book illustration style.
```

### Game Assets & Sprites

```
A 2D isometric game building sprite of a medieval blacksmith forge,
pixel art style with modern detail, warm orange glow from furnace,
anvil and tools visible, stone walls with wooden beams,
clean edges suitable for game engine, transparent background.
```

```
A top-down RPG treasure chest sprite, closed position,
ornate gold trim on dark wood, gemstone inlays,
32x32 pixel grid aligned, retro 16-bit style,
pure transparent background.
```

### Icons & UI Elements

```
A flat design app icon of a lightning bolt,
electric blue gradient on dark background,
rounded corners, clean vector style,
suitable for iOS app store, 1024x1024 square format.
```

```
A minimalist line icon set for a weather app:
sun, cloud, rain, snow, and wind symbols,
consistent 2px stroke weight, white on transparent,
modern UI design, 64x64 each.
```

### Concept Art

```
A dramatic concept art painting of a lone knight
standing before a massive dragon in a volcanic cavern,
dynamic lighting with lava glow and rim light,
epic fantasy atmosphere, painterly brushstrokes,
cinematic widescreen composition, AAA game quality.
```

### Product Mockups

```
A lifestyle product mockup of a minimalist ceramic coffee mug
on a marble countertop next to a croissant and newspaper,
soft morning light from a nearby window,
Scandinavian interior design aesthetic,
clean and aspirational brand photography style.
```

### Logos & Branding

```
A modern minimalist logo design for a tech startup called "Nexus",
abstract geometric shapes suggesting connection and innovation,
clean lines, balanced negative space,
works at small sizes, professional corporate identity style.
```

### Text-Heavy Designs

Use Gemini 3 Pro for accurate text rendering:

```
A vintage-style coffee shop menu board,
hand-lettered chalk typography on dark green background,
featuring "ESPRESSO $3" and "LATTE $4" in decorative script,
rustic wooden frame, warm cafe lighting,
authentic hand-crafted appearance.
```

## Quality Modifier Reference

### Photography
- 4K, 8K resolution
- HDR, high dynamic range
- Studio lighting, professional lighting
- Shot with [specific camera/lens]
- Shallow/deep depth of field
- Golden hour, blue hour, dramatic lighting

### Digital Art
- Highly detailed
- Professional quality
- Award-winning
- Trending on ArtStation
- Concept art quality
- AAA game quality

### Style References
- In the style of [art movement]: impressionism, art deco, art nouveau
- [Medium] style: oil painting, watercolor, charcoal, pencil sketch
- [Era] aesthetic: 80s retro, vintage, futuristic, cyberpunk

## Aspect Ratio Guidelines

| Ratio | Use Cases |
|-------|-----------|
| 1:1 | Social media posts, profile pictures, app icons |
| 3:2 | Standard photography, prints |
| 4:3 | Presentations, traditional displays |
| 16:9 | Desktop wallpapers, YouTube thumbnails, widescreen |
| 9:16 | Mobile wallpapers, Instagram stories, TikTok |
| 21:9 | Ultrawide monitors, cinematic banners |

## Transparency Considerations

When generating for transparency:
- Explicitly request: "on a pure white background" or "transparent background"
- Avoid: white/light colored subjects (hard to extract)
- Best for: game sprites, icons, logos, stickers, cutout elements
- Use difference matting workflow for best results

# Public Assets

This directory serves static assets for the React application.

## Cinematic Background Assets

The public landing page (`/`) expects the following assets to be present in this directory to render the full cinematic experience. Since this is an MVP, these files should be dropped in manually.

### `background.mp4`
The primary background video for the landing page.
- **Expected Format:** `.mp4`
- **Recommended Resolution:** 1920x1080 (1080p) or higher.
- **Recommended Duration:** Approximately 10–20 seconds.
- **Looping:** A seamless loop is highly preferred to avoid jarring cuts.
- **Audio:** Muted / No audio track (the application strips audio via `muted` attribute).
- **Encoding:** H.264 compatible encoding for broad browser support.
- **Visuals:** Should depict abstract, cinematic IPsec/network traffic (e.g., cool blue V-shaped streams, volumetric clouds, forward motion) without any text, logos, or purple/magenta colors.

### `poster.jpg`
The fallback image shown while the video loads or if reduced-motion preferences pause the video.
- **Recommended Resolution:** 1920x1080.
- **Content:** A high-quality, representative first frame (or an iconic frame) of `background.mp4`.
- **Composition:** Must match the exact framing of the video so transitions are seamless.

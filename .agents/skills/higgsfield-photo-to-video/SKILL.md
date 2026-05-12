---
version: 1.0.0
name: higgsfield-photo-to-video
description: |
  Convert one photo or an entire folder of photos into cinematic videos using
  the Higgsfield CLI (Seedance 2.0 model). Interviews the user with targeted
  questions to build a detailed, client-specific prompt before generating —
  no hardcoded prompts. Use this skill whenever the user says anything like:
  "make a video from this photo", "convert images to video", "generate a video
  from a photo", "photo to video", "animate this image", "turn these photos
  into videos", "create a cinematic video from my photos", "batch video from
  folder", or any variation of wanting to go from still image(s) to video.
  Always trigger this skill before attempting to run higgsfield generate
  commands manually for image-to-video tasks.
---

# Higgsfield Photo → Video

## What this skill does
Turns one image or a whole folder of images into cinematic videos. Before
generating anything, it interviews the user to understand the client, the
scene, and the intended effect — then builds a rich prompt and confirms it
before submitting.

---

## Step 1 — Get the input

Ask the user:
> "What's the path to your photo or folder of photos?"

If they give a folder, list the images inside so they can confirm which ones
to process. Supported formats: `.jpg`, `.jpeg`, `.png`, `.HEIC`, `.heic`.

Also ask where to save the videos, or default to a folder named
`[input_folder_name]_Videos` next to the source folder.

---

## Step 2 — Interview the user to build the prompt

Ask these questions conversationally — you don't need to ask them one by one
as separate messages. Group related ones together to keep it natural. The goal
is enough detail to write a prompt that a cinematographer would understand.

1. **The scene** — What's in the photo? (e.g. luxury home exterior, product,
   restaurant, landscape, etc.)

2. **The transformation** — What should change or move during the video?
   Examples: lighting shifts (day to night, lights turning on), weather
   (clear to misty), seasons, camera movement (slow zoom, pan, reveal),
   time-lapse, fire/water effects, etc.

3. **Starting state** — What does the very first frame look like? Be specific.
   (e.g. "pitch black, no lights on", "golden hour, sun just touching the
   horizon", "product floating in white space")

4. **Ending state** — What does the last frame look like?
   (e.g. "fully lit exterior, warm glowing windows", "product spinning with
   logo lockup", "storefront at peak dinner hour")

5. **Mood and tone** — How should it feel? (e.g. cinematic and dramatic,
   warm and inviting, clean and minimal, high-energy, serene and slow)

6. **Client/brand details** — Anything specific to emphasize? Architecture
   style, brand colors, textures, key features to highlight, things to avoid?

7. **Audio** — Should the video include generated ambient sound? (yes / no)

---

## Step 3 — Build and confirm the prompt

Using the answers, write a detailed cinematic prompt. A good prompt:
- Describes the **starting frame** specifically
- Describes the **transformation** as a sequence of events
- Describes the **ending frame** specifically
- Includes **mood, pacing, and tone** language
- References any **brand or scene specifics** the client cares about

Show the prompt to the user and ask: *"Does this look right, or anything
you'd like to adjust before I start generating?"*

Only proceed once they confirm.

---

## Step 4 — Generate the videos

Always set PATH first:
```bash
export PATH="$HOME/.npm-global/bin:$PATH"
```

Process images **one at a time** — the account limit is 8 concurrent jobs,
but processing sequentially avoids rate limit errors and makes it easy to
track progress.

### For each image:

**a) Convert HEIC to JPG if needed** (macOS only):
```bash
sips -s format jpeg "input.HEIC" --out "/tmp/converted.jpg"
```

**b) Submit the job:**
```bash
higgsfield generate create seedance_2_0 \
  --prompt "YOUR PROMPT HERE" \
  --start-image "/path/to/image.jpg" \
  --json 2>&1
```
This returns `["job-id-here"]` — an array. Extract the first element.

**c) Wait for completion:**
```bash
higgsfield generate wait "job-id-here" \
  --json \
  --timeout 20m \
  --interval 10s 2>&1
```
This returns a JSON object. The video URL is at `result_url`.

**d) Download the video:**
```bash
curl -sL "https://..." -o "/output/folder/ImageName.mp4"
```

Tell the user after each save: `✓ ImageName.mp4 saved (N of TOTAL)`

### Error handling:
- **HTTP 500 or Internal Server Error on submit**: wait 15 seconds and retry
  once. If it fails again, log it and move to the next image — come back at
  the end.
- **rate_limit_reached error**: wait 30 seconds before retrying.
- **No `result_url` in the wait response**: check `status` field. If
  `failed`, log the error and skip. If still `processing`, the timeout was
  hit — rerun `generate wait` with a fresh `--timeout`.
- **Sensitive content rejection**: the image was flagged by Higgsfield's
  content policy. Log it and skip — do not retry the same image.

---

## Step 5 — Final summary

When all images are done, report:
- How many videos were successfully saved and where
- Any that were skipped and why (error, content flag, etc.)
- Offer to retry any failures if the user wants

---

## Key technical facts

| Thing | Detail |
|---|---|
| Model | `seedance_2_0` |
| CLI path | `~/.npm-global/bin/higgsfield` |
| Job submit output | JSON array: `["job-id"]` |
| Job wait output | JSON object with `result_url` key |
| Wait flags | `--timeout` and `--interval` (NOT `--wait-timeout`) |
| HEIC conversion | `sips -s format jpeg` (built into macOS) |
| Concurrent limit | 8 jobs max — process one at a time to stay safe |

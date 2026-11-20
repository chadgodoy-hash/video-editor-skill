---
name: video-editor
description: Use when the user wants to edit a video — first cutting out "umm / ahh" fillers, then a talking-head video (camera MP4) by adding branded motion graphics, main-point captions, small full subtitles, reference images of things they name (characters, tools, products, logos), full-screen scenes for numbered items, animated illustrations for spoken lists, their own proof photos/clips, camera zoom moves, upbeat sound effects and a subtle background-music bed with HyperFrames, then render the final MP4; or a screen-recording tutorial (OBS, software walkthrough) via Screen-Tutorial Mode — bigger glowing cursor, quiet music, no SFX. Triggers on "edit this video", "tutorial video", "remove the umms / ahhs / fillers", "screen recording", "add motion graphics / hyperframes / overlays / captions / subtitles / reference images to my video", or a video-editing project folder.
argument-hint: [optional: path to the video file or its folder]
---

## What This Skill Does

Takes a raw talking-head clip and produces a finished, on-brand MP4:

1. Word-level transcript (local Whisper — handles mixed-language speech like Taglish)
2. Overlay plan synced to what the creator says (checkpoint: the creator approves)
3. HyperFrames composition: one calm intro graphic (real brand logo when he names a tool), lower third, chapter tags, progress bar, **full-screen scenes for numbered items** (creator hidden), **animated illustrations for every spoken list** (no text lists), full-screen kinetic text for big framing lines, the creator's own proof photos / reaction clips, main-point captions, small full subtitles, constant camera zoom in/out, end card
4. Upbeat sound effects (your SFX library, banned clips skipped) and a subtle, full-sounding music bed ~24 dB under the voice
5. Preview in Studio (checkpoint: the creator reviews) → render → verify

The only cutting this skill does is **filler removal** ("umm / ahh / ehh" + their hesitation pause — see "Filler removal" below, on by default). Otherwise the footage plays unchanged underneath: this is graphics packaging — if the clip needs retakes or whole sections removed, say so and suggest a rough cut first (CapCut/Premiere).

---

## Reference Files

- `brand.md` — colors, fonts, tagline, logo rules. Load at the start of every run.
- `example-composition.html` — the latest approved composition ("7 Ways How Virtual Assistants Earn Using HighLevel", 13:41, Final v2, 2026-11-06): HighLevel-logo hub intro, kinetic full-screen text, proof-photo shots, reaction clip, 7 full-screen path scenes, illustrated list stages, 3 sketch boards, 16 B-roll beats. Reuse its CSS/helpers/patterns; never its timings or copy. The previous one (Hard Lessons, 2026-10-18) is in `examples/hard-lessons-composition.html`.
- **`scripts/scenes.py` — motion-graphic scene library (2026-11-06).** Import it from the per-video generator (`sys.path` to this folder, `import scenes as SC`):
  - `SC.stage(H, J, SFX, id, a, b, label, [(key, caption, t, extra)…], tail_html=, tail_js=)` — right-side card whose **animated illustration swaps on each spoken list item** (replaces text lists).
  - `SC.pscene(H, J, SFX, n, a, b, title_html, sub, key, stamp=None)` — **full-screen numbered-item scene** (creator hidden): navy gradient + drifting dot grid + ghost number, "0N / 07", title (`<em>` = gold), subtitle, big experience meter, and an illustration on the right.
  - `SC.kinetic(...)` — full-screen kinetic text over the background (edit its words/times per video). `SC.hub(...)` — brand-logo hub with connected feature tiles on a navy split-screen backdrop (The creator slides left). `SC.confused(...)` — full-frame reaction clip with wipe in/out, title chip and floating "?".
  - Illustration keys for `ill()` (440×320 SVG + GSAP, each with its own motion): `contacts`, `mail` (paper plane), `calendar`, `booking`, `traits` (shield/folders/gear), `bizinfo`, `branding`, `socialacc`, `platforms`, `apps` (plug into socket), `writeposts`, `schedule`, `create`, `leads` (magnet), `followup` (phone chat), `learnai`, `techva`, `gears`, `hlplat` (HighLevel logo) and path-scene art `onboard`, `socialphone`, `workflow`, `clients`, `coins`, `saas`. Add new keys the same way for new topics.
- `scripts/build_7ways_example.py` — the generator behind the example (chapters, captions, camera, panels, stages, path scenes, B-roll, shots, boards, SFX with dedupe, overlap report). **Preferred starting point for new videos**: copy it next to the video, edit the data, run `python3 build.py hf-project/index.html cues.json`. It reads CSS/helpers from `templates/lesson-video-template.html` and `broll-cutaway.html`.
- **Your own settings:** `brand.md` (colors, fonts, name, site, tagline) and the folder paths below. Fill these in once before the first edit.
- `templates/lesson-video-template.html` + `scripts/build_composition.py` — the older template/generator pair (Hard Lessons). Still the source of the shared CSS + helpers.
- `assets/logos/` — create it and save official brand logos here as you source them (see Phase 4b). Never redraw or approximate a logo.
- `assets/fonts/` — Poppins + Montserrat woff2. Copy into every project.
- `assets/sfx/` — ready, leveled clips: generated `pop`, `tick`, `ding`, `impact`, plus `pencil`/`pencil-rev`/`pencil-erase` (real CC0 recordings for sketch boards). **Add your own whoosh pack** as `whoosh-1..7.wav` (leveled with `scripts/sfx_kit.py`) — the rest of this skill refers to those names.
- `reference-card.html` — copy-ready CSS/HTML/JS for a brief pop-in image of something the creator names (see Phase 4b).
- `broll.md` — **B-roll research playbook**: which lines get B-roll (names, things, actions, settings, evidence, examples, stories), density target, 3-candidate research recipe, quality bar, library. Load at Phase 2.
- `broll-cutaway.html` — copy-ready full-frame cutaway (Ken Burns drift) v2: `brollCut()` (slide / punch / split enters, push / pull / pan moves) + `brollShot()` (fact callout, auto-capped camera push, highlighter). Tested with `hyperframes check` (0 errors) and snapshots, 2026-10-19 — incl. a full 83 s test on real footage (5 cutaways, 2 browser captures with fact callouts).
- B-roll library: a `broll-library/` folder next to your video projects (`catalog.json`) — every image used in a final video, tagged, for reuse and to avoid repeats.
- `scripts/key_moments.py` — print word timings from the transcript.
- `scripts/build_subtitles.py` — build the small-subtitle cue list (`SUB_CUES`) from the transcript, apply a fixes file, flag squashed timings.
- `scripts/sfx_kit.py` — split + level a pack whose sounds are separated by silence.
- `scripts/find_fillers.py` + `scripts/ctc_align.py` + `scripts/cut_segments.py` — filler removal (see "Filler removal"). find/align run in the `~/.venvs/align` venv.
- `scripts/split_compilation.py` — first-pass boundary finder for back-to-back compilations (silence + spectral change). It over/under-splits; always confirm with spectrograms (see Phase 6).
- **Folders (set these once):** `SFX_LIB` = your leveled SFX library (env var used by the generators, default `~/sfx-library`), a background-music folder, and the B-roll library above.
- **SFX library:** your own leveled clips (-18 LUFS, 48 kHz) in `SFX_LIB` with a `catalog.json` (file, label, category, duration, `banned`) and an audition `index.html` — build it with `scripts/sfx_kit.py` / `scripts/split_compilation.py` (Phase 6). Prefer clips the creator has confirmed by ear.
  - **Mood: upbeat and friendly only.** the creator: "don't put creepy sound effects, it feels lonely" (2026-10-18). No eerie or melancholic sounds — no sustained/drawn-out tones, falling or rising tonal sweeps, long ringing bell/chime tails, heartbeats, or vocal blips. Use short, bright, playful sounds: pops, clicks, bloops, quick dings, whooshes, clean punchy hits, comedic boings/meme sounds for jokes.
  - **Banned — never use:** any clip with `"banned": true` in `catalog.json` (mark buzzing, creepy or lonely clips there as the creator rejects them). Also avoid sustained buzzy/pulsing textures in general: before picking a hit/impact, render its spectrogram — a wall of evenly spaced vertical stripes across the whole clip = buzz. Never stack the same long hit back-to-back (overlaps turn into a drone).

Also load the HyperFrames skills (`/hyperframes-core` before writing HTML; `/hyperframes-animation`, `/hyperframes-keyframes` for motion; `/hyperframes-audio` for mix questions). They're installed in `~/.claude/skills/`.

---

## Standing Rules — check before EVERY render (new edits AND re-renders)

These came from real feedback on finished edits. Change them to match your own taste — but a render that breaks one of them is a failed render.

1. **Calm intro — no title card.** Brand swipe + ONE graphic tied to what he says (one at a time). Never a title card in the opening — the YouTube title does that job. (2026-10-18, repeated 2026-10-19: "you're putting the title on the first part which I don't really like")
2. **Upbeat SFX only.** No buzz, no creepy/lonely sounds: tones, rising/falling sweeps, long bell/chime tails, heartbeat, vocal blips — every `"banned": true` clip in the SFX `catalog.json`. `grep` the composition for banned files before rendering.
3. **Subtle music bed always** (Phase 6b) — ≈ **24 dB under the voice** (bed ≈ -38.5 LUFS). 16–18 dB under was "too loud" (2026-10-19). Subtle but **not dry** — skip sparse track intros, keep low end, light reverb (2026-11-06). A render without `assets/music/bed.wav` is not done.
4. **Constant camera zoom in/out**, no repeated graphic treatments from his previous videos.
4b. **Sketch boards (pencil writing)** — 1–3 per video on the ideas that most need a picture (concept, framework, steps, comparison): torn paper slides in, the creator shifts right, invisible pen writes + draws with pencil sounds (Phase 4c). An edit with zero sketch boards needs a reason.
0. **Fillers removed** ("umm / ahh / ehh") before anything is timed — see "Filler removal". The creator asked for this on 2026-10-22.
5. **B-roll** per `broll.md`; the creator's call on each cutaway is final — if he rejects one, remove it, don't swap it silently.
6. **Show it, don't list it**. Whenever he enumerates things, each item gets an **animated illustration of what it is**, swapping on the spoken word (`SC.stage`) — "Update contacts = a contact list, email campaigns = a paper plane, basic tasks = a calendar". No bullet/text lists on screen except the final recap.
7. **Numbered items = full-screen scene without the creator** (`SC.pscene`): "01 / 07", title + subtitle block, experience/progress meter and a motion graphic about that item, then cut back to him. Big framing lines ("7 HighLevel income streams") get the same treatment as full-screen kinetic text (`SC.kinetic`), back to the creator on the next sentence. "People focus on the title or subtitle block."
8. **Real brand logos.** When he names a tool in the intro, the intro graphic uses the tool's official logo (e.g. HighLevel logo in the middle, CRM / Email / SMS / Calendar / Funnels / Social tiles connected by lines — `SC.hub`). Never redraw or approximate a logo.
9. **His own proof on screen.** Before building, check the video folder for photos/clips he dropped in (named by what they are, e.g. "Last september.jpg", "GHL proof.jpg", "Confused.MP4") and ask what's coming. Photos → full-frame `brollShot` with a title as the fact line (`hl: false` for plain photos); reaction clips → `SC.confused`-style full-frame clip, muted under his voice.

**Re-editing an older project** (adding B-roll, fixing a line, any new render of an edit made before these rules): first audit the existing `index.html` against rules 1–9 and fix what fails — remove an intro title card, replace banned SFX, add the music bed, plan 1–3 sketch boards if there are none — then do the requested change. Mention the fixes in the report. (2026-10-19: B-roll was added to the Oct 18 "Worth it" edit without this audit; Final v2 shipped with a title-card intro, banned SFX and no music — the creator caught all three.)

## Filler removal ("umm / ahh") — every video, before timing anything

The creator (2026-10-22, WFH tutorial): "remove the part where there uhmmss, ahmmm". Do it on the 30 fps / voice-fixed footage, **before** cursor tracking (tutorials) or the timing transcript (talking-head), because cuts shift every timestamp after them.

Why three scripts: plain Whisper drops fillers; a disfluency prompt brings them back but its word times drift ±0.5 s and it invents some; the creator also glues fillers onto the previous word ("dito-umm") so energy/pitch edges don't work. Proven recipe (WFH video: 12 fillers, 15.2 s removed, 12/12 joins clean):

1. **Find + plan:** `~/.venvs/align/bin/python -I scripts/find_fillers.py <footage> <video folder>/cuts.json` (~3 min per 7 min of video).
   - Transcribes word by word with a filler prompt (`--carry-initial-prompt -ml 1 -sow --dtw large.v3.turbo`); pass `--words <json>` to reuse one.
   - Candidates = filler tokens + long pauses with sound in them.
   - Each candidate is re-transcribed in two short windows; it's kept only if a filler is heard (drops breaths, mouse clicks, invented "uh"s).
   - `ctc_align.py` (wav2vec2 CTC forced alignment, ~20 ms) pins the real words on each side. The cut runs from the word before to the word after, guarding each word by 40 ms; the pause kept (`--keep`, default 0.25 s) is only silent frames, so no piece of the "ahh" survives.
   - Prints every cut (`before [um] after | heard text`) plus the skipped candidates and why.
2. **Read the list.** Tagalog "ah"/"eh" can be real words. **Sentence-final "eh" is a particle, not a filler** ("madali kasi eh", "kaya nga tracking eh") — always remove those cuts; the creator's tone depends on them. Sentence-start "Ah, ..." and mid-phrase "mga, ah, trabaho" are fillers. Delete any cut you doubt from `cuts.json` and note why in its `review`.
3. **Cut:** `python3 -I scripts/cut_segments.py <footage> cuts.json hf-project/footage_cut.mp4 [--track cursor_track.uncut.json cursor_track.json]` — trim/concat with 10 ms audio fades at every join; `--track` remaps an existing cursor track instead of re-tracking (~6 min saved).
4. **Verify every join:** re-transcribe ±1.6 s (then ±2.5 s / `-l tl` for unclear ones) around each new join time (old cut start minus the time removed before it) — the filler must be gone and the words on both sides intact. Whisper on a 3 s clip sometimes returns just "So," — that's a short-window glitch; widen before worrying.
4b. **Second pass:** run find_fillers.py again on `footage_cut.mp4` — Whisper misses some on the first pass (WHERE video: 25 → +2). For one it still won't plan (e.g. "um" glued to the next word), align the window with `ctc_align.py`, print 10 ms dB values, and cut from the pause to the dip right before the next word's onset. Cut again with `--track` if a track exists.
5. Use `footage_cut.mp4` (or the second-pass file) as the video for everything after (music bed length = its duration). Screen recordings show a small jump in the picture at each join; that's normal for tutorials.

Setup (done 2026-10-22, verify don't redo): `python3 -m venv --system-site-packages ~/.venvs/align && ~/.venvs/align/bin/pip install transformers` (reuses the system torch 2.12). Model `facebook/wav2vec2-base-960h` is cached in `~/.cache/huggingface`.

## Screen-Tutorial Mode (screen recordings — approved recipe: GoHighLevel tutorial Final v2, 2026-10-20)

Use this whenever the footage is a **screen recording** (OBS, software / website walkthrough, e.g. GoHighLevel) instead of the creator on camera. The creator wants **minimal edits**: a bigger glowing pointer so viewers can follow, a very quiet music bed, no SFX. Skip the Standing Rules' talking-head items (intro graphic, sketch boards, B-roll, lesson slams, captions, auto-zooms) unless he asks. The creator on Final v2: "Great job!".

No overlay-plan checkpoint needed — go straight from transcript to render, then show the creator the result.

1. **Re-encode** to 30 fps 8-bit H.264 (OBS records 60 fps — 30 halves render time): `-vf fps=30 … -g 30` → `hf-project/footage30.mp4`.
2. **Fix the voice level first.** OBS mic was very quiet (-30.5 LUFS GHL, -28 WFH). Two-pass `loudnorm=I=-16:TP=-1.5:LRA=11` with `highpass=f=80,afftdn=nr=10:nf=-45` before it; mux back with `-c:v copy`. (Pass 1 needs `-hide_banner -nostats` not `-v error`, or the loudnorm JSON is swallowed.)
2b. **Remove fillers** ("Filler removal" above) → `hf-project/footage_cut.mp4`; track and build on that file. OBS often has a false-start clip just before the real one (same intro, < 30 s) — skip it and say so.
3. **Track the cursor (dense):** `TRACK_FPS=15 python3 -I scripts/track_cursor_dense.py footage30.mp4 <video folder>/cursor_track.json` (~6 min per 21 min). Confirms the cursor on every frame with masked NCC (only the cursor's own pixels count) against `assets/cursor/macos_arrow.npy` (tip +3,+3) and `macos_hand.npy` (pointing hand over links, fingertip +5,+2) — works on white pages, dark sidebars and hover rows. The webcam bubble is auto-masked. The I-beam is not tracked (it matches letters like "I"/"l"); the overlay fades there and the creator's normal cursor shows. GHL: cursor found in 62% of frames.
   - If the creator's cursor looks different in a new recording (new macOS theme / size), cut a new template from a still frame (print the region as ASCII to find it) and save it next to the others.
4. **Spot-check** ~12 random samples before building: crop 160×160 around each point from the footage with a red dot at the tracked hotspot (ffmpeg `drawbox`; this ffmpeg has no `drawtext`). Every dot must sit on the arrow tip / fingertip. GHL: 12/12 and 8/8 after render.
5. **Build:** `python3 -I scripts/build_cursor_overlay.py <track.json> footage30.mp4 <duration> hf-project/index.html --music assets/music/bed.wav --music-vol 0.5`, then `hyperframes check` (expect 0 errors / 0 warnings). It draws a 1.9× macOS arrow or hand exactly over the real one (hotspot on hotspot, so the real cursor hides underneath) plus a soft yellow glow centred on the pointer body; holds while the cursor rests, interpolates the 15 fps samples, fades in/out over 0.2 s where the cursor is lost. Seek-safe: one proxy tween whose `onUpdate` binary-searches the track.
6. **Music:** bed per Phase 6b (chained to cover the length) at `data-volume` **0.5** (≈ 28 dB under the voice — 0.8 / ≈ 24 dB was "a little bit" too loud for a tutorial). **No SFX.** A calm lofi/chill track works well for tutorials.
7. **Render fast and resumable** (anything > 5 min), in the background. The creator wants the Mac kept awake for the whole edit (2026-10-22): start `caffeinate -dims -t 14400` in the background at the beginning of every edit, and wrap tracking/render in `caffeinate` too:
   `HF_SEGMENTED_CAPTURE=true caffeinate -i -s npx --yes hyperframes@<ver> render -w 6 --fps 30 --quality delivery --resume -o "<out>.mp4" > <scratchpad>/render.log 2>&1`. Default workers crawled at ~190 frames/min and died when the Mac slept; this does a 21-min video in ~12.5 min on the 10-core Mac. Progress is in the log (`Streaming frame N/total (segment k/13)`) — never pipe the render through `grep | head` (hides progress). Test on a 60 s slice first (draft quality, ~35 s) when anything in the recipe changed.
8. **Final loudness:** measure with `ebur128=peak=true`. The mix lands below -16 (−17 to −19.6 LUFS). Two-pass `loudnorm=I=-16:TP=-1.5:LRA=11:…:linear=true` on the audio with `-c:v copy` (in zsh write `${P}:linear` — `$P:l` is a zsh modifier that eats the colon), then if the peak is above −1 dBFS: `aresample=192000,alimiter=limit=0.84:level=false:attack=1:release=50,aresample=48000`. Target: I −16.0 LUFS, peak ≤ −1 dBFS.
9. **Privacy check before handing over:** screen recordings show emails, phone numbers and client names (users tables, form fields). List them with timestamps; blur only if the creator asks.
10. **Hand over:** name it `<title> - Final.mp4` (or `Final vN (<what changed>)` on a re-edit, keeping the old one) and `open` it.

### Optional: cursor-tracked zooms (only if the creator asks for zooms)

Rejected as the default ("not on point", GHL Final v1) but kept as a tool: `python3 -I scripts/track_cursor.py <video> assets/cursor/macos_arrow.npy track.json` → `python3 -I scripts/plan_zooms.py track.json zooms.json` (cursor resting ≥ 2.2 s → 1.6× zoom where it settled; pans for close targets; zooms out at page changes / after 14 s). Camera on `#cam` with `transform-origin: 0 0`, tween `x, y, scale` together (`x = 960 − s·cx`, `y = 540 − s·cy`, clamped), 0.7 s `power2.inOut`. Verify every target by cropping the would-be viewport. The baked-in webcam bubble gets cropped while zoomed. v1 composition: `Go HighLevel Tutorial for Beginners/index.v1-zooms-2026-10-20.html`.

## Steps

### Phase 0: Preflight

**Keep the Mac awake** for the whole edit (The creator, 2026-10-22): first thing, run `caffeinate -dims -t 14400` with `run_in_background`. Stop it when the edit is handed over.

Tools (all installed 2026-10-18 — verify, don't reinstall):
- Homebrew at `/opt/homebrew/bin/brew`. It is **not on your PATH** in non-login shells — always `export PATH=/opt/homebrew/bin:$PATH` in Bash calls.
- `ffmpeg`, `ffprobe`, `whisper-cli` (brew `whisper-cpp`)
- Whisper model: `~/whisper-models/ggml-large-v3-turbo-q5_0.bin`
- HyperFrames CLI: `npx --yes hyperframes@<pinned version>` (Node 22 at `~/.local/bin`)

Find the video: `$ARGUMENTS` path, or the MP4/MOV in the current folder. If more than one, ask which.

If the folder already has an `hf-project/` (older edit): run the **Standing Rules audit** above first — `grep` `hf-project/index.html` for `id="title"` and every banned clip name from the SFX `catalog.json`, and check for `music/bed.wav`. Back up `index.html` to the video folder (NOT inside `hf-project/` — a second root HTML there is a lint error: `multiple_root_compositions`).

### Phase 1: Probe, Transcribe, Look

Run in parallel:
1. `ffprobe` — duration, resolution, fps (DJI = 29.97 → `30000/1001`), codec.
2. Extract audio and transcribe:
   ```
   ffmpeg -v error -y -i <video> -vn -ac 1 -ar 16000 <scratchpad>/audio.wav
   whisper-cli -m ~/whisper-models/ggml-large-v3-turbo-q5_0.bin -f <scratchpad>/audio.wav -l en -osrt -ojf -of transcript
   ```
   Writes `transcript.srt` + `transcript.json` into the video folder. Use `-l en` even for Taglish — it transcribes Tagalog words phonetically, which is fine.
3. Grab 2–3 stills (`ffmpeg -ss <t> -frames:v 1 -vf scale=960:-1`) and Read them. Note where the creator's face sits and which side of the frame is clean. In the default setup (desk, window left, wall right) his face spans x≈860–1300 of 1920 → **panels go right (left edge ≥ 1400px), captions bottom-center, lower third bottom-left.**

**Filler removal** runs here, on the re-encoded footage ("Filler removal" above): cut first, then make `transcript.json` from `footage_cut.mp4` so every overlay time matches the cut video, and use `footage_cut.mp4` as the project video in Phase 3.

Flag likely mistranscriptions to the creator (one line each).


### Phase 2: Overlay Plan — CHECKPOINT

Read the transcript and pick the main points. Use `scripts/key_moments.py transcript.json <ranges>` for exact word times.

Present a table: `Time | What the creator says | Overlay | Camera`.

**The creator's taste rules (2026-10-18):**
- **Keep the intro calm — one graphic at a time.** Never stack a title card and a stat panel together ("the introduction is too busy"). Default intro = brand swipe + ONE graphic tied to what he's saying. Skip the title card when the opening already has a graphic; the YouTube title does that job.
- **Don't repeat a visual treatment from his previous videos.** Check `example-composition.html` and recent projects before picking a graphic (e.g. the "12 YEARS" ring was used in the VA Bootcamp intro → the Hard Lessons intro used a career staircase instead). Vary stat/list designs video to video.

Standard beats:
- 0:00 brand swipe + one intro graphic (title card only if nothing else is on screen). If the topic is a tool/platform, that graphic is the **official logo hub** (`SC.hub`, rule 8).
- "In this video, N things…" framing line → **full-screen kinetic text** (`SC.kinetic`), creator hidden for that sentence only.
- His story beats ("last September…", "I passed…", "now I'm working with…", "at first I was confused") → his own photos/clips from the video folder, full-frame with a title (rule 9). Ask for them in the plan if they're missing.
- Name intro → lower third "<Your Name> · <role line> · <your site>" (from `brand.md`) + camera push-in
- Numbers/stats → an animated stat — pick a fresh form each video (ring + count-up, career staircase with a climbing marker, timeline, bar race…)
- **Numbered-lesson / listicle videos** ("7 lessons", "5 tips", "7 ways") → a **full-screen item scene** per item (`SC.pscene`, rule 7: creator hidden 5.5–7 s, big "0N / 07", title + subtitle, meter, an illustration about that item, boom-swoosh in + impact on the number), the chapter tag shows the current item ("PATH 3 · SOCIAL MEDIA VA"), and a **recap panel** ticking off every item before the CTA. One visual metaphor per item (diagram, chat bubbles, stamps, illustrations on spoken words). The old right-side "lesson slam" card is replaced by this.
- Short emphatic phrases ("this is a hard rule") → a rotated **stamp** with a clean impact.
- **Explaining a concept / framework / steps / comparison** → a **sketch board** (Phase 4c): torn white paper slides in from the left, the creator shifts right, and an invisible pen writes the key words and draws shapes (circles, arrows, boxes, underlines, checks, speech bubbles) in sync with what he says. Use it 1–3 times per video for the ideas that most need a picture — it's the "whiteboard" moment, not a constant layer.
- Lists ("you'll learn X, Y, Z", "update contacts, send emails, set up tasks") → an **illustrated stage** (`SC.stage`, rule 6): one animated picture per item, swapping on each spoken word, caption under it. Items closer than ~0.7 s apart: nudge the later one to keep each picture on screen ≥ 0.7 s. In the plan table write the picture for each item ("contacts → contact list").
- Pain point / emotional line → camera punch-in + caption + a visual metaphor (e.g., roadmap Zero → Learn → Portfolio → Hired)
- Promises / benefits → badges with live icons
- Closing call to action → caption + visual (e.g., 7-day streak checking off)
- **B-roll (web images)** — follow `broll.md`. The creator wants **more B-roll, better researched** (2026-10-19). Scan the transcript sentence by sentence, not just proper nouns: names → reference card; things, actions, settings, stories → full-frame cutaway; evidence and examples → screenshot cutaway of the real source. Target one B-roll beat every 10–20 s of talking, never two within 4 s, never over the intro/hook/punchlines/CTA or a right-side panel/sketch board. List them in a separate plan table: `Time | Line | Type | B-roll idea | Style`. The creator may also flag B-roll himself ("put X at 1:20") — always include those. Check the B-roll library catalog first for reusable images.
- Outro → end card: circle wipe to the brand background, thank-you line, tagline slams, wordmark, site (+3 s after footage ends) — all from `brand.md`
- Throughout → chapter tags (top-left) + bottom progress bar
- **Throughout → camera zoom in / zoom out, as often as it fits** (The creator's preference, 2026-10-18). Don't save punch-ins for captions only — plan camera moves across the whole video. List them in the plan table as a `Camera` column. See "Camera moves" in Phase 4.

**Two caption layers** (The creator's preference):
- **Main-point captions** — big navy pills, only on key lines, keyword underlined on the spoken word.
- **Small subtitles** — full transcript, Montserrat 600 30px, navy pill at `bottom: 34px`, ≤ 44 chars per cue. Built as ONE clip whose text is set from a `SUB_CUES` array by an `onUpdate` proxy tween (seek-safe; see `example-composition.html`). Hidden during main-point caption windows (`SUB_HIDE`) so text never stacks. Lower third sits at `bottom: 120px` to clear them.
- Build cues with the script:
  ```
  python3 scripts/build_subtitles.py transcript.json --fixes <scratchpad>/fixes.json --end <end-card start> > <scratchpad>/cues.json
  ```
  `fixes.json` = `{"wrong": "right"}` for mistranscriptions (e.g. `"Kraming": "Maraming"`, `"ginagawa niya": "ginagawa nyo"`). The script prints every cue to stderr and flags `!! squashed timing` — merge/re-time those by hand (e.g. merge a 0.3 s "Hello guys!" into the next cue; split a squashed line across the previous cue's span). Read the full cue list before using it.
- In the plan, list every transcript fix as "said → shown" and mark guesses so the creator can confirm them (a wrong word on screen is worse than none).

**Sound in the plan:** a short `Music` line (which tracks from the music folder, Phase 6b) and any SFX needed for beats the local library can't cover.

Wait for the creator to approve or edit the plan. Ask for brand/logo changes only if `brand.md` doesn't cover it.

### Phase 3: Scaffold

```
npx --yes hyperframes@<ver> init hf-project --example blank --video <video> --skip-transcribe --non-interactive --resolution landscape
```
Then, from `hf-project/`:
1. **Re-encode the footage to 8-bit H.264** (overwrite the copy init made). Init converts DJI HEVC to **10-bit "High 10" H.264**, which browsers can't decode smoothly — the preview drifts out of lip-sync. Fix:
   ```
   ffmpeg -v error -y -i <original video> -map 0:v:0 -map 0:a:0 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -profile:v high -g 30 -keyint_min 30 -sc_threshold 0 -c:a aac -b:a 192k -movflags +faststart -map_metadata -1 <scratchpad>/fixed.mp4 && mv <scratchpad>/fixed.mp4 <project video name>.mp4
   ```
   Verify with ffprobe: `profile=High`, `pix_fmt=yuv420p`.
2. Copy `assets/fonts/*` and `assets/sfx/*` from this skill into `hf-project/assets/`.

### Phase 4: Build the Composition

Write `hf-project/index.html` starting from `example-composition.html`'s structure. Rules learned the hard way:
- Wrap the `<video>` in an **untimed** `<div id="cam">` (transform-origin at the creator's face, e.g. `1060px 430px`) for punch-ins. Never put `data-start` on that wrapper (lint error `video_nested_in_timed_element`).
- Animate inner nodes only — never tween a `.clip` element's opacity/visibility.
- No CSS `transform` on anything GSAP transforms; set start states inside `fromTo`.
- Later tweens re-owning a property: `immediateRender: false`.
- SVG line draws: `pathLength="1" stroke-dasharray="1"` + tween `strokeDashoffset` 1 → 0 (no measuring).
- Rotate SVG groups with `svgOrigin: "cx cy"`.
- Generated SVG (gear teeth, tick rings) is built at load time with deterministic loops — no `Math.random`, no timers.
- Root `data-duration` = footage length + end card (~3 s).
- Panels 450–460px wide, `right: 56px`. Lower third and main-point captions never on screen at the same time.
- Subtitles: one `#subs` clip spanning 0 → end-card start, a `.sub` span, and a single proxy tween over the whole duration whose `onUpdate` picks the cue for `proxy.t` (skip if inside a `SUB_HIDE` window) and only touches the DOM when the cue changes. Copy this block from `example-composition.html`; paste the script's JSON as `SUB_CUES` and the main-point caption windows as `SUB_HIDE`.
- **Camera moves — maximize zoom in / zoom out whenever possible.** All moves go on `#cam` (overlays sit outside it and stay still). Mix these four so it never feels repetitive:
  - **Punch-in** (`punch(a, b, s, inDur, outDur)`, s 1.10–1.18) — every main-point caption, punchline, question, pain point. Use 1.18–1.25 for the strongest lines (emotional, "matetegi ka" moments).
  - **Snap zoom** — instant cut-in for a joke, a hard word or a list beat: `tl.set("#cam", { scale: 1.2 }, t)` then `tl.set("#cam", { scale: 1 }, t2)` 1–3 s later, or hold until the next move. Pair with a swish/hit SFX.
  - **Slow push / pull** — through plain explanation stretches: `tl.fromTo("#cam", { scale: 1 }, { scale: 1.07, duration: 6–10, ease: "sine.inOut", immediateRender: false }, t)`, then ease back or straight into the next move. Alternate push-in and pull-out (start at 1.07 → 1) so the frame breathes.
  - **Zoom out reset** — pull back to 1.0 when a right-side panel enters, so the panel isn't fighting a tight frame.
  - Coverage target: the camera should be moving or sitting zoomed in for most of the talking time. Plain 1.0 static stretches longer than ~10 s should be rare.
  - Never overlap two moves on `#cam` — each move starts after the previous one finishes (or re-owns scale with `immediateRender: false` from the current value).
  - Limits: max scale 1.25 (1080p source gets soft beyond that); keep `transform-origin` on the face; snapshot every zoom > 1.15 to check the top of the head and chin aren't cut and nothing important (hands holding props) leaves frame.
  - Implementation that worked (Hard Lessons, 34 punch/snap moves + auto-filled slow push/pull, 142 keyframes): one `CAM` array of `[time, scale, duration, ease]` (duration 0 = snap) played in order, each tween `fromTo` the previous scale with `immediateRender: false`. `build_composition.py` generates it from `punch()`/`snap()` calls, asserts no overlaps, and fills every gap ≥ 4 s with sine push/pull cycles peaking at 1.05–1.07.
- Bottom stack (1080p): progress bar 0–6px · subtitles at 34px · main-point captions at 70px (subtitles hidden then) · lower third at 120px · streak/extra rows ≥ 200px.
- Badge/headline text: check it fits on one line (`white-space: nowrap` + smaller font) — the 450px panel clips long text. Big prices ("$10–15 / hour") wrapped at 104px; 74px + nowrap fits.
- More gotchas (7 Ways, 2026-11-06):
  - Extracting `<style>`/`<script>` from the skill's HTML snippets: match `<style>\n` — the header comments contain the text "(inside <style>)", and a naive regex pulls the comment in → `unbalanced_style_tags` error.
  - Shifting `#cam` sideways (split screen) exposes a **black strip** at the far edge — always slide a navy backdrop panel in behind the graphic (`SC.hub` does this).
  - Never tween `letterSpacing` (lint error `gsap_non_transform_motion`) — use `scaleX`/opacity.
  - Rotating several SVG shapes (falling dominoes): give each its own `svgOrigin` at its own pivot — one shared origin flings them across the board.
  - De-duplicate SFX on `(time, clip)` before writing `<audio>` tags (two systems adding the same tick → `duplicate_media_discovery_risk`).
  - Two back-to-back full-frame shots: overlap them ~0.3 s on different tracks so the creator doesn't flash between them.
  - Muted B-roll video (reaction clip): its own `<video class="clip" muted>` (never inside a timed div); hide the hard cut with a quick bar wipe clip at in/out. Transcode phone clips to 8-bit H.264 with `-an -dn -map_metadata -1` (iPhone/DJI extra data streams).

**Studio rewrites `index.html`** (it stamps `data-hf-id` attributes) whenever the preview is open. Before overwriting the file, diff it against your last build with the `data-hf-id`s stripped, comparing `data-start` / `data-duration` / `data-volume` per element and the `<audio>` count. The creator does make changes there (2026-11-06: music volume 1 → 0.4365 and one SFX deleted) — **port every change into the generator** (data-volume, removed cue) before rebuilding, or the next build silently undoes his tweaks.

### Phase 4b: B-roll + Reference Visuals

**Research every approved B-roll slot with `broll.md` §2:** 2–3 specific searches per slot → 3 candidates → pick the one that passes the quality bar (matches the exact line, ≥ 1280px for cutaways, no watermark, landscape, not used in the last 2 videos) → save to `hf-project/assets/broll/` with a credit. Drop a slot after 3 failed searches and tell the creator which ones. **Evidence and example slots use your Chrome browser** (`broll.md` §2b): open the real page, read it to verify the claim and pull real numbers, then capture the exact element (`zoom` region, `scale: 1`, `save_to_disk: true`). Read-only browsing; crop or blur anything private. Build cutaways from `broll-cutaway.html` v2 (DOM right after `#cam`, track 12): photos with `brollCut()` — rotate enters (slide / punch / split) and moves (push / pull / pan); browser captures with `brollShot()` — fact callout, camera push into the key spot, highlighter. Holds: photos 3.5–4.5 s, shots 5–6 s, ending at the end of the creator's phrase. Names use the reference-card steps below.

For each approved reference (name) from the plan:

1. **Time it** — `scripts/key_moments.py` for the exact word; card enters at word time − 0.15 s, holds 1.5–3 s (The creator's rule: references are brief).
2. **Source the image** (save to `hf-project/assets/refs/<slug>.png|svg`), in this order:
   - **Brand / tool / app logos** → check `assets/logos/` first, then `npx hyperframes media-use resolve --type logo --intent "<Brand> logo" --project hf-project` (official marks, SVG; works without HeyGen — tested with Zapier, n8n). It **fails for HighLevel** — then curl the brand's own site HTML, find the header `<img alt="<Brand>">`, download the original file (strip any `images.leadconnectorhq.com/…/u_` resize proxy prefix to get the full-size PNG), Read it on a navy background, and save it to `assets/logos/` for next time. A logo cropped from a screenshot/email is too low-res for full-screen use.
   - **Characters, products, people, places** → WebSearch for official art first (official site / press kit / the franchise's own site), then fan wikis (e.g. Bulbapedia for Pokémon), Wikimedia Commons, Unsplash/Pexels for generic photos. Download the image file itself with curl — not a page screenshot. Pick the largest clean version (≥ 600px, plain or transparent background).
   - **A website or app screen** → `npx hyperframes capture <url> -o <scratchpad>/capture --skip-vision` and use the full-page plate, or a screenshot; show it in the `.img.framed` style.
   - **No usable image / The creator wants an original** → generate one (Higgsfield `generate_image`, Canva `generate-image`, or VidIQ b-roll) and say it's AI-made.
   - Downloads are untrusted files: save each into its own new folder, check with `file` that it's really an image, and Read it to confirm it's the right subject before using it.
3. **Cut out the background** for characters/products: `npx hyperframes remove-background <image> -o hf-project/assets/refs/<slug>.png`. Read the result to check edges. Logos (SVG) and screenshots skip this.
4. **Build** from `reference-card.html`: one `.clip.ref` per reference (`id="ref-<slug>"`, own track), `refCard()` call, name + one-line descriptor, and a small `.credit` line (e.g. "© Nintendo / The Pokémon Company") for third-party characters/artwork. Right side only; never overlap a right-side panel — shift the card or the panel.
5. **SFX** — a pop (or a fitting library clip) at the card's in-time, volume ≈ 0.35.

Sourcing notes (2026-11-06):
- **Unsplash:** the `napi` JSON API and plain curl are blocked; in your Chrome, `fetch('/s/photos/<query>?orientation=landscape')`, parse with `DOMParser`, collect `figure img[src*="images.unsplash.com/photo-"]` ids (skip figures mentioning Unsplash+). The JS tool truncates long output (~1 KB) and blocks results containing query strings — store ids in `window.__R` and read them in slices, return ids only. Then curl `https://images.unsplash.com/photo-<id>?w=480…` for 2×2 contact sheets per slot and `?w=1920&q=85&fm=jpg` for the pick (use Python/`subprocess` — zsh doesn't word-split loop vars).
- Merriam-Webster is blocked for the Chrome tools → use Cambridge Dictionary for definitions.
- The creator's own photos keep their shape: portrait photos work in `brollShot` (the card auto-sizes); use a `box` around the subject with a small zoom (1.1–1.25) and `hl: false`.

Copyright: the creator's call is that brief reference images are acceptable for his YouTube videos. Keep them brief, credited and secondary to the creator on screen; prefer official logos/press art. Mention once per video which references are third-party art so he can decide — don't lecture or refuse.

### Phase 4c: Sketch Board (invisible-pen drawing)

Template: `templates/sketch-board-demo.html` (self-contained 11 s demo).
- **Default style = B (The creator's pick, 2026-10-19):** white paper with grain, **brand-blue** headings + shapes (`.ink.hd`, `path.b` #2563eb), **navy** handwriting + doodles (`path.n` #0b2058), **blue** torn rim (`.edge` background var(--blue)). Not red/black (off-brand), not a navy chalkboard (looks like the regular panels — the paper contrast is what makes the drawing moment stand out). Production version lives in `templates/lesson-video-template.html` (4 boards in Hard Lessons, Final v4).
- **Picking moments:** use a board when the creator *explains how something works* — a contrast ("not this, but this"), cause → effect, a process/loop, a group/relationship, or a set of concrete things he lists (doodle each). Not for punchlines (captions + zoom do those). A board **replaces** the panel planned for that moment (never stacks); max one per lesson and ~3–4 per 10-minute video. Drop any main-point caption that falls inside a board window — write that keyword on the board instead.
- **Doodle library** in the template's `sk` object: line, rect, ellipse, arrowShaft/arrowHead, check, cross, loop (learn→apply ∞), figure (stick person), washer, star, shirt, cup. Add new doodles the same way: a list of points through `wobble()` with a fixed seed.
- **Layering:** `#subs, #progress { z-index: 20; }` so they stay above the paper; the chapter tag stays under it (the board heading replaces it). `sketchIn/sketchOut` also slide the small subtitles left by 385px so they sit on the paper, then back. Copy its "Sketch board" CSS, one `.clip.sketch` per board, and the "Sketch helpers" JS.
- **Look:** off-white paper (`--paper #f7f6f2`) with a fine grain (SVG `feTurbulence`, seeded), jagged torn right edge from `tornEdge()` (seeded polygon; a slightly wider `.edge` layer behind gives the fibrous rim + shadow). Paper ≈ 1150px wide.
- **Camera:** `sketchIn(id, t)` slides the sheet in from x −1220 while `#cam` shifts x +420 (The creator's face moves to ≈1220–1700, fully clear of the paper); `sketchOut(id, t)` reverses. x is separate from the camera-track `scale`, so zoom moves can keep running.
- **Ink:** handwriting font **Gochi Hand** (`assets/fonts/gochi-hand-latin-400-normal.woff2`; Caveat 500/700 as an alternate). Heading in red (`.ink.red`, #c8102e), body in near-black; `.ink.blue` (brand blue) for a branded variant. Sizes: heading 88–96px, body 60–72px, punchline 90–100px.
- **Writing:** `write(sel, t, cps)` wipes the text in left→right with `clip-path` at handwriting speed (≈12–18 chars/s). Start each line on the spoken word (`key_moments.py`).
- **Drawing:** every shape is a `<path>` whose `d` is generated at load by `sk.line / rect / ellipse / arrowShaft + arrowHead / check / bubble` (seeded wobble so it looks hand-drawn, deterministic for render), then `draw(sel, t, dur)` animates `strokeDashoffset` 1→0. Draw emphasis shapes right after the word they mark (circle "#1", underline the heading, arrow to the result, check at the end).
- **Layout:** left margin ≈110–150px, heading at top ≈120px, max ~6 lines; snapshot and nudge shape coordinates so circles/underlines hug the words (estimate from the snapshot: board px ≈ frame px × 3.2 on a 600-wide contact-sheet cell).
- **Rules:** no right-side panels or reference cards while a board is up (The creator occupies the right); main-point captions off during a board (the board *is* the emphasis — add the window to `SUB_HIDE` only if subtitles would cover drawings low on the page); hold ≥ 1 s after the last stroke before `sketchOut`.
- **Sound:** real pencil-on-paper recording (CC0, "pencil_write" by NachtmahrTV via OpenGameArt — `assets/sfx/credits/pencil-sounds-CC0.txt`): kit `pencil.wav` + `pencil-rev.wav` (reversed, for variety) and `pencil-erase.wav`. **Pencil sound on drawings only** (shapes: underlines, circles, arrows, boxes, bubbles, checks) — the handwriting itself stays silent. One cue per shape, `data-duration` = that draw duration (+0.05), alternating pencil / pencil-rev on two tracks, volume ≈ 0.15 (The creator 2026-10-19: 0.55 "beats my voice", then asked for drawings-only and a bit lower). `whoosh-3` in, `whoosh-2` out. Never synthesize pencil sounds from noise — the creator: the synthetic one sounded "like scratching a wall" (2026-10-19).

### Phase 5: Verify Visuals

1. `npx hyperframes check` — must be **0 errors**. Expected harmless warnings: `nested_structure_needs_subcomposition`, `timeline_track_too_dense`, `composition_file_too_large`.
2. `npx hyperframes snapshot --at <one time per overlay> --no-end --describe false -o <scratchpad>/snaps` → Read the contact sheet(s). Check: nothing covers the face, no clipped text, no overlap between lower third and captions. Snapshot the middle of every B-roll cutaway: right image for the line, sharp at 1080p, subtitles/captions readable on top. Include times inside a lower-third window, a main-point caption window (small subtitle must be hidden), and plain talking stretches (subtitle visible, one line, readable).
3. Fix and re-snapshot until clean.

### Phase 6: Sound Effects

1. Pick from the skill's `assets/sfx/` and the SFX library (`catalog.json`). When no local clip fits a beat (keyboard typing, cash register, notification, meme boing), source a licensed clip, level it, and add it to the library. Prefer short, bright, dry cues; skip anything "drone", "riser", "tension", "eerie", "suspense", "sweep" or "ring". For a new pack:
   - Separate files or silence-separated sounds → `python3 scripts/sfx_kit.py <out_dir> <pack path>`.
   - One long compilation with sounds butting together → run `scripts/split_compilation.py` for a first pass, then render spectrograms in 18 s chunks (`ffmpeg -ss <t> -t 18 -i <file> -lavfi "showspectrumpic=s=1440x300:legend=1:scale=log:fscale=log:color=intensity:mode=combined" spec_N.png`), Read them, and set boundaries by eye (a new sound = sudden change in texture/pitch or a gap). Refine each cut to the quietest point between neighbours, then fade-in 5 ms / fade-out ≤ 0.25 s and loudnorm to -18 LUFS. Add the clips to a library folder with a `catalog.json` and an audition `index.html` (players + note fields) so the creator can listen and rename.
2. Character guide: `whoosh-7` big/long (intro + end card), `whoosh-3/4/5` punchy (panels in), `whoosh-1` soft (diagram swaps), `whoosh-2` quick (panels out); `pop` items/tiles/milestones; `tick` chapter tags, counters, streaks; `ding` completions; `impact` stamps/word slams. No `heartbeat` (banned — creepy/lonely).
3. Add one `<audio id="sfx-NN" src="assets/sfx/<name>.wav" data-start data-duration data-volume data-track-index>` per cue. **Every `<audio>` needs an `id`** or it's silent.
4. Start whooshes ~0.05 s before the visual move (their peak sits ~0.08 s in).
5. Volumes: the creator's voice ≈ -16 LUFS; clips are leveled to -18 LUFS. `data-volume` 0.2 (quiet ticks/outs) → 0.5 (intro/end whoosh) keeps SFX 8–12 dB under the voice.
6. Separate tracks per sound type (whooshes / pops+ticks / dings / impacts alternating) — layered sounds on one track trigger `duplicate_audio_track`.

Tell the creator plainly: Claude can measure sounds but can't hear them — he should judge the feel.

### Phase 6b: Background Music (subtle bed)

Music lives in your background-music folder (only tracks you are licensed to use on that channel). Keep it **subtle**.
**Pick steady, even, upbeat grooves** that don't fight the voice. Track choice matters more than the number: a busy track can feel too loud even 18 dB under. Note the tracks that work and reuse them as the default recipe; offer new music at the overlay-plan checkpoint, never swap silently.
- Log the chosen tracks (title, artist, source) in the video folder so the YouTube description can credit them if needed.

1. Measure each track (ffprobe duration, ebur128 loudness) and render a 40 s spectrogram. Skip heavy/dark/aggressive tracks (dense wall-to-wall low end, dramatic breakdowns) — the mood rule above applies to music too. Prefer steady, even grooves.
2. If no single track covers the video, chain tracks with 3 s `acrossfade` (bookending with the opening track works well). Always ffprobe the bed — a short bed silently cuts the music before the end.
2b. **No dry openings.** If a track opens with a sparse stop-start intro, start it with `-ss <seconds>` at its full groove.
3. Pre-mix ONE bed file with ffmpeg into `hf-project/assets/music/bed.wav`: per-track `loudnorm=I=-18` → crossfades → `atrim` to root duration → `highpass=f=70` + `equalizer=f=2500:width_type=o:width=1.5:g=-4` (clears room for speech but keeps body — the old 110 Hz / −6 dB made it thin) → `aecho=0.9:0.75:40|85|130:0.22|0.14|0.08` (light room, not dry) → `volume` ≈ **0.14** (re-measure after the reverb and scale the volume so the bed lands at the same LUFS as before — 7 Ways: test pass −40.3 → volume 0.1804 / swell 0.4509 for −38.1) (bed lands ≈ **-38.5 LUFS, ~24 dB under** the creator's ≈ -14.5 LUFS voice — the creator 2026-10-19: the old 0.28 / -32 LUFS level was "too loud, make it subtle") with an expression swell to ≈ 0.35 during the end card (no voice) → 1.5 s fade-in, fade-out on the last 1.6 s. Verify bed loudness with ebur128.
4. Add one `<audio id="music-bed" src="assets/music/bed.wav" data-start="0" data-duration="<root>" data-volume="1" data-track-index="40">`. Baking levels into the file keeps the composition simple and the mix exact.

### Phase 7: Preview — CHECKPOINT

```
npx --yes hyperframes@<ver> preview --background
npx --yes hyperframes@<ver> preview --status
```
URL is in the log: `http://localhost:3002/#project/hf-project`. Give it to the creator with a timestamped table of every overlay. Wait for approval or tweaks.

### Phase 8: Render + Verify

Run in the background (Bash `run_in_background`), output next to the original video:
```
npx --yes hyperframes@<ver> render --fps <source fps> --quality delivery -o "../<Video Name> - Final.mp4"
```
Use the source fps from Phase 1 (`30000/1001` for 29.97 DJI clips, `30` for the creator's current 30/1 footage). Pinned CLI version: `hyperframes@0.8.169`. Render time ≈ 1.1–1.3× the video length on an M4 Mac (4:41 → 4.5 min, 9:44 → 10–12 min); graphics-heavy edits take longer — 7 Ways (13:41, ~30 graphics + 16 B-roll) took 19.5–22.5 min with `HF_SEGMENTED_CAPTURE=true caffeinate -i -s npx --yes hyperframes@0.8.169 render -w 6 --fps 30 --quality delivery --resume -o …` (use this for anything > 5 min). The log's percentage and per-worker `framesCompleted` jump around — tell the creator the elapsed time and segment, not a made-up ETA. Run one render at a time — if a second is needed, queue it in one background command that waits for the first (`.hf-transaction-*` folder gone + output file present) before starting. **Re-renders after changes never overwrite a previous final** — name them `- Final v2 (<what changed>).mp4`, `v3`, … so the creator keeps every version he may have already uploaded. Then:
- ffprobe: 1920x1080, matching fps, h264 + aac, expected duration
- ebur128 loudness (≈ -17 LUFS, peak under -1 dBTP is fine)
- Extract 3 frames into a tile and Read it to confirm graphics and subtitles are burned in

After a render that changed the composition, copy `hf-project/index.html` over this skill's `example-composition.html` if it introduced a new reusable pattern.

Copy every B-roll and reference image used in the final into the B-roll library and append it to `catalog.json` (file, tags, type, source, credit, used_in, added) — see `broll.md` §4.


Report the file path, specs, and what the creator should watch for (lip-sync, SFX feel).

---

## Output Format

Report to the creator in short bullets: final file link, specs, overlay table, and next-step offers. Keep the editable project in `hf-project/` (don't delete it — re-renders take ~3 min). Never touch the original camera file.

# video-editor — a Claude Code skill

Edit talking-head YouTube videos with Claude Code and [HyperFrames](https://www.npmjs.com/package/hyperframes): cut "umm / ahh" fillers, add branded motion graphics, captions, subtitles, B-roll, sketch-board drawings, camera zooms, sound effects and a music bed, then render the final MP4. It also has a Screen-Tutorial Mode for screen recordings (bigger glowing cursor, quiet music).

Claude stops twice for you to check its work: once to approve the overlay plan, and once to review the preview before it renders.

## 1. Install the tools (Mac)

```bash
brew install ffmpeg whisper-cpp node
mkdir -p ~/whisper-models && curl -L -o ~/whisper-models/ggml-large-v3-turbo-q5_0.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
```

Filler removal needs a Python venv:

```bash
python3 -m venv ~/.venvs/align
~/.venvs/align/bin/pip install torch transformers numpy
```

You also need **Claude Code** (desktop app, VS Code extension or terminal) and the **HyperFrames skills** (`/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-keyframes`, `/hyperframes-audio`) installed in `~/.claude/skills/`.

## 2. Install the skill

```bash
git clone https://github.com/chadgodoy-hash/video-editor-skill.git ~/.claude/skills/video-editor
```

Or copy the folder into your project's `.claude/skills/video-editor/`. Restart Claude Code.

## 3. Make it yours (once)

1. Fill in **`brand.md`**: your colors, fonts, name, site, tagline and logo.
2. Add a **whoosh pack** to `assets/sfx/` as `whoosh-1.wav` … `whoosh-7.wav`. Level the clips with `python3 scripts/sfx_kit.py <out_dir> <pack>`.
3. Make an **SFX library** folder and point `SFX_LIB` at it (`export SFX_LIB=~/sfx-library`). Put a `catalog.json` in it, and set `"banned": true` on any clip you don't like.
4. Make a **music folder** with tracks you're licensed to use on your channel.
5. Read the **Standing Rules** in `SKILL.md` and edit them to match your taste. They hold the original creator's preferences, like a calm intro, constant zoom, sketch boards and music about 24 dB under the voice.

## 4. Use it

Put your video in a folder, open Claude Code there, and say:

> edit this video

or `/video-editor path/to/video.mp4`.

## What's inside

- `SKILL.md` — the full workflow Claude follows
- `brand.md` — your brand kit
- `broll.md` — the B-roll research playbook
- `scripts/` — filler removal, subtitles, cursor tracking, the scene library (`scenes.py`) and example generators
- `templates/`, `example-composition.html`, `examples/` — real compositions to copy patterns from
- `assets/` — fonts (SIL Open Font License), cursor templates and starter SFX (generated, plus CC0 pencil sounds; credits are in `assets/sfx/credits/`)

The example compositions come from real videos. Reuse their patterns, not their copy or timings.

# Tools

These scripts build the SVGs in `../assets`. GitHub READMEs cannot run JavaScript or load web fonts. Because of this, each image is a standalone SVG. Its animation is CSS, and its fonts are embedded as subsets.

## Set up once

```sh
cd tools && npm install && cd ..
pip install fonttools brotli
```

Google Chrome must be installed. To use another Chrome, set `CHROME_PATH`.

## Rebuild

Run these commands from the repo root.

```sh
python3 tools/gen_hero.py      # assets/hero.svg: keyboard + terminal
python3 tools/gen_oss.py       # assets/oss-*.svg: open-source cards
```

To change the terminal text, edit `OUTPUT` at the top of `tools/gen_hero.py`. A line can hold about 59 characters after the label column. A row with an empty label continues the row above it.

## Check before you push

```sh
node tools/film.mjs assets/hero.svg tools/shots/still.png --times 0 --scale 1     # payoff frame
node tools/film.mjs assets/hero.svg tools/shots/seq.png --times 1.5,3.8,8.5      # beats of the loop
node tools/img.mjs assets/hero.svg tools/shots/img.png 2500 600                  # real <img>, light + dark
node tools/page.mjs                                                              # whole README, light + dark
```

Screenshots go to `tools/shots/`. Git ignores this folder.

## Fonts

Geist and Geist Mono are by Vercel and use the SIL Open Font License (`fonts/OFL.txt`).

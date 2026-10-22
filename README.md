# LOVE.ai — AI Engineer Romantic Birthday Experience

## Run it
Open `index.html` in your browser. The soundtrack can be started with the music button; browsers do not permit auto-playing audio without an interaction.

## Personalize
Edit `const SETTINGS` inside `index.html`:
- `partnerName`, `yourName`, `birthdayNote`, and `finalMessage`
- `memories`: each record supports `icon`, `title`, `text`, and `image`.

## Add real photos
Put your own photos in the `photos/` folder, named:
- `first-date.jpg`
- `vacation.jpg`
- `favorite-memory.jpg`

Or modify the `image` filenames inside SETTINGS. If a file is missing, the photo area will show a friendly placeholder rather than a broken image. You may add any number of memories. Images appear **one at a time**: the next memory requires a click, and the game cannot start until every photo has been revealed.

## The experience
1. Welcome / initialize LOVE.ai
2. Terminal authentication (password LOVE by default)
3. Love letter — open on click
4. Photo memories — one by one
5. Catch five hearts
6. Blow out all candles
7. Final birthday surprise

Only one stage is on screen at any given time. Music controls persist.

## Share with a QR code
Publish the **whole folder** (including `assets/` and `photos/`) to Netlify Drop (https://app.netlify.com/drop) or GitHub Pages. Then make a QR card pointing to the final public URL:

```
python -m pip install 'qrcode[pil]' pillow
python generate_qr_card.py https://your-published-site.example/ --name "My Love" --from-name "Your Name"
```

Run `python generate_qr_card.py --help` to check supported options. The included `qr_card_template.png` is a design template, not a live QR code to your unpublished webpage.

## Privacy
Anyone with access to the public site or a direct image link may be able to see uploaded photos. Use photos you're comfortable publishing.

export interface ToolCopy {
  title: string;
  description: string;
  intro: string;
  faq: Array<{ q: string; a: string }>;
}

export const TOOL_COPY: Record<string, ToolCopy> = {
  '/': {
    title: 'Compress any image, in your browser',
    description: 'Shrink JPG, PNG, and WebP files instantly — no uploads, no account, no nonsense.',
    intro: `makepicsmall runs 100% in your browser. Your photos never touch our servers. Drop a file, we squish it, you download — simple.\n\nWhen you need more than "smaller," use a preset: compress specifically for WhatsApp, Instagram, your resume, or a passport photo. Every preset uses the exact size, dimensions, and format each destination actually expects.`,
    faq: [
      { q: 'Are my photos uploaded?', a: 'No. Compression runs entirely in your browser using WebAssembly. No file leaves your device.' },
      { q: 'What formats are supported?', a: 'JPG, PNG, and WebP at launch. AVIF, GIF, and HEIC support is coming.' },
      { q: 'Is there a file size limit?', a: "Yes — 50 MB per file so browsers don't run out of memory. Bigger files? Downscale first." },
    ],
  },
  '/compress/jpg': {
    title: 'Compress JPG — free, browser-based, no uploads',
    description: 'Shrink JPG file size instantly. Pick a quality or target size, download the result. Nothing uploaded.',
    intro: `Drop any JPG and we'll squish it using mozjpeg — the same optimizer Google's Squoosh uses, running in your browser. You can set a quality level (1–100) or a hard target size in KB.\n\nFor most photos, quality 75–85 is visually identical to the original at roughly half the size. Below 50, most people start noticing artifacts around edges.`,
    faq: [
      { q: 'How much can a JPG be compressed?', a: 'Typically 40–70% size reduction with no visible quality loss. Photos from smartphones often shrink the most because they ship with very high quality settings.' },
      { q: 'Will my EXIF data be preserved?', a: 'No — our compressor strips metadata. This is usually what you want; it makes the file smaller and removes location data before sharing.' },
      { q: 'What if I need the smallest possible file?', a: "Set a target size (100 KB, 500 KB, etc.) — we'll binary-search quality to hit it." },
    ],
  },
  '/compress/png': {
    title: 'Compress PNG — lossless shrinking in your browser',
    description: 'Reduce PNG file size while keeping the transparency and crisp edges. Runs fully client-side.',
    intro: `PNG compression is different from JPG. PNGs use lossless compression by default, so we're reorganizing the file structure, not throwing away pixels. Typical savings: 30–50%, sometimes more on screenshots and flat-color graphics.\n\nIf you need more aggressive savings and your PNG has lots of colors (like a photo), consider switching to JPG or WebP instead — click the format selector above.`,
    faq: [
      { q: 'Does this preserve transparency?', a: 'Yes. We use oxipng, which is lossless — alpha channels, color profiles, everything stays intact.' },
      { q: 'Why is my PNG still big after compression?', a: 'PNG is meant for lossless compression. Photos in PNG format are rarely compressible much — switch to JPG or WebP for 80%+ smaller files.' },
      { q: "What's the difference between PNG and WebP?", a: 'WebP offers lossless compression like PNG but smaller files, and also supports lossy mode. All modern browsers support it.' },
    ],
  },
  '/compress/webp': {
    title: 'Compress WebP — squeeze more out of modern images',
    description: 'Further reduce WebP file size with adjustable quality. Client-side, no uploads.',
    intro: `WebP is already a modern, efficient format. If you got a WebP from a camera app or web source and it's still big, we can squeeze more out of it — especially if the original was saved at a conservatively high quality.\n\nLike JPG, WebP supports lossy compression. Quality 80 is the sweet spot for most use cases.`,
    faq: [
      { q: 'Should I use WebP or JPG?', a: "WebP is ~25–35% smaller than equivalent-quality JPG. All modern browsers and most platforms support it. Prefer WebP unless you're serving to very old systems." },
      { q: 'Can I convert to WebP from JPG?', a: 'Format conversion is in Phase 2 — for now, we only re-encode WebP to WebP on this page.' },
      { q: 'Does WebP support transparency?', a: 'Yes — both lossy and lossless WebP support alpha channels.' },
    ],
  },
  '/compress/jpg/to/100kb': {
    title: 'Compress JPG to 100 KB (or less)',
    description: 'Shrink any JPG to 100 KB with automatic quality adjustment. Runs in your browser.',
    intro: `100 KB is the standard upload limit for many document forms, resume portals, and government ID applications. We automatically find the highest quality that fits under 100 KB.\n\nFor portrait-style photos, 100 KB typically gives you usable quality at 600–800 pixels on the long side. For very large source images, we recommend also setting a max dimension or using our resume / passport presets.`,
    faq: [
      { q: "What if my photo can't fit in 100 KB?", a: "We'll get as close as possible and show you the result. Very large or detailed images may need to be cropped or resized first." },
      { q: 'Which platforms need 100 KB JPGs?', a: 'Common requirements: resume portals, some passport applications (check country), older web forms, email signatures.' },
      { q: 'Will it look pixelated?', a: 'At 100 KB for a full-size photo, yes. For profile-photo sized images (600×600 or smaller), quality is usually good.' },
    ],
  },
  '/compress/jpg/to/500kb': {
    title: 'Compress JPG to 500 KB',
    description: 'Get a JPG under 500 KB while keeping as much quality as possible. Binary-search is automatic.',
    intro: `500 KB is a comfortable upload ceiling for most social posts, email attachments, and blog images. Our quality search finds the setting that hits as close to 500 KB as possible without going over.\n\nFor typical photos from a phone (2–10 MB source), this works out to a visually-identical result most people won't notice is compressed.`,
    faq: [
      { q: 'Why 500 KB specifically?', a: "It's a common soft limit: fast loading on blogs, fits in most email providers comfortably, and generally indistinguishable from the original to a casual viewer." },
      { q: 'Can I set a custom target?', a: 'Yes — use our main compress tool and type a custom KB value in the target field.' },
      { q: 'Does this change the image dimensions?', a: 'No — this page compresses only. To also resize, use one of our preset pages like "for Instagram" or set max dimensions in the main tool.' },
    ],
  },
  '/compress/png/to/100kb': {
    title: 'Compress PNG to 100 KB',
    description: 'Lossless PNG compression targeting 100 KB. Transparency and edges preserved.',
    intro: `PNG compression is fundamentally different from JPG — we can't just lower "quality." To hit 100 KB on a photo-style PNG, we may need to reduce the palette or transition through a lossy step. For logos, screenshots, and flat graphics, 100 KB is usually easy to achieve losslessly.\n\nIf your PNG is a photo, consider converting to JPG or WebP — you'll get 100 KB with much better visual quality.`,
    faq: [
      { q: "What if my PNG can't be compressed to 100 KB losslessly?", a: "We'll get it as close as possible. For complex photos, you may need to switch to JPG or WebP." },
      { q: 'Will transparency be preserved?', a: 'Yes, if we stay in lossless mode. For heavy compression, some PNGs drop to 8-bit palette which preserves transparency but reduces color count.' },
      { q: 'Why are PNG files so large?', a: 'PNG is lossless, so it preserves every pixel exactly. Perfect for graphics with sharp edges. Terrible for photographs.' },
    ],
  },
  '/to/50kb': {
    title: 'Compress image to 50 KB',
    description: "Shrink any JPG, PNG, or WebP to under 50 KB. Pick a file — we'll try to fit it.",
    intro: `50 KB is tight — this is what small-form document upload portals often require. We keep the input format and automatically find the best quality that fits.\n\nFor typical phone photos, reaching 50 KB requires significant downsampling. If you just need a thumbnail or small profile picture, 50 KB often works well.`,
    faq: [
      { q: 'Is 50 KB too small to look good?', a: 'For a full-size photo: often yes. For small thumbnails (300×300 or smaller): usually fine.' },
      { q: 'Can you resize my image too?', a: 'Not on this page — use a preset page like /for/resume for both resize and compress.' },
      { q: 'Why would I need 50 KB?', a: "Some government forms and old-school web forms enforce strict size limits. Check the requirements of whatever you're uploading to." },
    ],
  },
  '/to/100kb': {
    title: 'Compress image to 100 KB',
    description: 'Any JPG, PNG, or WebP down to 100 KB — quality preserved where possible.',
    intro: `100 KB is the classic document-upload limit. Our tool finds the best quality under that ceiling for whichever format you upload.\n\nIf you specifically need a JPG output, use /compress/jpg/to/100kb instead — it forces JPG format regardless of input.`,
    faq: [
      { q: 'What file format will I get back?', a: 'The same format as your input. Upload a PNG, get a smaller PNG. Upload a JPG, get a smaller JPG.' },
      { q: 'What if I want to change format?', a: 'Format conversion is in Phase 2. For now, pick a format-specific page from our home.' },
      { q: 'Does this work on transparent PNGs?', a: 'Yes — transparency is preserved in PNG output.' },
    ],
  },
  '/to/500kb': {
    title: 'Compress image to 500 KB',
    description: 'Generous ceiling, minimal visible quality loss. For most photos this is "invisible" compression.',
    intro: `500 KB is where smart compression shines — visually identical to the original for most photos, but half to a quarter of the file size. Great for email attachments, blog posts, and social media.`,
    faq: [
      { q: 'Will viewers notice the difference?', a: 'Typically no. 500 KB is above the threshold where most compression artifacts are visible on a screen.' },
      { q: 'Good for blog posts?', a: 'Perfect. Most blog themes display images at 800–1200px wide — 500 KB is more than enough resolution for that.' },
      { q: 'What if I need smaller?', a: 'Try /to/100kb or /to/50kb for tighter targets.' },
    ],
  },
  '/to/1mb': {
    title: 'Compress image to 1 MB',
    description: 'A safe upper bound for most web and email use. Retains near-original quality.',
    intro: `1 MB (1000 KB) is a comfortable ceiling for almost any online use. Most photos compress to 1 MB with zero visible quality loss.\n\nIf your upload destination is more strict (many are 500 KB or 100 KB), use one of those pages instead.`,
    faq: [
      { q: 'Can I email a 1 MB photo?', a: 'Yes, easily — all major email providers accept attachments up to 20–25 MB.' },
      { q: 'Is 1 MB small enough for WordPress?', a: 'Fine for upload, but for page speed aim lower (~300 KB per image on a blog post).' },
      { q: 'When would I use 1 MB specifically?', a: 'Forms with strict-ish limits where you still want maximum quality. Not common — most forms are stricter.' },
    ],
  },
  '/for/whatsapp': {
    title: 'Compress photo for WhatsApp (full quality)',
    description: "Send photos on WhatsApp without losing quality — resize to 1600 pixels and compress below the auto-squish threshold.",
    intro: `WhatsApp automatically re-compresses any photo you share in a chat, which is why pictures from friends look soft and blocky. The workaround: pre-shrink the photo yourself so WhatsApp leaves it alone, or send it in Document mode. We resize your photo to 1600 pixels on the long side and compress it enough that WhatsApp's server-side pass has little left to do.\n\nFor the best result, send the output file via "Document" (paperclip → Document) instead of the photo picker. Document mode skips WhatsApp's recompression entirely — your photo arrives exactly as you sent it, without losing quality.`,
    faq: [
      { q: 'Why does WhatsApp ruin my photos?', a: 'WhatsApp re-encodes every image sent through the photo picker at a low quality setting to save bandwidth. The fix is either to send it as a Document, or to pre-compress it so the re-encoding pass has little effect.' },
      { q: 'What is Document mode?', a: 'In any WhatsApp chat, tap the paperclip/attach icon and choose "Document" instead of "Photo." Your file is delivered as-is with no recompression.' },
      { q: 'Will 1600 pixels look good on big screens?', a: 'Yes — 1600 pixels on the long side displays sharply on phones, tablets, and most laptops. If the recipient zooms in aggressively on a 4K monitor, they might notice, but for normal viewing it is indistinguishable from the original.' },
    ],
  },
  '/for/whatsapp-dp': {
    title: 'Compress photo for WhatsApp DP (profile picture)',
    description: 'Crop and shrink a photo for your WhatsApp DP — 640 × 640 pixels, under 100 KB.',
    intro: `WhatsApp renders your profile picture (the WhatsApp DP) as a tight circle roughly 192 pixels across, but it stores a 640 × 640 source that it uses when someone taps your photo to see it full-size. We center-crop your image to a square, resize to 640 × 640, and compress to under 100 KB so it uploads fast even on a slow connection.\n\nA square source works best — if you feed us a portrait or landscape photo, we center-crop geometrically. If your face is off-center, crop it yourself first so the important part survives.`,
    faq: [
      { q: 'Why 640 × 640?', a: 'That is the internal resolution WhatsApp stores and displays when someone views your profile picture full-size. Larger images get downscaled anyway.' },
      { q: 'Will the tool center my face?', a: 'No — we center-crop geometrically from the middle of the source image. Pre-crop your photo if your face sits off to one side.' },
      { q: 'Does this work for WhatsApp Business profile pictures?', a: 'Yes — WhatsApp Business uses the same 640 × 640 specification for profile photos.' },
    ],
  },
  '/for/instagram': {
    title: 'Compress photo for Instagram feed post',
    description: 'Resize and compress a photo for an Instagram feed post — 1080 pixels on the long side.',
    intro: `Instagram displays feed photos at 1080 pixels on the long side and re-compresses anything bigger. Upload a pre-sized 1080 pixel image and the server has nothing left to shrink — your photo reaches the feed looking exactly like it does on your screen.\n\nWe downscale to 1080 pixels on the long side (whatever aspect ratio your photo has) and compress to around 500 KB. That gives Instagram a clean file to work with and keeps colors and sharpness intact.`,
    faq: [
      { q: 'What aspect ratios does Instagram support for a feed post?', a: 'Square (1:1), landscape (1.91:1), and portrait (4:5). Outside those bounds Instagram will crop. Our tool preserves whatever aspect ratio you upload — so crop first if you want a specific shape.' },
      { q: 'Will Instagram still compress my upload?', a: 'A little — Instagram always runs a lossy pass. But giving it a correctly-sized, pre-compressed file produces a visibly sharper result than uploading the full-size original.' },
      { q: 'Should I use this for Stories instead?', a: 'No — Stories are 1080 × 1920 (9:16). Use /for/instagram-story for that.' },
    ],
  },
  '/for/instagram-story': {
    title: 'Compress photo for Instagram Story',
    description: 'Resize and compress a photo to 1080 × 1920 (9:16) for Instagram Story uploads.',
    intro: `Instagram Stories are a strict 9:16 aspect ratio at 1080 × 1920 pixels. We center-crop your photo to 9:16, resize to 1080 × 1920, and compress so it uploads quickly on mobile data.\n\nIf your source photo is already a tall 9:16 shot, the crop is a no-op. If it is landscape or square, we crop from the middle — pre-crop yourself if the subject is off-center.`,
    faq: [
      { q: 'Why 1080 × 1920?', a: 'That is the exact pixel dimension Instagram uses for Story media. Uploading a larger file just gets downscaled; a smaller file gets upscaled and looks soft.' },
      { q: 'Can I use this for Reels?', a: 'Yes — Reels use the same 1080 × 1920 (9:16) specification for cover images and video frames.' },
      { q: 'What about text overlays and stickers?', a: "Add those inside Instagram after you upload. We only handle the base image; everything else is the app's job." },
    ],
  },
  '/for/resume': {
    title: 'Compress photo for a resume or CV',
    description: 'Shrink a headshot for your resume or CV — 600 × 600 pixels, under 100 KB, friendly to ATS systems.',
    intro: `Most resume templates and ATS (applicant tracking systems) prefer a square headshot around 600 × 600 pixels and under 100 KB. A giant 4 MB photo from your phone bloats the PDF and sometimes gets rejected outright. We center-crop your photo to square, resize to 600 × 600, and compress to fit comfortably under 100 KB.\n\nFor the best-looking CV, start with a head-and-shoulders shot against a plain background, taken in good lighting. We handle the file size; the photo choice is up to you.`,
    faq: [
      { q: 'Will an ATS read my photo?', a: 'Most ATS systems ignore photos entirely, but a small, well-formatted image avoids file-size errors on upload and keeps your CV PDF small enough to email. A 600 × 600 JPG under 100 KB is a safe default.' },
      { q: 'Should my resume even have a photo?', a: 'In the US, UK, and Canada, photos are discouraged on resumes. In most of continental Europe, Asia, and Latin America, they are standard. Follow local convention.' },
      { q: 'Can I use this photo for LinkedIn too?', a: 'LinkedIn prefers 400 × 400 — close but not identical. Use /for/linkedin for a LinkedIn-specific crop and size.' },
    ],
  },
  '/for/passport-us': {
    title: 'Compress photo for US passport application',
    description: 'Resize and compress a photo to meet state.gov requirements: 600 × 600 JPG, under 240 KB.',
    intro: `The US Department of State requires a 600 × 600 pixel JPG under 240 KB for digital passport applications. We automatically crop your photo to square, resize to 600 × 600, and compress to fit.\n\nBefore using this tool: make sure your source photo matches the other state.gov requirements — full-face view, plain white background, no glasses, no hat. We only handle the file dimensions and size — composition is up to you.`,
    faq: [
      { q: 'What are the official US passport photo specs?', a: '600 × 600 to 1200 × 1200 pixels (we default to 600 × 600), JPG only, under 240 KB file size. See travel.state.gov for the full guidance on composition, lighting, and background.' },
      { q: 'Will this tool auto-center my face?', a: 'No — we center-crop geometrically. Start with a photo where your face is already in the middle.' },
      { q: 'Can I use this for Canadian or UK passports?', a: 'No — those have different requirements. See /for/passport-canada or /for/passport-uk.' },
    ],
  },
  '/for/passport-canada': {
    title: 'Compress photo for Canadian passport application',
    description: 'Resize and compress a photo for an IRCC Canadian passport submission — 420 × 540 pixels, under 240 KB.',
    intro: `IRCC (Immigration, Refugees and Citizenship Canada) requires a specific photo size for a Canadian passport application. For the online uploaded version we target 420 × 540 pixels, JPG, under 240 KB. We center-crop your photo to a 7:9 ratio, resize to 420 × 540, and compress to fit.\n\nThe Canadian passport photo spec is stricter than most — face height, expression, background, and print size all matter. We handle the digital file size and pixel dimensions only. Check the IRCC guidance for composition rules before you submit.`,
    faq: [
      { q: 'What are the IRCC passport photo requirements?', a: 'For a digital photo: 420 × 540 pixels minimum, JPG, under 240 KB. For printed photos the standard is 50 × 70 mm with face 31–36 mm tall. Background must be plain white or light grey.' },
      { q: 'Is the digital photo accepted for every passport service?', a: 'Digital photos are accepted for online applications and renewals. In-person applications still require printed photos taken by an approved photographer.' },
      { q: 'Can I crop my face in the photo?', a: 'The IRCC wants your face to fill a specific portion of the frame. Our tool does a center crop — pre-crop the image yourself if your face is not already centered and sized correctly.' },
    ],
  },
  '/for/passport-uk': {
    title: 'Compress photo for UK passport application',
    description: 'Resize and compress a photo for a UK passport online application — 600 × 750 pixels, JPG.',
    intro: `The UK Passport Office accepts a digital photo up to 10 MB, but a cleaner, correctly-sized file uploads faster and avoids the "we could not read your photo" bounce-back. We resize to 600 × 750 pixels (a 4:5 portrait crop that matches the traditional passport photo ratio) and compress to keep the file under 1 MB.\n\nThe UK has specific rules about expression, lighting, and background — we do not enforce those. Start with a photo that already meets the composition guidelines on gov.uk before running it through the tool.`,
    faq: [
      { q: 'What does gov.uk require for the digital photo?', a: 'A JPEG between 50 KB and 10 MB, at least 600 × 750 pixels, taken in the last month, plain light background, neutral expression. We target 600 × 750 because larger files offer no benefit and upload slower.' },
      { q: 'Can I take the photo myself?', a: 'Yes — gov.uk accepts phone photos as long as they meet the composition rules. Use a plain wall, even lighting, and hold the camera at eye level.' },
      { q: 'Will the Passport Office re-check the photo?', a: 'Yes — after upload the photo is automatically validated. If it is too small, too big, or wrong-shaped, you are asked to retake it. This tool prevents the first two failure modes.' },
    ],
  },
  '/for/linkedin': {
    title: 'Compress photo for LinkedIn profile photo',
    description: 'Crop and shrink a headshot for a LinkedIn profile photo — 400 × 400 pixels, under 200 KB.',
    intro: `LinkedIn displays your profile photo as a 400 × 400 pixel square and recompresses anything bigger. Upload a pre-sized 400 × 400 image and the server leaves it alone, so your photo stays sharp on every device. We center-crop your photo to square, resize to 400 × 400, and compress to under 200 KB.\n\nFor best results, start with a head-and-shoulders shot where your face fills roughly 60% of the frame. LinkedIn crops to a circle on display, so anything in the corners will be hidden.`,
    faq: [
      { q: 'Why 400 × 400 and not bigger?', a: 'LinkedIn caps displayed size at 400 × 400 for profile photos. A 2000 × 2000 upload is downscaled server-side with extra compression — a pre-sized 400 × 400 file keeps its original sharpness.' },
      { q: 'Does LinkedIn crop my profile photo to a circle?', a: 'Yes on every display surface. Make sure your face is centered and nothing important sits in the four corners of the square.' },
      { q: 'Should I use the same photo for my resume?', a: 'You can, but the resume page targets 600 × 600 and under 100 KB. Resume PDFs embed photos differently than web profiles, so a resume-specific version is usually cleaner.' },
    ],
  },
};

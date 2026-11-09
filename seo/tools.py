#!/usr/bin/env python3
"""Writes the free tool pages in content/tools/. Each page: the working tool, a direct answer,
how-to steps, tips, an FAQ and the install card. Re-run after editing; it overwrites the files."""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "content", "tools")
DATE = "2026-11-08"

PRIVATE = ("<h2>Private by design</h2><p>The tool runs entirely inside this browser tab. Your photo is opened, edited and saved "
           "on your own device, and it is never sent to a server, so there is nothing for anyone to keep, scan or leak. "
           "No account, no watermark and no limit on how many photos you do. It even keeps working if you switch off your "
           "internet after the page has loaded.</p>")

def hide_line():
    return ('<p>Photos you never want anyone to see are better kept out of the gallery altogether. See '
            '<a href="{{root}}guides/how-to-hide-photos-on-android">how to hide photos on Android</a>, or how Sealcloak keeps them '
            '<a href="{{root}}features/encryption">encrypted on your phone</a>.</p>')

T = []
def tool(**k): T.append(k)

# ---------------------------------------------------------------- compress
COMPRESS_HOW = """<h2>How it works</h2>
<p>JPEG and WebP photos have a quality setting. The tool tries different settings and keeps the highest quality that still fits your target, so the photo looks as good as it can at that size. If even a low quality is too big (a huge photo squeezed into a tiny limit), it shrinks the width and height step by step until it fits. You'll see the new size next to each photo before you download it.</p>"""

def compress_page(slug, kb, kw, title, desc, lead, answer, uses, faq_extra, also):
    tool(slug=slug, tool="compress", opt={"targetKB": kb}, kw=kw, also=also, title=title, desc=desc,
         nav=f"Compress image to {kb} KB" if kb != 200 else "Compress image",
         summary=f"Shrink photos to {kb} KB or any size you need, without uploading them." if kb != 200 else "Shrink photos to the file size you need, without uploading them.",
         h1=title.split(":")[0], lead=lead, answer=answer,
         body=f"""<h2>How to compress a photo to {kb} KB</h2>
<ol>
<li>Choose your photo above, or drop it on the box. You can do several at once.</li>
<li>Check the target size. It's set to <strong>{kb} KB</strong>; type another number if your form asks for something different.</li>
<li>Keep JPEG as the format: it's accepted everywhere. Pick WebP only for websites.</li>
<li>Tap <strong>Download</strong> next to the result. The file name ends in its new size so you can find it.</li>
</ol>
{COMPRESS_HOW}
<h2>Where you'll need it</h2>
{uses}
{{{{cta}}}}
{PRIVATE}
<h2>Tips for the sharpest result</h2>
<ul>
<li><strong>Crop first.</strong> Cutting away empty background leaves more of the size budget for the part that matters. Use the <a href="{{{{root}}}}tools/crop-image">crop tool</a>, then compress.</li>
<li><strong>Set the longest side</strong> if the form also lists pixel dimensions. Smaller dimensions at good quality usually look better than big dimensions at low quality.</li>
<li><strong>Screenshots and scans</strong> of text compress very well as JPEG once they're cropped to the page.</li>
</ul>
{hide_line()}""",
         faq=[
            {"q": f"Will compressing to {kb} KB make my photo blurry?", "a": f"Only as much as it has to. The tool keeps the highest quality that fits in {kb} KB, and only reduces the dimensions if quality alone isn't enough. Cropping away background first leaves more detail for the subject."},
            {"q": "Is my photo uploaded to a server?", "a": "No. Everything happens in your browser on your own device. The photo is never sent anywhere, so it can't be stored, scanned or leaked by this site."},
            {"q": "Does it work on Android and iPhone?", "a": "Yes. It works in Chrome, Samsung Internet, Firefox and Safari on phones, tablets and computers. iPhone HEIC photos are converted to JPEG as part of the process."},
            {"q": "Can I compress several photos at once?", "a": "Yes. Choose or drop as many as you like. Each one is compressed to the same target size and gets its own download button."},
         ] + faq_extra)

compress_page("compress-image", 200, "compress image",
    "Compress image: reduce photo size in KB, free and private",
    "Reduce the file size of a photo to the KB you need. Free, no sign-up and no upload: the photo is compressed in your browser and never leaves your phone.",
    "Make a photo smaller in KB for forms, email or a website. Pick a target size, drop in your photos, and download them, all without uploading anything.",
    "To compress an image, choose it above, type the size you need in KB and tap Download. The tool picks the best quality that fits, and only shrinks the dimensions if it has to. Your photo stays on your device the whole time.",
    "<ul><li>Email attachments and messaging apps with size limits.</li><li>Job, college and government application forms.</li><li>Website and online shop images that need to load fast.</li><li>Freeing up storage when you keep many large photos.</li></ul>",
    [{"q": "What's the difference between compressing and resizing?", "a": "Compressing lowers the file size in KB, mostly by adjusting quality. Resizing changes the width and height in pixels. This tool compresses first and only resizes when a target is too small to reach otherwise."}],
    ["reduce image size", "image compressor", "reduce photo size in kb", "compress jpeg"])

compress_page("compress-image-to-100kb", 100, "compress image to 100kb",
    "Compress image to 100 KB: free, fast and private",
    "Compress a photo to under 100 KB for online forms and applications. Free, works on your phone, and the photo is never uploaded anywhere.",
    "Many application forms only accept photos under 100 KB. Drop your photo in, and download a copy that fits, with the best quality possible at that size.",
    "To compress an image to 100 KB, choose it above and tap Download: the target is already set to 100 KB. The tool keeps the highest quality that fits and only reduces the dimensions if needed. Nothing is uploaded.",
    "<ul><li>Government, passport and visa application portals.</li><li>College admission and scholarship forms.</li><li>Job portals and HR systems that cap photo uploads.</li><li>Profile pictures on sites with strict limits.</li></ul><p>Some forms ask for a range, such as 20 to 100 KB. Aim a little under the maximum, for example 90 KB, so the file is safely accepted.</p>",
    [{"q": "My form says between 50 KB and 100 KB. What should I type?", "a": "Type about 90 in the target size box. The result will be just under 100 KB and comfortably above the minimum, which forms accept most reliably."}],
    ["reduce photo size to 100kb", "100kb photo converter", "resize image to 100kb", "jpg to 100kb"])

compress_page("compress-image-to-50kb", 50, "compress image to 50kb",
    "Compress image to 50 KB online: free, no upload",
    "Shrink a photo to under 50 KB for exam and job forms. Free, quick on any phone, and private: the photo is compressed on your device, never uploaded.",
    "Exam and recruitment forms often want a photo under 50 KB. Drop yours in and download a sharp copy that fits, without sending it to any website.",
    "To compress an image to 50 KB, choose it above and tap Download; the target is already 50 KB. For passport-style photos, crop to the head and shoulders first so the face stays sharp. The photo never leaves your phone.",
    "<ul><li>Exam registration forms that ask for a recent photo between 20 and 50 KB.</li><li>Recruitment portals and online applications.</li><li>ID cards and membership forms.</li></ul><p>If the form also gives pixel dimensions, such as 200 × 230, use the <a href=\"{{root}}tools/resize-image\">resize tool</a> first and compress after.</p>",
    [{"q": "How do I get a photo between 20 KB and 50 KB?", "a": "Type 45 in the target size box. The result lands just under 50 KB and well above 20 KB. If a form rejects it, check whether it also needs exact pixel dimensions."}],
    ["reduce photo size to 50kb", "photo resize 50kb", "image to 50kb converter", "compress jpg to 50kb"])

compress_page("compress-image-to-20kb", 20, "compress image to 20kb",
    "Compress image to 20 KB: photos and signatures, free",
    "Shrink a photo or signature to under 20 KB for application forms. Free, works on your phone, nothing is uploaded: it all happens in your browser.",
    "Signature uploads and small ID photos often have to be under 20 KB. Crop tightly, drop the image in, and download a copy that fits.",
    "To compress an image to 20 KB, crop it to just the signature or face, then choose it above and tap Download; the target is already 20 KB. Tight cropping keeps it readable at this small size. Nothing is uploaded.",
    "<ul><li>Signature uploads on exam and government forms (often 10 to 20 KB).</li><li>Thumb impressions and small ID photos.</li><li>Old systems with very small upload limits.</li></ul><p>For a signature, sign on plain white paper with a dark pen, photograph it in good light, and crop right to the ink before compressing.</p>",
    [{"q": "Why does my signature look faint after compressing?", "a": "Usually because the photo includes lots of paper around it. Crop close to the ink so the size budget goes to the signature, and photograph it in bright, even light with a dark pen."}],
    ["signature resize 20kb", "reduce image size to 20kb", "photo 20kb converter", "compress signature image"])

# ---------------------------------------------------------------- resize, crop
tool(slug="resize-image", tool="resize", opt={"w": 1080}, kw="resize image", also=["resize photo", "change image size in pixels", "image resizer online", "resize image to 1080"],
     title="Resize image: change photo size in pixels, free", nav="Resize image",
     desc="Resize photos to exact pixel dimensions or by percentage. Free, keeps proportions, works on your phone, and photos are never uploaded.",
     summary="Change a photo's width and height in pixels or by percentage.",
     h1="Resize image", lead="Change a photo to the exact width and height you need, or scale it by a percentage. Proportions stay right unless you choose otherwise.",
     answer="To resize an image, choose it above, type the width or height in pixels (or switch to percentage), and tap Download. Leave Keep proportions on so the photo isn't stretched. Everything happens on your device.",
     body=f"""<h2>How to resize a photo</h2>
<ol>
<li>Pick <strong>Width and height</strong> to set pixels, or <strong>Percentage</strong> to scale (50% halves both sides).</li>
<li>Type a width, a height, or both. With <strong>Keep proportions</strong> on, the photo fits inside the size you typed without stretching.</li>
<li>Choose the photos. Each one is resized and gets its own download button.</li>
</ol>
<h2>Common sizes</h2>
<div class="table-wrap"><table>
<thead><tr><th>Use</th><th>Size in pixels</th></tr></thead>
<tbody>
<tr><td>Instagram square post</td><td>1080 × 1080</td></tr>
<tr><td>Instagram portrait post</td><td>1080 × 1350</td></tr>
<tr><td>Stories, Reels, WhatsApp status</td><td>1080 × 1920</td></tr>
<tr><td>YouTube thumbnail</td><td>1280 × 720</td></tr>
<tr><td>Profile picture (most sites)</td><td>400 × 400 or larger</td></tr>
<tr><td>Full HD wallpaper</td><td>1920 × 1080</td></tr>
</tbody></table></div>
<p>To fill an exact shape such as 1080 × 1350 without stretching, <a href="{{{{root}}}}tools/crop-image">crop to 4:5</a> first, then resize.</p>
{{{{cta}}}}
{PRIVATE}
<h2>Resizing vs compressing</h2>
<p>Resizing changes the number of pixels. Compressing changes how much space those pixels take in KB. If a form gives a limit in KB, use <a href="{{{{root}}}}tools/compress-image">compress image</a>. If it gives pixels, resize here. Some forms want both: resize first, then compress.</p>
{hide_line()}""",
     faq=[
        {"q": "Will resizing make my photo blurry?", "a": "Making a photo smaller keeps it sharp; the tool scales down in steps for a clean result. Making a photo much bigger than the original can't add detail, so enlarged photos look softer."},
        {"q": "How do I resize without stretching the photo?", "a": "Keep 'Keep proportions' switched on. The photo then fits inside the width and height you typed, and the other side is worked out automatically."},
        {"q": "Can I resize many photos at once?", "a": "Yes. Choose or drop several photos and each one is resized with the same settings, with its own download button."},
        {"q": "Are my photos uploaded?", "a": "No. They're resized in your browser on your own device and never sent to any server."},
     ])

tool(slug="crop-image", tool="crop", opt={}, kw="crop image", also=["crop photo online", "crop image to square", "crop picture", "crop image 4:5"],
     title="Crop image online: square, 4:5, 16:9 or free, private", nav="Crop image",
     desc="Crop a photo to square, 4:5, 16:9, 9:16 or any shape. Free, works on your phone with touch, and your photo is never uploaded anywhere.",
     summary="Crop a photo to square, 4:5, 16:9 or any shape you draw.",
     h1="Crop image", lead="Cut a photo down to the part that matters, freehand or to an exact shape for Instagram, YouTube, WhatsApp or a profile picture.",
     answer="To crop an image, choose it above, pick a shape (or Free), drag the box over the part you want to keep and tap Download cropped photo. The crop is saved at full resolution, and the photo never leaves your device.",
     body=f"""<h2>How to crop a photo</h2>
<ol>
<li>Choose a photo above.</li>
<li>Pick a shape: <strong>1:1</strong> for square, <strong>4:5</strong> for Instagram portrait, <strong>16:9</strong> for YouTube and widescreen, <strong>9:16</strong> for stories and status, or <strong>Free</strong>.</li>
<li>Drag inside the box to move it, drag a corner to resize it, or drag anywhere else to draw a new box.</li>
<li>Tap <strong>Download cropped photo</strong>.</li>
</ol>
<h2>Which shape to use</h2>
<ul>
<li><strong>1:1 square:</strong> profile pictures, WhatsApp display photo, marketplace listings.</li>
<li><strong>4:5:</strong> the tallest photo Instagram shows in the feed.</li>
<li><strong>9:16:</strong> stories, Reels, Shorts and WhatsApp status.</li>
<li><strong>16:9:</strong> YouTube thumbnails, slides and TV screens.</li>
<li><strong>3:2 and 4:3:</strong> prints and most camera photos.</li>
</ul>
{{{{cta}}}}
{PRIVATE}
<h2>Crop before you share</h2>
<p>Cropping is also a privacy habit. Before posting a photo, check the edges for things you didn't mean to share: a letter with your address, a screen, a house number, a car plate or a face in the background. Crop them out, or use <a href="{{{{root}}}}tools/blur-face">blur faces</a> when they're in the middle. Then <a href="{{{{root}}}}tools/remove-photo-location">remove the location</a> hidden inside the file.</p>
{hide_line()}""",
     faq=[
        {"q": "Does cropping lower the photo quality?", "a": "No. The cropped area is saved at the photo's full resolution. Only the parts outside the box are removed."},
        {"q": "How do I crop a photo to a square?", "a": "Choose the 1:1 shape, then drag the box over the part you want and download. The result is a perfect square at full resolution."},
        {"q": "Does it work with touch on a phone?", "a": "Yes. Drag with your finger to move the box, drag a corner to resize it, and drag elsewhere to start a new box."},
        {"q": "Is my photo uploaded?", "a": "No. It's cropped in your browser on your own device and never sent to a server."},
     ])

# ---------------------------------------------------------------- passport
tool(slug="passport-photo-maker", tool="passport", opt={"country": "us"}, kw="passport photo maker",
     also=["passport size photo online", "passport photo 35x45", "2x2 photo maker", "passport photo print sheet 4x6"],
     title="Passport photo maker: free 2×2 and 35×45 mm photos", nav="Passport photo maker",
     desc="Make a passport-size photo from your own picture: US 2×2 in, 35×45 mm and more, plus a 4×6 print sheet. Free, and your photo is never uploaded.",
     summary="Crop a photo to passport size and get a 4×6 print sheet.",
     h1="Passport photo maker", lead="Turn a photo taken against a plain wall into a correctly sized passport photo, then print a sheet of copies at any photo shop for the price of one 4×6 print.",
     answer="To make a passport photo, take a well-lit picture against a plain light wall, choose it above, pick your country's size and fit the face in the oval. Download the single photo for online forms, or the 4×6 sheet to print several copies cheaply.",
     body=f"""<h2>How to make your passport photo</h2>
<ol>
<li><strong>Take the photo:</strong> stand about a metre from a plain white or light-grey wall, facing a window. Ask someone to take it at eye level. No glasses, neutral expression, mouth closed.</li>
<li>Choose it above and select your <strong>photo size</strong>.</li>
<li>Move and resize the box so the face sits inside the oval: chin at the bottom of the oval, top of the hair near the top, eyes about level with the middle.</li>
<li>Tap <strong>Download photo</strong> for online applications, or <strong>Download 4×6 in print sheet</strong> and print it as a normal 4×6 (10×15 cm) photo.</li>
</ol>
<h2>Sizes included</h2>
<div class="table-wrap"><table>
<thead><tr><th>Document</th><th>Size</th></tr></thead>
<tbody>
<tr><td>US passport and visa</td><td>2 × 2 in (51 × 51 mm)</td></tr>
<tr><td>India, UK, Schengen visa, EU passports, Australia, Japan, Philippines</td><td>35 × 45 mm</td></tr>
<tr><td>Canada passport, Brazil</td><td>50 × 70 mm</td></tr>
<tr><td>China visa</td><td>33 × 48 mm</td></tr>
<tr><td>Malaysia passport</td><td>35 × 50 mm</td></tr>
<tr><td>Indonesia</td><td>4 × 6 cm</td></tr>
</tbody></table></div>
<p>Rules change and some offices are strict about background colour and head size. Always check the official requirements for your application before you print.</p>
{{{{cta}}}}
{PRIVATE}
<p>That matters here: a passport photo is exactly the kind of image you don't want sitting on a stranger's server next to your name. When you're done, keep a copy of your ID somewhere private rather than in the open gallery; that's what <a href="{{{{root}}}}features/hidden-vaults">a vault</a> is for.</p>
<h2>Getting it accepted</h2>
<ul>
<li>Even light with no shadows on the face or the wall behind you.</li>
<li>Plain background; this tool doesn't change the background, so start with a light wall.</li>
<li>The photo must be recent, in focus and not edited beyond cropping.</li>
<li>Saved at 300 dpi, so the print shop prints it at the exact size.</li>
</ul>""",
     faq=[
        {"q": "How do I print the passport photos?", "a": "Download the 4×6 print sheet and order it as a standard 4×6 inch (10×15 cm) print at any photo shop, pharmacy kiosk or online print service. Then cut along the thin lines."},
        {"q": "Does it remove or change the background?", "a": "No. It crops and sizes your photo only. Take the picture against a plain white or light-grey wall so the background is already right."},
        {"q": "Can I use it for online passport and visa applications?", "a": "Yes. Use 'Download photo' for a single JPEG at the right proportions and 300 dpi. If the form also has a KB limit, run it through the compress tool afterwards."},
        {"q": "Is my photo uploaded or stored?", "a": "No. Your photo is processed in your browser on your own device and is never sent to any server."},
        {"q": "Is a 35 × 45 mm photo the same as passport size in India?", "a": "Yes, Indian passport applications use 35 × 45 mm photos with a white background. Choose the India option, and check the latest Passport Seva instructions before you apply."},
     ])

# ---------------------------------------------------------------- blur, brighten
tool(slug="blur-face", tool="blur", opt={}, kw="blur face in photo", also=["blur faces online", "pixelate face", "blur part of image", "censor photo"],
     title="Blur face in photo: blur or pixelate, free and private", nav="Blur faces",
     desc="Blur or pixelate faces, number plates and personal details in a photo before you share it. Free, works on your phone, and nothing is uploaded.",
     summary="Blur or pixelate faces, plates and details before sharing.",
     h1="Blur face in photo", lead="Hide faces, number plates, addresses or screens in a photo before you post it. Draw a box over each one, choose blur or pixelate, and download.",
     answer="To blur a face in a photo, choose it above and drag a box over each face. Pick Blur or Pixelate, set the strength, and tap Download. The blur is permanent in the saved copy, and the photo never leaves your device.",
     body=f"""<h2>How to blur faces and details</h2>
<ol>
<li>Choose a photo above.</li>
<li>Drag a box over each face, plate or detail you want hidden. Add as many as you need.</li>
<li>Choose <strong>Blur</strong> for a soft look or <strong>Pixelate</strong> for blocks, and raise the strength until nothing is recognisable.</li>
<li>Tap <strong>Download</strong>. Use <strong>Undo</strong> to remove the last box.</li>
</ol>
<h2>What to hide before you post</h2>
<ul>
<li>Faces of children, strangers and anyone who hasn't agreed to be posted.</li>
<li>Car number plates and house numbers.</li>
<li>Addresses on parcels, letters and documents.</li>
<li>Screens, ID cards, bank cards, boarding passes and tickets.</li>
<li>School logos and uniforms that reveal where your children are each day.</li>
</ul>
{{{{cta}}}}
{PRIVATE}
<h2>Make it strong enough</h2>
<p>Light blurring can sometimes be partly undone or still leave a face recognisable to people who know the person. Use a high strength, cover a little more than the face itself, and look at the result at full size before sharing. For anything truly sensitive, cropping the area out entirely is the safest option; use the <a href="{{{{root}}}}tools/crop-image">crop tool</a>. Remember that the file may also hold the place it was taken: <a href="{{{{root}}}}tools/remove-photo-location">remove the location</a> too.</p>
{hide_line()}""",
     faq=[
        {"q": "Does it find faces automatically?", "a": "No, you draw a box over each face yourself. That keeps it accurate, works with side-on and partly hidden faces, and means no face detection runs on your photos."},
        {"q": "Can a blur be reversed?", "a": "The saved copy is changed permanently, but weak blurring can leave a face recognisable. Use a high strength, cover the whole area, or crop the part out entirely for anything sensitive."},
        {"q": "Is pixelate or blur safer?", "a": "At high strength both hide a face well. Pixelate with large blocks is the easiest to judge by eye: if you can't make out features at full size, it's hidden."},
        {"q": "Is my photo uploaded?", "a": "No. The blurring happens in your browser on your own device, and the photo is never sent anywhere."},
     ])

tool(slug="brighten-photo", tool="brighten", opt={}, kw="brighten photo", also=["brighten dark photo", "increase brightness of image", "fix dark picture", "photo brightness editor"],
     title="Brighten photo online: fix dark pictures, free", nav="Brighten photo",
     desc="Fix dark or dull photos with one tap, or adjust brightness, contrast and colour yourself. Free, works on your phone, and photos are never uploaded.",
     summary="Fix dark or dull photos in one tap, or adjust them yourself.",
     h1="Brighten photo", lead="Rescue a photo taken indoors, at night or against the light. Auto fix lifts the shadows without washing out the bright parts, and you can fine-tune it by hand.",
     answer="To brighten a dark photo, choose it above; Auto fix runs straight away. Adjust Brightness, Contrast and Colour if you like, then tap Download for a full-resolution copy. Your photo stays on your device.",
     body=f"""<h2>How to brighten a photo</h2>
<ol>
<li>Choose a photo above. <strong>Auto fix</strong> is applied straight away.</li>
<li>Move <strong>Brightness</strong> to lift or darken the shadows, <strong>Contrast</strong> to add punch, and <strong>Colour</strong> to bring back faded colours.</li>
<li>Tap <strong>Download</strong>. The changes are applied to the full-size photo, not the preview.</li>
</ol>
<h2>Why this looks natural</h2>
<p>Simply adding brightness makes everything lighter, including skies and faces that were already bright, so they turn white and lose detail. This tool brightens with a curve instead: dark areas are lifted a lot, mid-tones a little, and highlights hardly at all. That's how phone editors and photo apps fix underexposed pictures, and it keeps the photo looking real.</p>
<h2>Getting the best result</h2>
<ul>
<li>Very dark night photos carry noise; brighten moderately and add a little contrast rather than pushing brightness to the top.</li>
<li>Photos taken against a window: brighten until the face looks right and accept that the window stays bright.</li>
<li>Old scanned prints: raise Colour a touch to undo fading.</li>
</ul>
{{{{cta}}}}
{PRIVATE}
{hide_line()}""",
     faq=[
        {"q": "Will brightening make my photo look grainy?", "a": "Dark photos already contain grain that you can't see until they're brightened. Lift brightness moderately and add a little contrast for the cleanest look."},
        {"q": "Does it save at full resolution?", "a": "Yes. You edit on a quick preview, and the download applies the same settings to the original full-size photo."},
        {"q": "What does Auto fix do?", "a": "It measures how dark the photo is overall and sets brightness, contrast and colour to bring it to a natural level. You can adjust each slider afterwards."},
        {"q": "Is my photo uploaded?", "a": "No. All editing happens in your browser on your own device and the photo is never sent to a server."},
     ])

# ---------------------------------------------------------------- pdf
tool(slug="jpg-to-pdf", tool="pdf", opt={"page": "a4"}, kw="jpg to pdf", also=["image to pdf", "photo to pdf", "convert images to pdf", "combine photos into one pdf"],
     title="JPG to PDF: combine photos into one PDF, free and private", nav="JPG to PDF",
     desc="Turn photos and scans into one PDF on your phone: A4, Letter or fit to image. Free, no watermark, and your files are never uploaded anywhere.",
     summary="Turn photos and scans into a single PDF, in the order you choose.",
     h1="JPG to PDF", lead="Combine photos of documents, receipts or notes into one tidy PDF. Put the pages in order, pick a page size, and download. No watermark and no sign-up.",
     answer="To convert JPG to PDF, choose your photos above, put them in order with the arrows, pick A4, Letter or Fit to image, and tap Create PDF. Each photo becomes one page. Everything happens on your device, so your documents are never uploaded.",
     body=f"""<h2>How to turn photos into a PDF</h2>
<ol>
<li>Choose or drop your photos. JPG, PNG, WebP and iPhone HEIC all work.</li>
<li>Use the ↑ and ↓ buttons to put the pages in order, and × to remove one.</li>
<li>Pick a <strong>page size</strong>: A4 for most of the world, Letter for the US and Canada, or <strong>Fit to image</strong> to make each page the shape of its photo.</li>
<li>Tap <strong>Create PDF</strong> and download it.</li>
</ol>
<h2>Good for</h2>
<ul>
<li>Sending signed forms and ID copies as one file.</li>
<li>Receipts and bills for expense claims.</li>
<li>Class notes and whiteboard photos.</li>
<li>Applications that only accept PDF uploads.</li>
</ul>
<p>Photos are placed on the page at their full proportions with a small margin, so nothing is cut off. Landscape photos get landscape pages automatically.</p>
{{{{cta}}}}
{PRIVATE}
<p>That matters most for documents: ID cards, bank letters and signed forms are exactly what you shouldn't hand to a random converter site. If you scan documents often, Sealcloak's <a href="{{{{root}}}}features/private-camera-and-scanner">document scanner</a> makes PDFs inside an encrypted vault, so the scans never touch your gallery.</p>
<h2>Keeping the PDF small</h2>
<p>Each page is saved as a good-quality JPEG, which keeps most PDFs small enough to email. If a portal has a strict size limit, run the photos through <a href="{{{{root}}}}tools/compress-image">compress image</a> first.</p>""",
     faq=[
        {"q": "Is there a limit on the number of pages?", "a": "No fixed limit. Very large numbers of high-resolution photos depend on your device's memory, but dozens of pages work fine on a normal phone."},
        {"q": "Will my PDF have a watermark?", "a": "No. There's no watermark, no sign-up and no limit. The PDF contains only your pages."},
        {"q": "Can I convert iPhone HEIC photos to PDF?", "a": "Yes. HEIC photos are converted on your device as they're added, then placed in the PDF like any other photo."},
        {"q": "Are my documents uploaded?", "a": "No. The PDF is created in your browser on your own device. Your photos and the PDF are never sent to any server."},
     ])

# ---------------------------------------------------------------- converters
def converter(slug, src, dst, mime, kw, also, why, faq_extra, accept="image/*,.heic,.heif"):
    tool(slug=slug, tool="convert", opt={"to": mime, "accept": accept}, kw=kw, also=also,
         title=f"{src} to {dst}: convert {'photos' if src == 'HEIC' else 'images'} free, no upload", nav=f"{src} to {dst}",
         desc=f"Convert {src} to {dst} in your browser, several files at once. Free, no sign-up, no watermark, and your photos are never uploaded to any server.",
         summary=f"Convert {src} files to {dst} on your device, in bulk.",
         h1=f"{src} to {dst} converter", lead=f"Turn {src} files into {dst} in a couple of taps. Drop in one file or a whole batch; each one converts on your device with its own download button.",
         answer=f"To convert {src} to {dst}, choose your {src} files above and tap Download next to each result. The conversion runs in your browser, so nothing is uploaded and there's no limit on how many files you convert.",
         body=f"""<h2>How to convert {src} to {dst}</h2>
<ol>
<li>Choose or drop your {src} files above. You can select many at once.</li>
<li>Each file converts straight away and shows its new size.</li>
<li>Tap <strong>Download</strong> next to each one.</li>
</ol>
<h2>Why convert {src} to {dst}</h2>
{why}
{{{{cta}}}}
{PRIVATE}
<h2>{src} vs {dst} at a glance</h2>
<div class="table-wrap"><table>
<thead><tr><th></th><th>JPG</th><th>PNG</th><th>WebP</th><th>HEIC</th></tr></thead>
<tbody>
<tr><td>Best for</td><td>Photos</td><td>Screenshots, logos, text</td><td>Websites</td><td>iPhone camera</td></tr>
<tr><td>Transparency</td><td>No</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>File size</td><td>Small</td><td>Large</td><td>Smallest</td><td>Small</td></tr>
<tr><td>Opens everywhere</td><td>Yes</td><td>Yes</td><td>Most apps</td><td>Often not</td></tr>
</tbody></table></div>
<p>Need a smaller file as well? Use <a href="{{{{root}}}}tools/compress-image">compress image</a> after converting.</p>
{hide_line()}""",
         faq=[
            {"q": f"Will converting {src} to {dst} lose quality?", "a": ("PNG is lossless, so the result keeps every pixel of the decoded image. " if dst == "PNG" else f"{dst} uses high-quality compression (92%), so the difference is invisible in normal viewing. ") + "Converting can't add back detail that the original file didn't have."},
            {"q": "Can I convert many files at once?", "a": "Yes. Choose or drop as many files as you like. Each converts on your device and gets its own download button."},
            {"q": "Does it work on my phone?", "a": "Yes. It works in Chrome, Samsung Internet, Firefox and Safari on Android, iPhone, tablets and computers."},
            {"q": "Are my files uploaded?", "a": "No. The conversion happens in your browser on your own device, and your files are never sent to any server."},
         ] + faq_extra)

converter("heic-to-jpg", "HEIC", "JPG", "image/jpeg", "heic to jpg", ["convert heic to jpg", "heic to jpeg", "open heic on android", "iphone photo to jpg"],
    "<p>iPhones save photos as HEIC by default. It's an efficient format, but many Android phones, Windows PCs, websites and forms can't open it. When an iPhone user sends you photos as files, or you copy them from an old iPhone, converting to JPG makes them open everywhere.</p><p>HEIC photos are decoded on your device by a small open-source decoder that this page loads, so the photo itself still never leaves your phone.</p>",
    [{"q": "Why can't my Android phone open HEIC photos?", "a": "Some Android phones and many apps don't support HEIC, the format iPhones use by default. Converting to JPG makes the photos open in any gallery, app or website."},
     {"q": "How do I stop my iPhone saving HEIC?", "a": "On the iPhone, open Settings, then Camera, then Formats, and choose Most Compatible. New photos are then saved as JPG."}])
converter("webp-to-jpg", "WebP", "JPG", "image/jpeg", "webp to jpg", ["convert webp to jpg", "webp to jpeg", "save webp as jpg", "open webp file"],
    "<p>Websites use WebP because it's small, so images you save from the web often end up as .webp files. Some apps, printers, older editors and upload forms don't accept WebP. JPG works everywhere. Transparent areas become white, since JPG has no transparency; use <a href=\"{{root}}tools/webp-to-png\">WebP to PNG</a> if you need to keep it.</p>",
    [{"q": "Why do images I save from websites end up as WebP?", "a": "Many websites serve WebP because it loads faster. Your browser saves it in that format, even if the page looked like it showed a normal JPG."}])
converter("webp-to-png", "WebP", "PNG", "image/png", "webp to png", ["convert webp to png", "webp to png transparent", "save webp as png"],
    "<p>PNG keeps transparency and sharp edges, which makes it the right choice for logos, stickers, icons and screenshots saved from websites as WebP. It's also accepted by every editor and design app. PNG files are larger than WebP, so for ordinary photos <a href=\"{{root}}tools/webp-to-jpg\">WebP to JPG</a> gives a smaller file.</p>",
    [{"q": "Does WebP to PNG keep transparency?", "a": "Yes. Transparent areas in the WebP stay transparent in the PNG, so logos and stickers keep their clean edges."}])
converter("png-to-jpg", "PNG", "JPG", "image/jpeg", "png to jpg", ["convert png to jpg", "png to jpeg", "reduce png size"],
    "<p>PNG files can be very large, especially screenshots and photos saved as PNG. Converting to JPG usually makes them several times smaller, which helps with email, forms that ask for JPG, and storage. Transparent areas become white, because JPG has no transparency.</p>",
    [{"q": "Why is my PNG so much bigger than a JPG?", "a": "PNG stores every pixel exactly, which suits text and graphics but makes photos very large. JPG is designed for photos and is usually several times smaller."}])
converter("jpg-to-png", "JPG", "PNG", "image/png", "jpg to png", ["convert jpg to png", "jpeg to png", "image to png"],
    "<p>Some apps, design tools and upload forms only accept PNG. PNG is also handy when you'll edit an image several times, because it doesn't lose quality each time it's saved. Note that converting won't make the background transparent by itself; it only changes the format. The PNG is usually larger than the JPG.</p>",
    [{"q": "Will converting JPG to PNG make the background transparent?", "a": "No. Converting only changes the file format. The background stays as it is in the photo; removing it needs a separate background remover."}])
converter("png-to-webp", "PNG", "WebP", "image/webp", "png to webp", ["convert png to webp", "jpg to webp", "image to webp"],
    "<p>WebP files are much smaller than PNG and JPG at the same visual quality, so websites load faster and use less data. Every modern browser shows WebP. Use it for website images, blogs and online shops. For sending photos to people, JPG is still the safest choice because every app opens it.</p>",
    [{"q": "Do all browsers support WebP?", "a": "Yes. Chrome, Safari, Firefox, Edge and Samsung Internet all display WebP, so it's safe to use on websites."}])

# ---------------------------------------------------------------- qr
QR_BODY = lambda extra: f"""{extra}
<h2>Make it scan reliably</h2>
<ul>
<li><strong>Keep strong contrast:</strong> a dark code on a light background. Light codes on dark backgrounds don't scan on every phone.</li>
<li><strong>Leave the white border</strong> around the code; scanners need it.</li>
<li><strong>Print it big enough:</strong> at least 2 × 2 cm, and bigger for posters read from a distance.</li>
<li><strong>Use higher error correction</strong> if the code may get scratched, folded or partly covered.</li>
<li><strong>Test it</strong> with your phone camera before printing hundreds.</li>
</ul>
{{{{cta}}}}
<h2>Private by design</h2><p>The code is generated inside this browser tab using a small open-source library. What you type, including Wi-Fi passwords, is never sent to a server, and there is no tracking. The code is static: it contains your text directly, so it never expires and doesn't depend on any website staying online.</p>
<h2>SVG or PNG?</h2>
<p>PNG is an image that works everywhere: messages, documents and social media. SVG is a vector file that stays perfectly sharp at any size, which is what print shops and designers prefer for posters, menus and packaging.</p>
<p>Codes that open links are only as safe as the link. Be careful scanning codes from strangers; our guide to <a href="{{{{root}}}}guides/how-to-hide-photos-on-android">keeping photos private</a> and <a href="{{{{root}}}}features/encryption">how encryption protects your files</a> cover the basics of staying in control of your data.</p>"""

tool(slug="qr-code-generator", tool="qr", opt={"type": "text"}, kw="qr code generator", also=["free qr code generator", "create qr code", "qr code for link", "qr code maker no sign up"],
     title="QR code generator: free, no sign-up, codes never expire", nav="QR code generator",
     desc="Make QR codes for links, text, Wi-Fi, email, phone and SMS. Free, no sign-up, download PNG or SVG, and the codes never expire.",
     summary="QR codes for links, Wi-Fi, email and more. PNG or SVG, never expires.",
     h1="QR code generator", lead="Create a QR code for a link, text, Wi-Fi network, email, phone number or SMS. Choose the colours and size, and download a PNG or SVG that works forever.",
     answer="To create a QR code, pick the type above, type your link or details, and download it as PNG or SVG. The code is made in your browser, has no tracking and never expires, because it contains your information directly.",
     body=QR_BODY("""<h2>How to create a QR code</h2>
<ol>
<li>Choose a <strong>type</strong>: link or text, Wi-Fi, email, phone or SMS.</li>
<li>Fill in the details. The code updates as you type.</li>
<li>Pick a size and colours if you want, then <strong>Download PNG</strong> or <strong>Download SVG</strong>.</li>
</ol>
<p>For a guest Wi-Fi sign, see the <a href="{{root}}tools/wifi-qr-code">Wi-Fi QR code</a> page.</p>
<h2>Why codes made here never expire</h2>
<p>Many free QR sites create "dynamic" codes that point to their own short link, then switch them off unless you pay. Codes made here are static: the link or text is stored inside the code itself, so it works as long as the link it points to does.</p>"""),
     faq=[
        {"q": "Do these QR codes expire?", "a": "No. They're static codes that contain your link or text directly, with no redirect through another website, so they keep working indefinitely."},
        {"q": "Is the QR code generator really free?", "a": "Yes. There's no sign-up, no watermark, no scan limit and no paid tier for the codes. Download as many as you like."},
        {"q": "Can I change the link after printing?", "a": "No. A static code can't be edited after it's made. If the destination may change, point the code at a page you control and update that page instead."},
        {"q": "Is what I type sent anywhere?", "a": "No. The code is generated in your browser. Your text, links and Wi-Fi passwords are never sent to a server."},
        {"q": "Can I make a coloured QR code?", "a": "Yes. Pick any colour and background, but keep the code dark on a light background with strong contrast, or some phones won't scan it."},
     ])

tool(slug="wifi-qr-code", tool="qr", opt={"type": "wifi"}, kw="wifi qr code", also=["wifi qr code generator", "share wifi password qr", "qr code for wifi", "guest wifi qr code"],
     title="WiFi QR code generator: share Wi-Fi without the password", nav="Wi-Fi QR code",
     desc="Make a QR code that connects guests to your Wi-Fi with one scan. Free, works with Android and iPhone, and the password never leaves your device.",
     summary="One scan connects guests to your Wi-Fi. The password stays on your device.",
     h1="WiFi QR code generator", lead="Let guests join your Wi-Fi by pointing their camera at a code, with no reading out long passwords. Print it for your home, office, shop or Airbnb.",
     answer="To make a Wi-Fi QR code, type your network name and password above, choose the security type (usually WPA), and download the code. Guests scan it with their phone camera and connect straight away. The password is never sent anywhere.",
     body=QR_BODY("""<h2>How to make your Wi-Fi QR code</h2>
<ol>
<li>Type the <strong>network name</strong> exactly as it appears in your Wi-Fi list, including capitals and spaces.</li>
<li>Type the <strong>password</strong> and choose the security: WPA covers WPA, WPA2 and WPA3, which is almost every router today.</li>
<li>Tick <strong>Hidden network</strong> only if your network doesn't appear in the Wi-Fi list.</li>
<li>Download it and test with your phone: open the camera, point it at the code and tap Connect.</li>
</ol>
<h2>Where to find your network name and password</h2>
<p>They're usually on a sticker on the router. On Android you can also open Settings, then Wi-Fi, tap your network and choose Share; on many phones this shows the password under a QR code after you unlock. On an iPhone, Settings, then Wi-Fi, then the ⓘ next to your network shows the password after Face ID.</p>
<h2>Use a guest network</h2>
<p>If your router supports it, create a separate guest network and put that on the code. Guests then can't see your other devices, and you can change the guest password at any time without reconnecting your own phones and TV.</p>"""),
     faq=[
        {"q": "Do Android phones and iPhones scan Wi-Fi QR codes?", "a": "Yes. Recent Android phones and iPhones read Wi-Fi codes straight from the camera app or Google Lens, then offer to join the network."},
        {"q": "Is it safe to type my Wi-Fi password here?", "a": "The code is generated in your browser and the password is never sent to a server. Anyone who scans the printed code can join, so use a guest network for public places."},
        {"q": "What if I change my Wi-Fi password?", "a": "The old code stops working, because the password is stored inside it. Make a new code with the new password and replace the printed one."},
        {"q": "Which security type should I choose?", "a": "Choose WPA for almost every modern router; it covers WPA, WPA2 and WPA3. Choose WEP only for very old equipment, and None for open networks."},
     ])

# ---------------------------------------------------------------- PDF and security tools (added 2026-11-09)
PDFPRIV = ("<h2>Private by design</h2><p>Most PDF websites upload your document to their servers to process it. This one doesn't. "
           "The PDF is opened, edited and saved inside this browser tab, on your own device, using open-source PDF libraries the page loads. "
           "Contracts, bank statements, ID scans and medical letters never leave your phone or computer. No sign-up, no watermark, no file limit.</p>")
def pdftool(**k):
    k.setdefault("nav", k["h1"]); tool(**k)

pdftool(slug="merge-pdf", tool="merge-pdf", opt={}, kw="merge pdf", also=["combine pdf files", "merge pdf online free", "join pdf", "merge pdf without uploading"],
  title="Merge PDF: combine PDF files free, without uploading", h1="Merge PDF",
  desc="Combine several PDF files into one, in the order you choose. Free, no sign-up or watermark, and your documents are merged on your device, never uploaded.",
  summary="Combine PDFs into one file, in your order.",
  lead="Join several PDFs into a single document: statements, scans, forms and attachments. Put them in order, merge, done. Nothing is uploaded.",
  answer="To merge PDF files, choose two or more PDFs above, use the arrows to set the order, and tap Merge PDFs. You get one PDF with every page, in that order. The merge happens on your device, so your documents are never uploaded.",
  body="""<h2>How to merge PDFs</h2>
<ol><li>Choose or drop two or more PDF files.</li><li>Use ↑ and ↓ to put them in order, and × to remove one.</li><li>Tap <strong>Merge PDFs</strong> and download <em>merged.pdf</em>.</li></ol>
<h2>Good to know</h2>
<ul><li>Pages keep their original size, orientation and quality; nothing is re-compressed.</li>
<li>Password-protected PDFs can't be merged until the password is removed in the app that created them.</li>
<li>To merge photos rather than PDFs, use <a href="{{root}}tools/jpg-to-pdf">JPG to PDF</a>. To drop pages first, use <a href="{{root}}tools/delete-pdf-pages">delete PDF pages</a>.</li></ul>
{{cta}}
""" + PDFPRIV + """<p>Merged documents often contain personal details. Keep them in an encrypted place afterwards; Sealcloak's <a href="{{root}}features/encryption">vault</a> keeps PDFs out of your Downloads folder and cloud.</p>""",
  faq=[{"q": "Is it safe to merge PDFs here?", "a": "Yes. The PDFs are merged in your browser on your own device and never sent to a server, so nobody else can see or keep them."},
       {"q": "Is there a limit on files or pages?", "a": "No fixed limit. Very large documents depend on your device's memory, but dozens of files and hundreds of pages work on a normal computer or phone."},
       {"q": "Will merging reduce quality?", "a": "No. Pages are copied as they are, so text, images and links stay exactly the same as in the original files."},
       {"q": "Can I merge PDFs on my phone?", "a": "Yes. It works in Chrome, Samsung Internet, Firefox and Safari on Android and iPhone."}])

pdftool(slug="split-pdf", tool="split-pdf", opt={}, kw="split pdf", also=["extract pages from pdf", "split pdf into pages", "separate pdf pages", "split pdf online free"],
  title="Split PDF: extract pages or save each page, free and private", h1="Split PDF",
  desc="Extract the pages you need from a PDF, or save every page as its own file. Free, works on your phone, and the PDF is never uploaded anywhere.",
  summary="Extract pages, or save every page separately.",
  lead="Pull out just the pages you need, like one bank statement page or a single signed form, or split a PDF into separate one-page files.",
  answer="To split a PDF, choose it above, type the pages you want (for example 1-3, 5), choose whether to keep them in one PDF or save each page separately, and tap Split PDF. The PDF is split on your device and never uploaded.",
  body="""<h2>How to split a PDF</h2>
<ol><li>Choose the PDF. You'll see how many pages it has.</li><li>Type pages and ranges, such as <code>2</code>, <code>1-3, 7</code> or <code>5-</code> for page 5 to the end. Leave it blank for all pages.</li>
<li>Choose <strong>Selected pages in one PDF</strong> or <strong>Every page as its own PDF</strong>.</li><li>Tap <strong>Split PDF</strong> and download the results.</li></ol>
<h2>When it's useful</h2>
<ul><li>Sending only the relevant page of a long statement or contract.</li><li>Uploading a single page to a form that limits file size.</li>
<li>Sharing part of a document without exposing the rest of your personal details.</li></ul>
{{cta}}
""" + PDFPRIV + """<p>Need the opposite? <a href="{{root}}tools/merge-pdf">Merge PDFs</a> into one. Want pages as images instead? Try <a href="{{root}}tools/pdf-to-jpg">PDF to JPG</a>.</p>""",
  faq=[{"q": "How do I extract one page from a PDF?", "a": "Choose the PDF, type the page number in the Pages box, keep 'Selected pages in one PDF', and tap Split PDF. You get a PDF with just that page."},
       {"q": "Can I split every page into a separate file?", "a": "Yes. Choose 'Every page as its own PDF' and leave Pages blank. Each page becomes its own PDF with its own download button."},
       {"q": "Does splitting reduce quality?", "a": "No. Pages are copied unchanged, so text stays selectable and images keep their quality."},
       {"q": "Is my PDF uploaded?", "a": "No. Splitting happens in your browser on your own device, so the document never leaves it."}])

pdftool(slug="rotate-pdf", tool="rotate-pdf", opt={}, kw="rotate pdf", also=["rotate pdf pages", "rotate pdf and save", "rotate pdf online free", "fix upside down pdf"],
  title="Rotate PDF pages and save them permanently, free", h1="Rotate PDF",
  desc="Turn sideways or upside-down PDF pages the right way and save it permanently. Rotate all pages or just some. Free, private, no upload.",
  summary="Fix sideways and upside-down PDF pages for good.",
  lead="Scanned a page sideways, or got a PDF that opens upside down? Rotate all pages or just the wrong ones, and save the fix permanently.",
  answer="To rotate a PDF, choose it above, pick 90° clockwise, 180° or 90° anticlockwise, type the pages to turn (or leave blank for all), and tap Rotate PDF. The saved file stays rotated in every app. Nothing is uploaded.",
  body="""<h2>How to rotate pages</h2>
<ol><li>Choose the PDF.</li><li>Pick the rotation: 90° clockwise, 180° (upside down) or 90° anticlockwise.</li>
<li>Type the pages that need turning, like <code>2, 4-6</code>, or leave it blank to rotate every page.</li><li>Tap <strong>Rotate PDF</strong> and download.</li></ol>
<h2>Rotate in a viewer vs rotate the file</h2>
<p>Most PDF viewers can turn a page on screen, but the next person who opens the file sees it sideways again. Rotating here changes the page itself, so it opens the right way everywhere: email, print, upload portals and phones.</p>
<p>For multi-page scans where only some pages are wrong, rotate just those pages. If a whole scan is sideways, leave Pages blank.</p>
{{cta}}
""" + PDFPRIV + """<p>Scanning documents on your phone? Sealcloak's <a href="{{root}}features/private-camera-and-scanner">document scanner</a> makes PDFs inside an encrypted vault.</p>""",
  faq=[{"q": "How do I rotate a PDF and save it?", "a": "Choose the PDF above, pick the rotation and pages, tap Rotate PDF and download. The new file stays rotated in every app and when printed."},
       {"q": "Can I rotate only one page?", "a": "Yes. Type that page number in the Pages box. Other pages stay as they are."},
       {"q": "Does rotating change quality?", "a": "No. Only the page orientation changes; the content is untouched and text stays selectable."},
       {"q": "Is the PDF uploaded?", "a": "No. It's rotated in your browser on your own device and never sent anywhere."}])

pdftool(slug="delete-pdf-pages", tool="delete-pdf-pages", opt={}, kw="delete pages from pdf", also=["remove pages from pdf", "delete pdf pages online free", "remove blank page pdf"],
  title="Delete pages from a PDF: remove pages free, no upload", h1="Delete pages from a PDF",
  desc="Remove blank, duplicate or private pages from a PDF before you share it. Type the pages to delete and download. Free, and the PDF stays on your device.",
  summary="Remove unwanted or private pages before sharing.",
  lead="Drop blank scans, duplicate pages, or pages with details you don't want to share, and send a cleaner PDF.",
  answer="To delete pages from a PDF, choose it above, type the pages to remove (for example 2, 7-9), and tap Remove pages. You get a new PDF without them; the original isn't changed. Everything happens on your device.",
  body="""<h2>How to remove pages</h2>
<ol><li>Choose the PDF; you'll see its page count.</li><li>Type the pages to remove, such as <code>3</code> or <code>2, 7-9</code>.</li><li>Tap <strong>Remove pages</strong> and download the edited PDF.</li></ol>
<h2>Share only what's needed</h2>
<p>Documents often carry more than the recipient needs. A rental application rarely needs every page of a bank statement; a form might only need the signed page. Removing extra pages is a simple privacy habit: less information shared is less information that can leak, be forwarded or be misused.</p>
<p>To keep specific pages instead of deleting, use <a href="{{root}}tools/split-pdf">split PDF</a>.</p>
{{cta}}
""" + PDFPRIV + """<p>Before sharing, also <a href="{{root}}tools/remove-pdf-metadata">remove the PDF's hidden metadata</a>, such as author name and software.</p>""",
  faq=[{"q": "How do I delete a page from a PDF for free?", "a": "Choose the PDF above, type the page number in 'Pages to remove' and tap Remove pages. Download the new PDF without that page."},
       {"q": "Can I delete several pages at once?", "a": "Yes. Type pages and ranges separated by commas, such as 2, 5, 7-9."},
       {"q": "Is the original PDF changed?", "a": "No. You download a new copy without the removed pages; your original file stays as it was."},
       {"q": "Is my PDF uploaded?", "a": "No. Pages are removed in your browser on your own device, and the PDF never leaves it."}])

pdftool(slug="pdf-to-jpg", tool="pdf-to-jpg", opt={}, kw="pdf to jpg", also=["convert pdf to jpg", "pdf to image", "pdf to png", "save pdf page as image"],
  title="PDF to JPG: turn PDF pages into images, free and private", h1="PDF to JPG",
  desc="Convert each page of a PDF into a sharp JPG or PNG image, ready to share or upload. Free, no sign-up, and the PDF is converted on your device.",
  summary="Turn PDF pages into JPG or PNG images.",
  lead="Some forms and apps only accept images. Turn each page of a PDF into a high-quality JPG or PNG in a couple of taps.",
  answer="To convert a PDF to JPG, choose it above, pick the quality and JPG or PNG, and tap Convert to images. Each page becomes its own image with a download button. The conversion happens on your device, not on a server.",
  body="""<h2>How to convert</h2>
<ol><li>Choose the PDF.</li><li>Pick a quality: Standard for screens, High for most uses, Very high for printing or zooming.</li>
<li>Choose JPG (smaller) or PNG (sharpest text).</li><li>Tap <strong>Convert to images</strong> and download the pages you need.</li></ol>
<h2>Which format to choose</h2>
<ul><li><strong>JPG:</strong> smaller files, best for scans and photos, accepted everywhere.</li><li><strong>PNG:</strong> crisp text and lines, larger files.</li></ul>
<p>If a form needs a small file, run the image through <a href="{{root}}tools/compress-image">compress image</a> afterwards. To go the other way, use <a href="{{root}}tools/jpg-to-pdf">JPG to PDF</a>.</p>
{{cta}}
""" + PDFPRIV,
  faq=[{"q": "How do I convert a PDF to JPG for free?", "a": "Choose the PDF above, pick the quality and format, and tap Convert to images. Each page becomes a JPG you can download."},
       {"q": "Can I convert just one page?", "a": "Every page is converted, and each has its own download button, so download only the ones you need. Or split the PDF first."},
       {"q": "Why does the text look blurry?", "a": "Choose High or Very high quality, or PNG, for sharper text. Standard quality is sized for phone screens."},
       {"q": "Is my PDF uploaded?", "a": "No. Pages are rendered into images in your browser on your own device."}])

pdftool(slug="compress-pdf", tool="compress-pdf", opt={}, kw="compress pdf", also=["reduce pdf size", "compress pdf online free", "pdf compressor", "make pdf smaller for email"],
  title="Compress PDF: reduce PDF file size, free and without upload", h1="Compress PDF",
  desc="Shrink large PDFs, especially scans and photo-heavy files, so they fit email and upload limits. Free, works on your phone, and nothing is uploaded.",
  summary="Make scanned and photo-heavy PDFs much smaller.",
  lead="Scanned documents and photo-heavy PDFs can be enormous. Compress them so they fit email attachments and upload limits on forms and portals.",
  answer="To compress a PDF, choose it above, keep Recommended compression (or Strong for smaller files), and tap Compress PDF. You'll see the new size; if the PDF is already compact, the original is kept. Everything happens on your device.",
  body="""<h2>How it works</h2>
<p>The tool redraws each page as a well-compressed image and builds a new, smaller PDF. That's exactly what shrinks scans and photo-heavy documents the most, often by 50 to 90%. The trade-off is that text in the compressed copy can't be selected or searched, so keep the original for editing.</p>
<h2>Choose a level</h2>
<ul><li><strong>Recommended:</strong> good balance, readable on any screen and printable.</li><li><strong>Strong:</strong> smallest files, fine for viewing on screens.</li>
<li><strong>Light:</strong> sharper pages, smaller savings.</li></ul>
<h2>Steps</h2>
<ol><li>Choose the PDF.</li><li>Pick a compression level.</li><li>Tap <strong>Compress PDF</strong>, check the new size, and download.</li></ol>
{{cta}}
""" + PDFPRIV + """<p>If a portal needs a specific size, try Strong, or <a href="{{root}}tools/delete-pdf-pages">remove pages</a> you don't need first.</p>""",
  faq=[{"q": "How do I reduce a PDF's size for email?", "a": "Choose the PDF above and tap Compress PDF. Scans often shrink by more than half; if it's still too big, use Strong compression."},
       {"q": "Will compression make my PDF blurry?", "a": "Recommended keeps pages clear for reading and printing. Strong is softer but still readable on screen. Light keeps the most detail."},
       {"q": "Why can't I select text after compressing?", "a": "Pages are rebuilt as images to save the most space. Keep your original PDF if you need searchable or editable text."},
       {"q": "Is my PDF uploaded?", "a": "No. It's compressed in your browser on your own device and never leaves it."}])

pdftool(slug="remove-pdf-metadata", tool="pdf-metadata", opt={}, kw="remove pdf metadata", also=["pdf metadata remover", "remove author from pdf", "pdf properties remove", "clean pdf metadata"],
  title="Remove PDF metadata: author, software and dates, free", h1="Remove PDF metadata",
  desc="See and remove the hidden details inside a PDF, such as author name, title, software and dates, before you share it. Free, and the PDF is never uploaded.",
  summary="Strip author, software and dates from a PDF.",
  lead="PDFs quietly carry details about who made them: your name as author, your organisation, the software used, and when it was created and edited. See them here, and remove them.",
  answer="To remove PDF metadata, choose the PDF above. You'll see its hidden properties, such as author, title and software. Tap Remove metadata to download a clean copy without them. The PDF is cleaned on your device and never uploaded.",
  body="""<h2>What a PDF can reveal</h2>
<ul><li><strong>Author:</strong> often your full name or your computer's user name.</li><li><strong>Title and subject:</strong> sometimes an old draft name or internal reference.</li>
<li><strong>Creator and producer:</strong> the app and version that made it.</li><li><strong>Created and modified dates</strong>, to the second.</li>
<li><strong>XMP metadata:</strong> a second, hidden copy of these details, plus editing history in some files.</li></ul>
<h2>When to clean a PDF</h2>
<ul><li>Sending a CV, a complaint or a tip where your name or employer shouldn't appear in the file.</li><li>Publishing documents online.</li>
<li>Sharing forms or letters drafted on a work computer.</li></ul>
<h2>Steps</h2>
<ol><li>Choose the PDF and review what it contains.</li><li>Tap <strong>Remove metadata</strong>.</li><li>Download the clean copy and share that one.</li></ol>
{{cta}}
""" + PDFPRIV + """<p>Photos carry hidden data too: <a href="{{root}}tools/remove-photo-location">remove the location from photos</a> before sharing them.</p>""",
  faq=[{"q": "How do I remove the author name from a PDF?", "a": "Choose the PDF above and tap Remove metadata. The clean copy has no author, title, subject, software or dates in its properties."},
       {"q": "Does removing metadata change the document?", "a": "No. Pages, text and images stay exactly the same; only the hidden properties are removed."},
       {"q": "Does it remove text I can see on the page?", "a": "No. Metadata is the hidden information about the file. Names printed on the page itself stay; remove those pages or edit the document if needed."},
       {"q": "Is my PDF uploaded?", "a": "No. It's cleaned in your browser on your own device and never sent to a server."}])

tool(slug="encrypt-text", tool="encrypt-text", opt={}, kw="encrypt text", also=["encrypt message with password", "text encryption online", "aes encrypt text", "decrypt text online"],
  title="Encrypt text with a password: AES-256, free and private", nav="Encrypt text", h1="Encrypt text with a password",
  desc="Turn a message into unreadable text with a password, and decrypt it again. AES-256-GCM in your browser. Free, and nothing you type is ever sent anywhere.",
  summary="Lock a message with a password, AES-256-GCM.",
  lead="Send a private note, an address or a code through any chat or email as scrambled text that only someone with the password can read.",
  answer="To encrypt text, type your message and a password above and tap Encrypt. Copy the result, which starts with sc1., and send it anywhere. The recipient pastes it here with the same password and taps Decrypt. Encryption uses AES-256-GCM in your browser.",
  body="""<h2>How to use it</h2>
<ol><li>Type or paste your message.</li><li>Choose a strong password; a <a href="{{root}}tools/password-generator">random passphrase</a> is easy to share by phone.</li>
<li>Tap <strong>Encrypt</strong> and copy the result.</li><li>Send it by chat or email, and share the password a different way.</li><li>To read it, paste the encrypted text here, type the password and tap <strong>Decrypt</strong>.</li></ol>
<h2>How secure is it?</h2>
<p>Your password is stretched into a key with PBKDF2-SHA256 over 600,000 rounds and a random salt, and the message is encrypted with AES-256-GCM, which also detects any change to the encrypted text. With a strong password, the message can't realistically be read without it. A weak password is the main risk, so check it with the <a href="{{root}}tools/password-strength-checker">password strength checker</a>.</p>
{{cta}}
<h2>Private by design</h2><p>Everything happens in this browser tab using your browser's built-in Web Crypto. Your message and password are never sent to a server or stored. For files instead of text, use <a href="{{root}}tools/encrypt-file">encrypt a file</a>.</p>""",
  faq=[{"q": "Is it safe to encrypt text online?", "a": "Here, yes: the text is encrypted in your browser and never sent anywhere. Be careful with sites that process your text on their servers."},
       {"q": "What encryption does it use?", "a": "AES-256-GCM, with the key derived from your password using PBKDF2-SHA256 and 600,000 iterations with a random salt."},
       {"q": "What if I forget the password?", "a": "The message can't be decrypted. There's no reset or backdoor, which is what keeps it private."},
       {"q": "Can the recipient decrypt it on their phone?", "a": "Yes. They open this page in any modern browser, paste the text, type the password and tap Decrypt."}])

tool(slug="password-strength-checker", tool="password-strength", opt={}, kw="password strength checker", also=["how strong is my password", "password checker", "test password strength", "how long to crack my password"],
  title="Password strength checker: how long to crack your password?", nav="Password strength checker", h1="Password strength checker",
  desc="See how strong a password really is, how long it could take to crack, and what makes it weak. Checked in your browser; the password is never sent anywhere.",
  summary="See how long a password would take to crack.",
  lead="Type a password to see how strong it really is, roughly how long it would take to crack, and which common patterns make it weaker than it looks.",
  answer="Type a password above to see its strength, an estimate of how long it would take to crack, and specific weaknesses such as common words, sequences or years. The check runs in your browser, and the password is never sent or stored.",
  body="""<h2>What the checker looks at</h2>
<ul><li><strong>Length</strong> and the <strong>variety</strong> of characters: lowercase, capitals, digits and symbols.</li>
<li><strong>Common passwords</strong>, including ones with a number or symbol tacked on.</li><li><strong>Sequences</strong> like 1234, abcd and qwerty, and <strong>repeated characters</strong>.</li>
<li><strong>Years and dates</strong>, which attackers try early.</li><li><strong>Predictable patterns</strong>, like a capital letter, a word, then numbers.</li></ul>
<h2>Reading the result</h2>
<p>The estimate assumes two attacks. "From a stolen password database" means an attacker with fast hardware guessing offline, the worst case after a data breach. "Guessing online" means trying passwords on a login page, which is far slower because sites limit attempts. Strong passwords hold up against both.</p>
{{cta}}
<h2>Private by design</h2><p>The checker runs entirely in your browser. What you type isn't sent anywhere, saved or logged. Even so, it's best practice to check a password that's similar to yours rather than your real one. Need a better one? Use the <a href="{{root}}tools/password-generator">password generator</a>, and see <a href="{{root}}tools/password-generator/how-long-should-a-password-be">how long a password should be</a>.</p>""",
  faq=[{"q": "Is it safe to type my password into a strength checker?", "a": "This checker runs in your browser and never sends what you type anywhere. Still, testing a similar password rather than your real one is a good habit."},
       {"q": "What makes a password strong?", "a": "Length and randomness. 16 or more random characters, or a passphrase of five or more random words, is strong. Avoid words, names, dates and patterns."},
       {"q": "How long does it take to crack an 8-character password?", "a": "If it's a common word with a number, almost instantly. Even 8 random characters can fall in hours to days against fast offline cracking."},
       {"q": "Why is my password weak even with symbols?", "a": "Symbols in predictable places, like a capital first letter and ! at the end, don't add much. Attackers try those patterns first."}])

tool(slug="hash-generator", tool="hash", opt={}, kw="sha-256 checksum", also=["hash generator", "md5 checksum", "verify file checksum", "sha256 hash generator online"],
  title="SHA-256 and MD5 checksum: hash text or files, free", nav="Hash and checksum", h1="SHA-256 and MD5 checksum generator",
  desc="Get the SHA-256, SHA-1, SHA-512 and MD5 checksum of any file or text, and verify a download matches. Runs in your browser; files are never uploaded.",
  summary="Checksums for files and text, and verify downloads.",
  lead="Check that a download hasn't been changed or corrupted, or get the fingerprint of any file or text. Paste an expected checksum to compare automatically.",
  answer="To get a file's checksum, drop it above; you'll see its MD5, SHA-1, SHA-256 and SHA-512 hashes. To verify a download, paste the checksum the publisher gives into the compare box; a green match means the file is identical. Nothing is uploaded.",
  body="""<h2>How to verify a download</h2>
<ol><li>Find the checksum on the publisher's download page, usually labelled SHA-256.</li><li>Paste it into <strong>Compare with</strong>.</li>
<li>Drop the downloaded file above.</li><li>A ✓ match means the file is exactly what the publisher released.</li></ol>
<h2>Which algorithm?</h2>
<div class="table-wrap"><table><thead><tr><th>Algorithm</th><th>Use today</th></tr></thead><tbody>
<tr><td>SHA-256</td><td>The standard choice for verifying downloads</td></tr><tr><td>SHA-512</td><td>Also secure; longer output</td></tr>
<tr><td>SHA-1</td><td>Legacy; not safe against deliberate tampering</td></tr><tr><td>MD5</td><td>Legacy; fine for spotting accidental corruption only</td></tr></tbody></table></div>
{{cta}}
<h2>Private by design</h2><p>Files and text are hashed in your browser with its built-in Web Crypto (and a small MD5 routine), so even large files never leave your device. Encryption is a different thing from hashing: to lock a file with a password, use <a href="{{root}}tools/encrypt-file">encrypt a file</a>.</p>""",
  faq=[{"q": "How do I check a file's SHA-256 checksum?", "a": "Drop the file above and read the SHA-256 line. To verify it, paste the expected checksum into the compare box and look for the match message."},
       {"q": "What's the difference between hashing and encryption?", "a": "A hash is a one-way fingerprint that can't be turned back into the file. Encryption scrambles data so it can be unlocked with a key or password."},
       {"q": "Is MD5 still safe?", "a": "Not for security: it can be deliberately forged. It's still fine for spotting accidental corruption. Use SHA-256 to verify downloads."},
       {"q": "Is my file uploaded?", "a": "No. It's hashed in your browser on your own device, however large it is."}])

pdftool(slug="protect-pdf", tool="protect-pdf", opt={}, kw="password protect pdf", also=["add password to pdf", "lock pdf with password", "encrypt pdf", "protect pdf online free"],
  title="Password protect a PDF: AES-256, free, nothing uploaded", h1="Password protect a PDF",
  desc="Add a password to a PDF so it asks for it in any reader. AES-256 encryption, optional print and copy limits. Free, and the PDF never leaves your device.",
  summary="Add a password that any PDF reader will ask for.",
  lead="Lock a PDF with a password before you email or share it. The result is a normal PDF: Adobe, Chrome, phones and every PDF reader ask for the password before showing anything.",
  answer="To password protect a PDF, choose it above, type and confirm a password, choose whether printing, copying and editing are allowed, and tap Protect PDF. The file is encrypted with AES-256 on your device and opens in any PDF reader once the password is entered.",
  body="""<h2>How to protect a PDF</h2>
<ol><li>Choose the PDF.</li><li>Type a strong password twice. A <a href="{{root}}tools/password-generator">random passphrase</a> is easy to read out over the phone.</li>
<li>Choose whether the recipient may print, copy text or edit.</li><li>Tap <strong>Protect PDF</strong> and download the protected copy.</li>
<li>Send the PDF, and share the password a different way, never in the same email.</li></ol>
<h2>How strong is it?</h2>
<p>The PDF is encrypted with AES-256, the strongest standard PDF encryption, using qpdf, a widely used open-source PDF tool that runs here in your browser. Without the password, the pages can't be read. As always, the password is the weak point: use 12 or more characters, and nothing guessable like a date of birth.</p>
<h2>Protect PDF vs encrypt a file</h2>
<p>A protected PDF opens in any PDF reader, which is what most people need. Our <a href="{{root}}tools/encrypt-file">encrypt a file</a> tool works for any file type, and the recipient decrypts it on our page. Print and copy limits are honoured by most readers, but they're restrictions, not encryption; the password is what protects the content.</p>
{{cta}}
""" + PDFPRIV + """<p>Already have a protected PDF you can open but want without the password? Use <a href="{{root}}tools/unlock-pdf">unlock PDF</a>.</p>""",
  faq=[{"q": "How do I add a password to a PDF for free?", "a": "Choose the PDF above, type and confirm a password, and tap Protect PDF. Download the protected copy; any PDF reader will ask for the password."},
       {"q": "Will the recipient need special software?", "a": "No. The protected file is a normal PDF. Adobe Reader, browsers, phones and other PDF readers ask for the password and then open it."},
       {"q": "What encryption is used?", "a": "AES-256, the strongest standard encryption for PDFs, applied by qpdf running in your browser."},
       {"q": "Is my PDF uploaded?", "a": "No. It's encrypted in your browser on your own device, and the password is never sent anywhere."},
       {"q": "What if I forget the password?", "a": "Keep the original unprotected file somewhere safe. A strongly protected PDF can't be opened without its password, by us or anyone."}])

pdftool(slug="unlock-pdf", tool="unlock-pdf", opt={}, kw="remove password from pdf", also=["unlock pdf", "remove pdf password", "pdf password remover", "unlock bank statement pdf"],
  title="Remove password from a PDF you can open: free, private", h1="Remove password from a PDF",
  desc="Tired of typing a password every time you open a statement? Remove it from a PDF you know the password for. Free, and the PDF never leaves your device.",
  summary="Save a copy without the password, when you know it.",
  lead="Bank statements, payslips and bills often arrive locked with your date of birth or account number. If you know the password, save a copy that opens without it.",
  answer="To remove a password from a PDF, choose it above, type its current password and tap Unlock PDF. You get a copy without the password. This only works when you know the password; it doesn't crack or guess passwords. Nothing is uploaded.",
  body="""<h2>How to unlock a PDF</h2>
<ol><li>Choose the protected PDF.</li><li>Type the password you normally use to open it.</li><li>Tap <strong>Unlock PDF</strong> and download the unlocked copy.</li></ol>
<h2>Common statement passwords</h2>
<p>Banks, card issuers and payroll systems often build the password from your details, for example part of your name with your date of birth, or the last digits of your account or customer ID. The email that came with the statement usually explains the format. This tool needs that password; it doesn't guess or break passwords.</p>
<h2>Keep unlocked copies safe</h2>
<p>A statement without a password is easier to read, for you and for anyone who finds it. Don't leave unlocked copies in Downloads, email or a shared cloud folder. Keep them in an encrypted vault such as Sealcloak, which stores documents <a href="{{root}}features/encryption">encrypted on your phone</a> behind your own pattern, or add a new password with <a href="{{root}}tools/protect-pdf">protect PDF</a>.</p>
{{cta}}
""" + PDFPRIV,
  faq=[{"q": "Can I unlock a PDF without the password?", "a": "No. This tool removes a password you already know. It doesn't crack or guess passwords, and you should only unlock documents you're entitled to open."},
       {"q": "How do I remove the password from my bank statement PDF?", "a": "Choose the statement above, type the password you use to open it, often based on your name, date of birth or account number, and tap Unlock PDF."},
       {"q": "Does unlocking change the document?", "a": "No. The pages are identical; only the password protection and its restrictions are removed."},
       {"q": "Is my PDF or password uploaded?", "a": "No. The PDF is unlocked in your browser on your own device, and neither the file nor the password is sent anywhere."}])

# ---------------------------------------------------------------- write
# ---------------------------------------------------------------- security
tool(slug="password-generator", tool="password", opt={"kind": "chars"}, kw="password generator",
     also=["strong password generator", "random password generator", "passphrase generator", "secure password generator"],
     title="Password generator: strong, random and private", nav="Password generator",
     desc="Create strong random passwords or easy-to-type passphrases. Generated on your device with secure randomness, never sent or stored anywhere.",
     summary="Strong random passwords and passphrases, made on your device.",
     h1="Strong password generator", lead="Make a password nobody can guess: random characters for a password manager, or a passphrase of real words you can actually remember and type.",
     answer="To create a strong password, use the generator above: 20 random characters, or a passphrase of 5 or more random words. It uses your device's secure random number generator, and the password is never sent anywhere. Use a different password for every account.",
     body=f"""<h2>How to use it</h2>
<ol>
<li>Choose <strong>Random characters</strong> for passwords you'll store in a password manager, or <strong>Passphrase</strong> for ones you need to remember.</li>
<li>Set the length. 16 to 20 characters, or 5 to 6 words, is strong for almost everything.</li>
<li>Tap <strong>Copy</strong>, paste it into the sign-up form, and save it in your password manager.</li>
</ol>
<h2>What makes a password strong</h2>
<p>Strength comes from randomness, not from clever tricks. "P@ssw0rd2024" looks complex but is one of the first guesses attackers try, because people make the same substitutions. A password picked truly at random from a large set can't be guessed that way. The strength line under the password shows how many bits of randomness it has: every extra bit doubles the number of guesses needed.</p>
<div class="table-wrap"><table>
<thead><tr><th>Password</th><th>Randomness</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>8 random letters and digits</td><td>about 48 bits</td><td>Weak against offline cracking</td></tr>
<tr><td>4 random words</td><td>about 52 bits</td><td>Fair</td></tr>
<tr><td>5 random words</td><td>about 65 bits</td><td>Good for most accounts</td></tr>
<tr><td>16 random characters (all types)</td><td>about 100 bits</td><td>Very strong</td></tr>
<tr><td>20 random characters (all types)</td><td>about 130 bits</td><td>Very strong</td></tr>
</tbody></table></div>
<h2>Why passphrases work</h2>
<p>Passphrases like <em>velvet-orbit-canyon-plural-sprout</em> are picked at random from the EFF's list of 7,776 words, so each word adds almost 13 bits. They're far easier to type on a phone and remember than random symbols, which makes them ideal for the few passwords you can't keep in a manager: your phone, your computer and the password manager itself.</p>
{{{{cta}}}}
<h2>Private by design</h2>
<p>Passwords are generated inside this browser tab with <code>crypto.getRandomValues</code>, the same secure random source browsers use for encryption, and every character is equally likely. Nothing you generate is sent, logged or stored. Close the tab and it's gone.</p>
<p>The same idea runs through Sealcloak: its <a href="{{{{root}}}}features/recovery-phrase">9-word recovery phrase</a> is a random passphrase made on your phone, and your vault is <a href="{{{{root}}}}features/encryption">encrypted with AES-256-GCM</a> from a key only you hold.</p>
<h2>Good password habits</h2>
<ul>
<li>One password per account, so a leak from one site can't unlock the others.</li>
<li>Turn on two-step verification wherever it's offered.</li>
<li>Store passwords in a password manager, not in your photos, notes or chat history.</li>
<li>Change a password straight away if a site tells you it was breached.</li>
</ul>""",
     faq=[
        {"q": "Is this password generator safe to use?", "a": "Yes. Passwords are created in your browser with its secure random generator and never sent anywhere or stored. You can disconnect from the internet after the page loads and it still works."},
        {"q": "How long should my password be?", "a": "At least 16 random characters for accounts stored in a password manager, or a passphrase of 5 to 6 random words for passwords you need to remember."},
        {"q": "Are passphrases as secure as random characters?", "a": "A passphrase of 6 random words has about 78 bits of randomness, which is very strong, and it's much easier to type. What matters is that the words are chosen at random, not by you."},
        {"q": "Should I write my password down?", "a": "Keep it in a password manager rather than in a note or a screenshot. A photo of your passwords sitting in the gallery is one of the easiest things for someone to find."},
     ])

tool(slug="encrypt-file", tool="encrypt", opt={"drop": "Drop files here", "choose": "Choose files", "hint": "Any file type. Files never leave this device."},
     kw="encrypt file with password", also=["password protect file", "encrypt file online", "aes 256 file encryption", "lock file with password"],
     title="Encrypt file with password: AES-256, free and private", nav="Encrypt a file",
     desc="Password-protect any file with AES-256-GCM encryption before you send or store it. Free, runs in your browser, and the file is never uploaded.",
     summary="Lock any file with a password using AES-256-GCM, on your device.",
     h1="Encrypt a file with a password", lead="Lock any file (a PDF, photo, video or document) with a password before you email it, put it on a USB stick or store it in the cloud. Only someone with the password can open it.",
     answer="To encrypt a file with a password, type a strong password above, then choose the file. You get a .locked copy encrypted with AES-256-GCM. To open it again, come back to this page, type the same password and choose the .locked file. Nothing is uploaded.",
     body=f"""<h2>How to encrypt and decrypt a file</h2>
<ol>
<li>Type a strong password. A <a href="{{{{root}}}}tools/password-generator">random passphrase</a> is ideal.</li>
<li>Choose the file. You get a copy ending in <strong>.locked</strong>; the original isn't changed.</li>
<li>Send or store the .locked file. Share the password a different way, for example by phone call rather than in the same email.</li>
<li>To open it: on this page, type the same password and choose the .locked file. The original file comes back with its name.</li>
</ol>
<h2>How the encryption works</h2>
<p>Your password is stretched into a 256-bit key with PBKDF2-SHA256 over 600,000 rounds and a random salt, which makes guessing passwords slow. The file is then encrypted with AES-256-GCM, which also detects tampering: if a single byte of the .locked file is changed, it refuses to decrypt instead of giving you a corrupted file. Everything runs through your browser's built-in Web Crypto, on your device.</p>
<div class="table-wrap"><table>
<thead><tr><th>Part</th><th>What it does</th></tr></thead>
<tbody>
<tr><td>AES-256-GCM</td><td>Encrypts the file and detects any change to it</td></tr>
<tr><td>PBKDF2-SHA256, 600,000 rounds</td><td>Turns your password into a key and slows down guessing</td></tr>
<tr><td>Random salt and IV per file</td><td>The same file and password never produce the same output</td></tr>
</tbody></table></div>
{{{{cta}}}}
<h2>Private by design</h2>
<p>The file is read, encrypted and saved inside this browser tab. It's never sent to a server, and the password is never stored. That also means nobody can recover a forgotten password, including us, so keep it somewhere safe.</p>
<h2>For files on your phone</h2>
<p>This tool is for one-off files you send or store elsewhere. For photos, videos and documents you keep on your Android phone, Sealcloak does the same kind of protection automatically: every file is <a href="{{{{root}}}}features/encryption">encrypted with AES-256-GCM</a> as you add it, inside <a href="{{{{root}}}}features/hidden-vaults">vaults</a> that open with your own pattern, and it can make <a href="{{{{root}}}}features/secure-sharing">passphrase-locked packages</a> for sharing.</p>""",
     faq=[
        {"q": "How secure is the encryption?", "a": "It uses AES-256-GCM with a key derived from your password by PBKDF2-SHA256 over 600,000 rounds. With a strong password, the file can't realistically be opened without it. A weak password is the main risk."},
        {"q": "What happens if I forget the password?", "a": "The file can't be opened. The password isn't stored anywhere and there's no reset or backdoor, which is exactly what keeps the file private."},
        {"q": "How does the other person open the file?", "a": "They open this page, type the password and choose the .locked file. It decrypts in their browser and gives back the original file with its name."},
        {"q": "Is my file uploaded?", "a": "No. Encryption and decryption happen in your browser on your own device. The file and the password are never sent anywhere."},
        {"q": "Is there a file size limit?", "a": "The limit is your device's memory. Files of a few hundred megabytes work on most computers; very large videos may be too much for a phone browser."},
     ])

SKELETON = """<!--meta {meta} -->
<section class="panel">
  <div class="panel-inner wrap">
    <article class="article">
      <div class="meta"><a href="{{{{root}}}}tools/">Free tools</a> · Runs in your browser</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="tool" data-tool="{tool}" data-opt='{opt}'></div>
      <div class="answer">
        <div class="eyebrow">Quick answer</div>
        <p>{answer}</p>
      </div>
      <div class="prose">
{body}
        {{{{faq}}}}
      </div>
      {{{{related}}}}
    </article>
  </div>
</section>
<script src="{{{{root}}}}js/tools.js" defer></script>
"""

import re
for t in T:
    words = len(re.sub(r"<[^>]+>", " ", t["body"] + t["lead"] + t["answer"] + " ".join(f["q"] + f["a"] for f in t["faq"])).split())
    meta = {"title": t["title"], "navTitle": t["nav"], "description": t["desc"], "keyword": t["kw"], "alsoTargets": t["also"],
            "summary": t["summary"], "date": DATE, "readMins": max(2, round(words / 220)), "nav": "guides", "faq": t["faq"]}
    # How-to steps (from the page's first numbered list) and what the tool does, for HowTo and WebApplication rich results
    ol = re.search(r"<ol>([\s\S]*?)</ol>", t["body"])
    meta["steps"] = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", li)).strip() for li in re.findall(r"<li>([\s\S]*?)</li>", ol.group(1))] if ol else []
    meta["category"] = "SecurityApplication" if t["tool"] in ("password", "encrypt", "encrypt-text", "password-strength", "hash", "protect-pdf", "unlock-pdf") else "BusinessApplication" if "pdf" in t["tool"] else "DesignApplication" if t["tool"] in ("qr",) else "MultimediaApplication"
    meta["features"] = ["Runs entirely in your browser", "Files are never uploaded", "No sign-up", "No watermark", "Free"]
    html = SKELETON.format(meta=json.dumps(meta, indent=2, ensure_ascii=False), h1=t["h1"], lead=t["lead"], tool=t["tool"],
                           opt=json.dumps(t["opt"]), answer=t["answer"], body=t["body"])
    open(os.path.join(ROOT, t["slug"] + ".html"), "w").write(html)
    print(t["slug"], words)

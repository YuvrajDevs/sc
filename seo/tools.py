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
    meta["category"] = "SecurityApplication" if t["tool"] in ("password", "encrypt") else "DesignApplication" if t["tool"] in ("qr",) else "MultimediaApplication"
    meta["features"] = ["Runs entirely in your browser", "Files are never uploaded", "No sign-up", "No watermark", "Free"]
    html = SKELETON.format(meta=json.dumps(meta, indent=2, ensure_ascii=False), h1=t["h1"], lead=t["lead"], tool=t["tool"],
                           opt=json.dumps(t["opt"]), answer=t["answer"], body=t["body"])
    open(os.path.join(ROOT, t["slug"] + ".html"), "w").write(html)
    print(t["slug"], words)

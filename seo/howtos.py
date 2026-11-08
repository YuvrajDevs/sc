#!/usr/bin/env python3
"""Writes the how-to pages that sit under each tool: content/tools/<tool>/<slug>.html.
Each answers one specific search and embeds the working tool, so the reader can do it right there.
Re-run after editing; it overwrites the files."""
import json, os, re

ROOT = os.path.join(os.path.dirname(__file__), "..", "content", "tools")
DATE = "2026-11-08"
TOOLS = {  # parent slug: (tool kind, options, nav name)
    "compress-image": ("compress", {"targetKB": 200}, "Compress image"),
    "compress-image-to-50kb": ("compress", {"targetKB": 50}, "Compress image to 50 KB"),
    "resize-image": ("resize", {"w": 1080}, "Resize image"),
    "passport-photo-maker": ("passport", {"country": "us"}, "Passport photo maker"),
    "remove-photo-location": ("meta", {}, "Remove photo location"),
    "blur-face": ("blur", {}, "Blur faces"),
    "heic-to-jpg": ("convert", {"to": "image/jpeg"}, "HEIC to JPG"),
    "webp-to-png": ("convert", {"to": "image/png"}, "WebP to PNG"),
    "jpg-to-pdf": ("pdf", {"page": "a4"}, "JPG to PDF"),
    "wifi-qr-code": ("qr", {"type": "wifi"}, "Wi-Fi QR code"),
    "password-generator": ("password", {"kind": "words"}, "Password generator"),
    "encrypt-file": ("encrypt", {"drop": "Drop files here", "choose": "Choose files", "hint": "Any file type. Files never leave this device."}, "Encrypt a file"),
    "brighten-photo": ("brighten", {}, "Brighten photo"),
}
P = []
def page(parent, slug, **k): P.append(dict(parent=parent, slug=slug, **k))

# ---------------------------------------------------------------- compress
page("compress-image", "compress-photo-for-email", opt={"targetKB": 1000},
  kw="reduce photo size for email", also=["photo too large to email", "compress photos for email", "email attachment size limit"],
  title="Reduce photo size for email: send big photos without bouncing",
  desc="Photo too large to email? See the attachment limits for Gmail and Outlook, and shrink your photos to send in one email. Free, and nothing is uploaded.",
  summary="Shrink photos so they fit in one email.",
  h1="Reduce photo size for email", lead="Phone photos are often 3 to 8 MB each, so a handful can blow past an email's attachment limit. Shrink them here first and they'll send in one go, still looking sharp.",
  answer="To reduce a photo's size for email, choose it above with the target at 1000 KB (1 MB) and download the result. Five photos at 1 MB each fit comfortably under Gmail's 25 MB limit. The photos are compressed on your device and never uploaded.",
  body="""<h2>Attachment limits</h2>
<div class="table-wrap"><table><thead><tr><th>Email service</th><th>Attachment limit</th></tr></thead><tbody>
<tr><td>Gmail</td><td>25 MB per email</td></tr><tr><td>Outlook.com</td><td>20 MB per email</td></tr><tr><td>Yahoo Mail</td><td>25 MB per email</td></tr></tbody></table></div>
<p>The limit counts the whole email, and attachments grow by about a third when they're encoded for sending, so aim well below it. As a rule of thumb, photos of about 1 MB each look great on any screen and let you send a dozen or more at once.</p>
<h2>Picking the right size</h2>
<ul><li><strong>For viewing on a phone or computer:</strong> 500 KB to 1 MB per photo is plenty.</li>
<li><strong>For printing at 6 × 4 inches:</strong> keep at least 1600 pixels on the long side and about 1 to 2 MB.</li>
<li><strong>For a form or portal:</strong> use the exact limit it gives, for example <a href="{{root}}tools/compress-image-to-100kb">100 KB</a>.</li></ul>
{{cta}}
<h2>Why compress here rather than in an online converter</h2>
<p>Most compression websites upload your photos to their servers to process them. For holiday snaps that may not matter, but for ID scans, family photos or anything personal, it's an unnecessary copy on someone else's computer. This tool works inside your browser: the photo is never sent anywhere. Before sharing, you can also <a href="{{root}}tools/remove-photo-location">remove the hidden location</a> that phone photos carry.</p>""",
  faq=[{"q": "Why does my email say the attachment is too large?", "a": "Most email services limit attachments to 20 or 25 MB per email, and a few phone photos can exceed that. Compress them to about 1 MB each and they'll fit."},
       {"q": "Will compressed photos look worse?", "a": "At around 1 MB, photos look the same on phone and computer screens. The tool keeps the best quality that fits your target size."},
       {"q": "Can I compress several photos at once?", "a": "Yes. Choose or drop as many photos as you like; each gets compressed to the same target and has its own download button."},
       {"q": "Are my photos uploaded?", "a": "No. Compression happens in your browser on your own device, so your photos never leave it."}])

page("compress-image-to-50kb", "photo-signature-size-online-forms", opt={"targetKB": 50},
  kw="photo and signature size for online form", also=["photo size 20kb to 50kb", "signature size 10kb to 20kb", "exam form photo size"],
  title="Photo and signature size for online forms: get it right",
  desc="Common photo and signature size rules for exam, job and government forms, and how to make your files fit in seconds. Free, works on your phone, no upload.",
  summary="Make photos and signatures fit form size rules.",
  h1="Photo and signature size for online forms", lead="Online application forms are strict: a photo between 20 and 50 KB, a signature between 10 and 20 KB, exact dimensions, JPEG only. Here's how to get both files right on the first attempt, from your phone.",
  answer="Most online forms want a recent passport-style photo of about 20 to 50 KB and a signature of about 10 to 20 KB, both as JPEG. Crop each tightly, then compress it with the tool above; the target is set to 50 KB, and you can type 20 for a signature. Always check the exact rules in the form's notification.",
  body="""<h2>Typical requirements</h2>
<div class="table-wrap"><table><thead><tr><th>File</th><th>Usual size</th><th>Usual format</th></tr></thead><tbody>
<tr><td>Photograph</td><td>20 to 50 KB</td><td>JPEG, recent, light background</td></tr>
<tr><td>Signature</td><td>10 to 20 KB</td><td>JPEG, dark ink on white paper</td></tr>
<tr><td>Thumb impression (if asked)</td><td>10 to 20 KB</td><td>JPEG</td></tr></tbody></table></div>
<p>These are common ranges, not rules. Each exam or employer publishes its own, sometimes with pixel dimensions such as 200 × 230 for the photo and 140 × 60 for the signature. If pixel sizes are given, <a href="{{root}}tools/resize-image">resize</a> first, then compress.</p>
<h2>Step by step</h2>
<ol><li>Take the photo against a plain light wall in daylight, face centred, shoulders visible.</li>
<li>Crop it to head and shoulders with the <a href="{{root}}tools/crop-image">crop tool</a>, or make a proper <a href="{{root}}tools/passport-photo-maker">passport-size photo</a>.</li>
<li>Compress it above to 45 KB so it lands safely inside a 20 to 50 KB range.</li>
<li>Sign on white paper with a black or blue pen, photograph it, crop right to the ink, and compress it to 18 KB.</li></ol>
{{cta}}
<h2>Common rejections and fixes</h2>
<ul><li><strong>"File size too large":</strong> type a lower target, such as 40, and compress again.</li>
<li><strong>"File size too small":</strong> forms sometimes reject tiny files. Raise the target or resize to the stated dimensions first.</li>
<li><strong>"Invalid format":</strong> make sure the format is JPEG; iPhone HEIC photos are converted automatically.</li>
<li><strong>Blurry signature:</strong> crop closer and use brighter, even light.</li></ul>
<p>Your ID photos and signature are exactly what you shouldn't upload to random converter sites. This tool works on your device only. Keep the originals somewhere private afterwards; that's what <a href="{{root}}features/hidden-vaults">a vault</a> is for.</p>""",
  faq=[{"q": "What is the usual photo size for online forms?", "a": "Many exam and job forms ask for a JPEG photo between 20 and 50 KB, and a signature between 10 and 20 KB. Always follow the exact numbers in the form's official notification."},
       {"q": "How do I reduce a signature to under 20 KB?", "a": "Crop the photo of your signature right to the ink, then compress it above with the target set to 18 KB. A tight crop keeps it sharp at that size."},
       {"q": "My form also gives pixel dimensions. What do I do?", "a": "Resize the photo to those exact pixels first with the resize tool, with Keep proportions off if the shape differs, then compress it to the KB limit."},
       {"q": "Is it safe to make form photos here?", "a": "Yes. Nothing is uploaded: your photo and signature are processed in your browser on your own device."}])

# ---------------------------------------------------------------- resize
page("resize-image", "whatsapp-dp-size", opt={"w": 640, "h": 640},
  kw="whatsapp dp size", also=["whatsapp profile picture size", "whatsapp dp full size", "whatsapp dp crop problem"],
  title="WhatsApp DP size: fit your full photo without awkward cropping",
  desc="The right WhatsApp profile picture size and shape, and how to make a full photo fit the round DP without losing heads or text. Free, no upload.",
  summary="Make your WhatsApp profile picture fit the circle.",
  h1="WhatsApp DP size", lead="WhatsApp shows your profile picture as a circle cut from a square, so a tall or wide photo gets heads, hands or text chopped off. Make it square first and you choose exactly what's shown.",
  answer="A WhatsApp DP should be square; 640 × 640 pixels or larger looks sharp everywhere. Crop your photo to 1:1 with the crop tool, or resize it above, keeping the subject in the centre because the corners are hidden by the circle.",
  body="""<h2>The size and shape that works</h2>
<ul><li><strong>Shape:</strong> square (1:1). WhatsApp crops anything else.</li>
<li><strong>Size:</strong> 640 × 640 pixels is a good target; larger is fine.</li>
<li><strong>Safe area:</strong> keep faces and text inside the central circle, because the corners don't show.</li></ul>
<h2>Fitting a full photo without cropping</h2>
<p>If you want the whole photo visible, such as a group picture or a logo with text, it has to become square without cutting anything off. Use the <a href="{{root}}tools/crop-image">crop tool</a> with the 1:1 shape and place the box over the most important part, or accept a little border: resize the long side to 640 pixels and add the photo to a square in any editor. For most selfies, a 1:1 crop centred on the face looks best.</p>
<h2>Step by step</h2>
<ol><li>Open the <a href="{{root}}tools/crop-image">crop tool</a>, choose 1:1, and frame the face in the middle.</li>
<li>Download it, then drop it in the resizer above at 640 × 640.</li>
<li>In WhatsApp, open Settings, tap your photo, then Edit, and choose the new picture.</li></ol>
{{cta}}
<h2>A privacy note</h2>
<p>Depending on your settings, anyone with your number may see your DP. In WhatsApp's Privacy settings you can limit your profile photo to contacts, or to nobody. Photos of children are best kept off public DPs; our guide to <a href="{{root}}tools/blur-face/blur-kids-faces">blurring kids' faces</a> shows a middle way.</p>""",
  faq=[{"q": "What size should a WhatsApp DP be?", "a": "Square, about 640 × 640 pixels or larger. WhatsApp shows it as a circle, so keep the subject in the centre and away from the corners."},
       {"q": "Why does WhatsApp cut my DP?", "a": "WhatsApp crops profile photos to a square and then shows a circle. Tall or wide photos lose their edges. Crop to 1:1 yourself first to control what's shown."},
       {"q": "Can I set a full-size DP without cropping?", "a": "Only by making the picture square first, either by cropping or by placing it on a square background. WhatsApp won't show a non-square DP whole."},
       {"q": "Who can see my WhatsApp profile photo?", "a": "It depends on your privacy settings. In WhatsApp, open Settings, then Privacy, then Profile photo, and choose Everyone, My contacts, specific contacts or Nobody."}])

page("resize-image", "instagram-photo-size", opt={"w": 1080, "h": 1350},
  kw="instagram photo size", also=["instagram post size", "instagram portrait size 1080x1350", "instagram story size"],
  title="Instagram photo size: post, portrait, story and reel sizes",
  desc="The Instagram sizes that look best: 1080 × 1080 square, 1080 × 1350 portrait and 1080 × 1920 stories, and how to resize photos to fit. Free, no upload.",
  summary="The right size for every Instagram format.",
  h1="Instagram photo size", lead="Instagram shows everything 1080 pixels wide, and the height decides how much of the feed your photo fills. Use the right size and nothing gets cropped or blurry.",
  answer="Post at 1080 × 1350 (4:5 portrait) for the most feed space, 1080 × 1080 for square, and 1080 × 1920 (9:16) for stories and reels. Crop to the shape first, then resize above. Everything happens on your device.",
  body="""<h2>Sizes at a glance</h2>
<div class="table-wrap"><table><thead><tr><th>Format</th><th>Shape</th><th>Size in pixels</th></tr></thead><tbody>
<tr><td>Portrait post</td><td>4:5</td><td>1080 × 1350</td></tr><tr><td>Square post</td><td>1:1</td><td>1080 × 1080</td></tr>
<tr><td>Landscape post</td><td>1.91:1</td><td>1080 × 566</td></tr><tr><td>Story, reel</td><td>9:16</td><td>1080 × 1920</td></tr>
<tr><td>Profile picture</td><td>1:1 (shown round)</td><td>320 × 320 or larger</td></tr></tbody></table></div>
<h2>Why 4:5 wins in the feed</h2>
<p>Portrait posts take up the most vertical space as people scroll, so they're noticed more than square or landscape ones. Most phone photos are 3:4, slightly taller than 4:5, so a gentle crop is all you need.</p>
<h2>How to resize for Instagram</h2>
<ol><li>Crop to the shape with the <a href="{{root}}tools/crop-image">crop tool</a> (4:5, 1:1 or 9:16).</li>
<li>Resize above to the exact pixels in the table.</li>
<li>Upload from your phone; Instagram won't need to crop or squash it.</li></ol>
{{cta}}
<h2>Before you post</h2>
<p>Instagram removes location data from the file itself, but the picture can still reveal a lot: house numbers, car plates, school uniforms. <a href="{{root}}tools/blur-face/blur-license-plate">Blur plates and details</a> first, and keep anything truly private out of your camera roll altogether with an encrypted <a href="{{root}}features/hidden-vaults">vault</a>.</p>""",
  faq=[{"q": "What is the best Instagram post size?", "a": "1080 × 1350 pixels (4:5 portrait). It fills the most space in the feed. Square 1080 × 1080 also works well."},
       {"q": "What size is an Instagram story?", "a": "1080 × 1920 pixels, a 9:16 vertical shape. Keep text away from the top and bottom, where Instagram shows its own buttons."},
       {"q": "Why does Instagram make my photo blurry?", "a": "Usually because the photo is much larger or a different shape than Instagram expects, so it's compressed heavily. Upload 1080 pixels wide in the right shape."},
       {"q": "Are my photos uploaded to resize them?", "a": "No. Cropping and resizing happen in your browser on your own device."}])

page("resize-image", "youtube-thumbnail-size", opt={"w": 1280, "h": 720},
  kw="youtube thumbnail size", also=["youtube thumbnail 1280x720", "youtube thumbnail under 2mb", "youtube thumbnail dimensions"],
  title="YouTube thumbnail size: 1280 × 720 under 2 MB, made easy",
  desc="YouTube thumbnails should be 1280 × 720 pixels, 16:9, and under 2 MB. Crop, resize and compress yours in seconds, free and without uploading.",
  summary="Make thumbnails that meet YouTube's rules.",
  h1="YouTube thumbnail size", lead="YouTube asks for a 16:9 image of 1280 × 720 pixels and under 2 MB. Get any of those wrong and it's rejected or shown blurry.",
  answer="Make your thumbnail 1280 × 720 pixels in 16:9, saved as JPEG or PNG under 2 MB. Crop to 16:9, resize above to 1280 × 720, then compress to under 2,000 KB if needed.",
  body="""<h2>YouTube's thumbnail rules</h2>
<ul><li><strong>Size:</strong> 1280 × 720 pixels (minimum width 640).</li><li><strong>Shape:</strong> 16:9.</li>
<li><strong>File:</strong> JPG, PNG or GIF, under 2 MB.</li></ul>
<h2>Making one from a photo or screenshot</h2>
<ol><li>Open the <a href="{{root}}tools/crop-image">crop tool</a>, choose 16:9, and frame the subject with space for text.</li>
<li>Resize it above to 1280 × 720.</li>
<li>If it's over 2 MB, <a href="{{root}}tools/compress-image">compress</a> it to about 1,500 KB.</li>
<li>Upload it in YouTube Studio under Details, then Thumbnail.</li></ol>
{{cta}}
<h2>Thumbnails that get clicked</h2>
<ul><li>One clear subject, large and close.</li><li>Three to five words of text at most, readable on a phone.</li>
<li>Strong contrast, and nothing important in the bottom-right corner, where YouTube shows the video length.</li></ul>
<p>If the frame includes other people, number plates or screens with personal details, <a href="{{root}}tools/blur-face">blur them</a> before publishing.</p>""",
  faq=[{"q": "What size is a YouTube thumbnail?", "a": "1280 × 720 pixels, in a 16:9 shape, under 2 MB, as JPG, PNG or GIF."},
       {"q": "Why won't YouTube accept my thumbnail?", "a": "It's usually over 2 MB or the wrong format. Compress it under 2 MB and save it as JPEG or PNG."},
       {"q": "Can I use a screenshot from my video?", "a": "Yes. Crop it to 16:9 and resize it to 1280 × 720. Adding a few words of large text helps it stand out."},
       {"q": "Is anything uploaded when I resize here?", "a": "No. Your image is resized in your browser on your own device."}])

# ---------------------------------------------------------------- passport
page("passport-photo-maker", "passport-photo-size-india", opt={"country": "in"},
  kw="passport size photo india", also=["passport photo size in india 35x45", "passport size photo dimensions india", "passport photo white background india"],
  title="Passport size photo in India: 35 × 45 mm, white background",
  desc="Passport size photo in India is 35 × 45 mm with a white background. Make one from your own photo and print a 4×6 sheet of copies. Free, nothing uploaded.",
  summary="Make a 35 × 45 mm Indian passport-size photo.",
  h1="Passport size photo in India", lead="In India, \"passport size\" usually means 35 × 45 mm with a plain white background, and it's asked for everywhere: visa forms, ID cards, admissions and job applications.",
  answer="An Indian passport-size photo is 35 × 45 mm with a white background, the face centred and filling most of the frame. Choose India above, fit the face in the oval, and download the single photo for online forms or the 4×6 sheet to print copies.",
  body="""<h2>The standard size</h2>
<ul><li><strong>Size:</strong> 35 × 45 mm (about 413 × 531 pixels at 300 dpi).</li>
<li><strong>Background:</strong> plain white.</li><li><strong>Face:</strong> looking straight at the camera, neutral expression, eyes open, both ears visible where possible.</li>
<li><strong>Recent:</strong> taken within the last few months.</li></ul>
<p>Requirements differ by purpose. Visa applications for other countries follow that country's rules, and passport photos for some services are taken at the office itself. Always check the official instructions for your application.</p>
<h2>Making it at home</h2>
<ol><li>Stand about a metre in front of a plain white wall, facing a window for even light.</li>
<li>Have someone take the photo at eye level, with your shoulders in the frame.</li>
<li>Choose it in the tool above, keep India selected, and fit your face in the oval.</li>
<li>Download the photo, or the 4×6 sheet to print several copies at a photo studio.</li></ol>
{{cta}}
<h2>For online forms with a KB limit</h2>
<p>Many Indian portals also set a file size, often between 20 and 50 KB. After making the photo, run it through <a href="{{root}}tools/compress-image-to-50kb">compress to 50 KB</a>. See our guide to <a href="{{root}}tools/compress-image-to-50kb/photo-signature-size-online-forms">photo and signature sizes for online forms</a>. Keep scans of ID documents in an encrypted <a href="{{root}}features/hidden-vaults">vault</a>, not your gallery.</p>""",
  faq=[{"q": "What is passport size photo in India?", "a": "Usually 35 × 45 mm with a plain white background, the face centred and filling most of the height. Check the exact rules for your application."},
       {"q": "How many passport photos fit on a 4×6 print?", "a": "Six 35 × 45 mm photos fit on a standard 4×6 inch print with small gaps for cutting, which is what the print sheet in this tool gives you."},
       {"q": "Can I use a phone photo?", "a": "Yes, if it's sharp, evenly lit, taken against a plain white wall and cropped to the right size. This tool handles the cropping and sizing."},
       {"q": "Is my photo uploaded?", "a": "No. It's cropped and sized in your browser on your own device and never sent to a server."}])

page("passport-photo-maker", "us-passport-photo-size", opt={"country": "us"},
  kw="us passport photo size", also=["2x2 passport photo", "us passport photo requirements", "passport photo 2x2 inches"],
  title="US passport photo size: 2 × 2 inches, made from your own photo",
  desc="US passport and visa photos are 2 × 2 inches with the head 1 to 1⅜ inches tall on a white background. Make one free and print a 4×6 sheet. No upload.",
  summary="Make a 2 × 2 inch US passport photo.",
  h1="US passport photo size", lead="US passport and visa photos are a square 2 × 2 inches, with strict rules on head size and background. Make one from a photo taken at home, and print it for the price of one 4×6 print.",
  answer="A US passport photo is 2 × 2 inches (51 × 51 mm), with the head between 1 and 1⅜ inches from chin to top of the head, on a white or off-white background, no glasses. Choose the US size above, fit the face in the oval and download the photo or a 4×6 print sheet.",
  body="""<h2>The key requirements</h2>
<ul><li><strong>Size:</strong> 2 × 2 inches (600 × 600 pixels at 300 dpi).</li>
<li><strong>Head size:</strong> 1 to 1⅜ inches from chin to top of head.</li>
<li><strong>Background:</strong> plain white or off-white, no shadows.</li>
<li><strong>No glasses</strong>, neutral expression or a natural smile, eyes open.</li>
<li><strong>Recent:</strong> taken in the last six months.</li></ul>
<p>Rules are set by the US Department of State and can change; check travel.state.gov before you apply.</p>
<h2>Step by step</h2>
<ol><li>Take a photo facing a window, in front of a plain white wall, at eye level.</li>
<li>Choose it above and keep "US passport and visa (2 × 2 in)" selected.</li>
<li>Move and resize the box until the face fills the oval: chin at the bottom, hair near the top.</li>
<li>Download the 4×6 sheet and print it as a regular 4×6 photo, then cut out two copies.</li></ol>
{{cta}}
<h2>Online renewals</h2>
<p>For online renewal, a digital photo is uploaded instead of printed. Use "Download photo" for the single 600 × 600 image. Keep your passport scans private afterwards; an encrypted <a href="{{root}}features/encryption">vault</a> keeps them out of your camera roll and cloud.</p>""",
  faq=[{"q": "What size is a US passport photo?", "a": "2 × 2 inches (51 × 51 mm), with the head measuring 1 to 1⅜ inches from chin to top of the head, on a white or off-white background."},
       {"q": "Can I wear glasses in a US passport photo?", "a": "No. Glasses aren't allowed in US passport photos except in rare medical cases with a signed statement."},
       {"q": "How do I print 2×2 photos cheaply?", "a": "Download the 4×6 print sheet and order it as a standard 4×6 photo print at a pharmacy or photo kiosk, then cut along the lines."},
       {"q": "Is my photo stored anywhere?", "a": "No. Everything happens in your browser on your own device; nothing is uploaded or stored."}])

page("passport-photo-maker", "print-passport-photos-4x6", opt={"country": "eu"},
  kw="print passport photos 4x6", also=["passport photo print sheet", "passport size photo sheet", "print passport photos at home"],
  title="Print passport photos on a 4×6 sheet for the price of one print",
  desc="Put several passport photos on one 4×6 inch sheet and print them at any photo kiosk. Works for 35×45 mm, 2×2 in and more. Free, nothing uploaded.",
  summary="Several passport photos on one cheap 4×6 print.",
  h1="Print passport photos on a 4×6 sheet", lead="Photo studios charge for a set of passport photos. A standard 4×6 inch print costs a fraction of that, and it can hold four to six passport photos at the exact size.",
  answer="Make your passport photo above, tap \"Download 4×6 in print sheet\", and order it as a normal 4×6 inch (10 × 15 cm) print. Choose \"actual size\" or no cropping at the kiosk, then cut along the thin lines.",
  body="""<h2>How many fit</h2>
<div class="table-wrap"><table><thead><tr><th>Photo size</th><th>Copies per 4×6 sheet</th></tr></thead><tbody>
<tr><td>35 × 45 mm (India, UK, EU, Australia)</td><td>6</td></tr><tr><td>2 × 2 in (US)</td><td>4</td></tr>
<tr><td>50 × 70 mm (Canada, Brazil)</td><td>2</td></tr><tr><td>33 × 48 mm (China visa)</td><td>6</td></tr></tbody></table></div>
<h2>Printing it right</h2>
<ol><li>Make your photo in the tool above and download the print sheet.</li>
<li>Order a 4×6 inch (10 × 15 cm) print at a kiosk, pharmacy or online service.</li>
<li>Choose glossy or matte photo paper, and turn off any "fill" or "auto crop" option so it prints at actual size.</li>
<li>Check one photo with a ruler before cutting the rest.</li></ol>
<p>The sheet is saved at 300 dpi, so each photo prints at its exact size.</p>
{{cta}}
<h2>Printing at home</h2>
<p>Home printers often scale images to fit the page. Use a 4×6 photo tray and set the scale to 100% or "actual size". Ordinary paper isn't accepted for most official photos, so use photo paper.</p>
<p>Taking the photo yourself also means it never sits on a studio's computer. Keep the original somewhere private, such as an encrypted <a href="{{root}}features/hidden-vaults">vault</a>, and see our guide on <a href="{{root}}tools/passport-photo-maker/passport-photo-size-india">passport-size photos in India</a>.</p>""",
  faq=[{"q": "Can I print passport photos at a normal photo kiosk?", "a": "Yes. Print the 4×6 sheet as a standard 4×6 inch photo with no cropping, then cut out the photos along the lines."},
       {"q": "How many 35 × 45 mm photos fit on 4×6?", "a": "Six, with small gaps between them for cutting."},
       {"q": "Why are my printed photos the wrong size?", "a": "The kiosk or printer probably scaled the image. Choose actual size or 100%, and turn off fill or auto crop."},
       {"q": "Is the sheet made on my device?", "a": "Yes. The sheet is built in your browser; your photo is never uploaded."}])

# ---------------------------------------------------------------- location
META_TOOL = '''<div class="meta-drop" id="meta-drop">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/><path d="M4 4l16 16"/></svg>
        <p><strong>Drop photos here</strong> or</p>
        <label class="btn btn-primary">Choose photos<input id="meta-input" type="file" accept="image/jpeg,image/png" multiple hidden></label>
        <p class="dim">JPEG and PNG. Your photos never leave this device.</p>
      </div>
      <ul class="meta-results" id="meta-results" aria-live="polite"></ul>'''

page("remove-photo-location", "find-where-a-photo-was-taken", opt={},
  kw="find where a photo was taken", also=["how to see location of a photo", "photo gps location finder", "check photo metadata location"],
  title="Find where a photo was taken: check its hidden GPS location",
  desc="See the GPS location, date and phone hidden inside a photo, and open it on a map. Works on phone and computer, free, and the photo is never uploaded.",
  summary="Read a photo's hidden location, date and phone model.",
  h1="Find where a photo was taken", lead="Many photos carry the exact place they were taken, hidden in their EXIF data. Drop a photo here to see the coordinates, the date and the phone that took it.",
  answer="To find where a photo was taken, drop the original file in the tool above. If it has GPS data, you'll see the coordinates; paste them into Google Maps to see the spot. Photos sent through WhatsApp or downloaded from social media usually have the location removed.",
  body="""<h2>What you can find out</h2>
<ul><li><strong>GPS coordinates</strong>, often accurate to a few metres.</li><li><strong>Date and time</strong> the photo was taken.</li>
<li><strong>Phone make and model.</strong></li></ul>
<p>To see the place, copy the two numbers (latitude, longitude) into the search box of Google Maps or any map app.</p>
<h2>When there's no location</h2>
<ul><li>The camera had location tags turned off.</li><li>The photo was sent through WhatsApp, Instagram, Facebook or similar apps, which usually strip it.</li>
<li>It's a screenshot, which never has a location.</li><li>It was edited or saved by an app that removed the data.</li></ul>
{{cta}}
<h2>Check your own photos before sharing</h2>
<p>The same data that helps you find where a photo was taken lets anyone else find out where you were, including your home. Before posting or sending originals, use the tool's "Download clean copy" to <a href="{{root}}tools/remove-photo-location">remove the location</a>, and learn how to <a href="{{root}}tools/remove-photo-location/turn-off-camera-location-android">stop your camera adding it</a>.</p>""",
  faq=[{"q": "Can I see where a photo was taken?", "a": "Only if the original file still contains GPS data. Drop it in the tool above; if there's a location, you'll see the coordinates to open on a map."},
       {"q": "Why does my photo show no location?", "a": "Location tags were off, or the photo passed through an app such as WhatsApp or Instagram that removes it, or it's a screenshot."},
       {"q": "Can I find the location of a photo someone sent me?", "a": "Only if they sent the original file, for example as a document or email attachment. Normal photo messages usually have it removed."},
       {"q": "Is the photo uploaded?", "a": "No. The data is read in your browser on your own device."}])

page("remove-photo-location", "turn-off-camera-location-android", opt={},
  kw="turn off location on camera android", also=["stop camera saving location", "samsung camera location tags off", "remove gps from camera android"],
  title="Turn off camera location on Android: Samsung, Pixel and more",
  desc="Stop your Android camera saving GPS location in every photo. Steps for Samsung, Pixel, Xiaomi and others, plus how to clean photos you already took.",
  summary="Stop new photos recording where you are.",
  h1="Turn off camera location on Android", lead="Your camera may be quietly saving the exact GPS spot of every photo. Turning it off takes ten seconds, and it protects every picture you take from now on.",
  answer="Open your Camera app's settings and turn off the option called Location tags, Save location or GPS tag. On Samsung it's Location tags; on Pixel it's Save location. Photos you've already taken keep their location, so clean those with the tool above before sharing.",
  body="""<h2>Where to find it</h2>
<div class="table-wrap"><table><thead><tr><th>Phone</th><th>Setting</th></tr></thead><tbody>
<tr><td>Samsung Galaxy</td><td>Camera → Settings (gear) → Location tags</td></tr>
<tr><td>Google Pixel</td><td>Camera → Settings → Save location</td></tr>
<tr><td>Xiaomi, Redmi, POCO</td><td>Camera → Settings → Save location info</td></tr>
<tr><td>OPPO, realme, OnePlus</td><td>Camera → Settings → Location</td></tr>
<tr><td>vivo</td><td>Camera → Settings → Location / GPS tag</td></tr></tbody></table></div>
<p>Wording changes between versions. If you can't find it, search the Settings app for "location" and look under Camera, or remove the camera app's location permission in Settings → Apps → Camera → Permissions.</p>
<h2>Check it worked</h2>
<ol><li>Take a test photo.</li><li>Drop it into the tool above.</li><li>If no location appears, you're done.</li></ol>
{{cta}}
<h2>Photos you already took</h2>
<p>Turning off location tags doesn't change existing photos. Use the tool to download clean copies of anything you share. For photos you never want seen, keep them out of the gallery altogether: Sealcloak's <a href="{{root}}features/private-camera-and-scanner">private camera</a> saves straight into an encrypted vault. See also how to <a href="{{root}}tools/remove-photo-location/find-where-a-photo-was-taken">check a photo's location</a>.</p>""",
  faq=[{"q": "How do I stop my Samsung camera saving location?", "a": "Open the Camera app, tap the gear icon, and turn off Location tags. New photos won't include GPS data."},
       {"q": "Does turning off location remove it from old photos?", "a": "No. It only affects new photos. Clean older ones with the tool above before you share them."},
       {"q": "Can I keep location for some photos?", "a": "Yes. Leave location on, and clean only the photos you share. Many people turn it off simply so they don't have to remember."},
       {"q": "Do apps like Google Photos still know where I was?", "a": "They may estimate places from other data such as your Google account location history. Check those settings separately."}])

page("remove-photo-location", "remove-location-from-photos-iphone", opt={},
  kw="remove location from photo iphone", also=["iphone photo location off when sharing", "remove gps from iphone photo", "iphone share without location"],
  title="Remove location from a photo on iPhone before you share it",
  desc="Share iPhone photos without their location: use the Options switch when sharing, turn off camera location, or clean the file here. Free, nothing uploaded.",
  summary="Share iPhone photos without where they were taken.",
  h1="Remove location from a photo on iPhone", lead="iPhone photos record where they were taken. You can strip that each time you share, stop it at the camera, or clean any file in your browser.",
  answer="On iPhone, tap Share, then Options at the top, and turn off Location before sending. To stop it for every new photo, go to Settings → Privacy & Security → Location Services → Camera and choose Never. You can also drop a photo in the tool above for a clean copy.",
  body="""<h2>Three ways</h2>
<ol><li><strong>When sharing:</strong> tap Share, then Options under the photo preview, and switch off Location.</li>
<li><strong>For all new photos:</strong> Settings → Privacy & Security → Location Services → Camera → Never.</li>
<li><strong>For any file:</strong> drop it in the tool above and download the clean copy. This also works for photos you've moved to a computer.</li></ol>
<h2>HEIC photos</h2>
<p>iPhones save photos as HEIC by default. This tool cleans JPEG and PNG, so either share as "Most Compatible" or convert first with <a href="{{root}}tools/heic-to-jpg">HEIC to JPG</a>, which runs on your device too. You can set future photos to JPEG in Settings → Camera → Formats → Most Compatible.</p>
{{cta}}
<h2>Sending to Android users</h2>
<p>If you send originals to someone on Android, as a file or by email, the location goes with them unless you remove it. And if you move to Android yourself, see our guide to <a href="{{root}}tools/heic-to-jpg/open-heic-on-android">opening HEIC photos on Android</a>.</p>""",
  faq=[{"q": "How do I share an iPhone photo without location?", "a": "Tap Share, tap Options at the top of the share sheet, and turn off Location. The photo is then sent without its GPS data."},
       {"q": "How do I stop my iPhone camera saving location?", "a": "Go to Settings, Privacy & Security, Location Services, Camera, and choose Never."},
       {"q": "Does this tool work with HEIC?", "a": "It cleans JPEG and PNG. Convert HEIC to JPG first with our HEIC to JPG tool, or set the camera to Most Compatible."},
       {"q": "Is anything uploaded?", "a": "No. The tool reads and cleans the file in your browser on your own device."}])

page("remove-photo-location", "does-whatsapp-remove-location", opt={},
  kw="does whatsapp remove location from photos", also=["whatsapp exif data", "whatsapp photo metadata", "whatsapp document photo location"],
  title="Does WhatsApp remove location from photos? Mostly, with one catch",
  desc="WhatsApp usually strips location from photos sent normally, but not from photos sent as documents. Check any photo's hidden data here, free and private.",
  summary="When WhatsApp keeps your photo's location, and when it doesn't.",
  h1="Does WhatsApp remove location from photos?", lead="Normally, yes: photos sent the usual way are compressed and lose their hidden data. But send the same photo as a document, and it arrives exactly as it left your camera, location included.",
  answer="Photos sent normally on WhatsApp are compressed and generally lose their location data. Photos sent as a document keep everything, including GPS coordinates. If you send originals, clean them first with the tool above.",
  body="""<h2>Normal photo vs document</h2>
<div class="table-wrap"><table><thead><tr><th>How you send it</th><th>Location data</th><th>Quality</th></tr></thead><tbody>
<tr><td>As a photo</td><td>Generally removed</td><td>Compressed</td></tr>
<tr><td>As a document (file)</td><td>Kept</td><td>Original</td></tr>
<tr><td>HD photo option</td><td>Check with the tool</td><td>Higher</td></tr></tbody></table></div>
<p>Behaviour can change with app updates. The only way to be sure is to check the file the other person receives, or to clean it before sending.</p>
<h2>How to check</h2>
<ol><li>Send the photo to yourself (Message yourself) the same way you plan to send it.</li>
<li>Save the received photo, then drop it in the tool above.</li>
<li>If coordinates appear, clean the original and send the clean copy instead.</li></ol>
{{cta}}
<h2>Other apps</h2>
<p>Most social apps strip location from images they display, but email, Bluetooth, cloud links and USB transfers send the original file. When in doubt, <a href="{{root}}tools/remove-photo-location">remove the location</a> first, and keep private photos in an encrypted <a href="{{root}}features/hidden-vaults">vault</a> rather than in chats.</p>""",
  faq=[{"q": "Does WhatsApp keep the location in photos?", "a": "Photos sent normally are generally compressed and lose their location data. Photos sent as documents keep it."},
       {"q": "How do I send a photo on WhatsApp without location?", "a": "Send it as a normal photo, or if you need the original quality as a document, remove the location first with the tool above."},
       {"q": "Can someone find my location from a WhatsApp photo?", "a": "From a normal photo message, usually not from the file itself. From a photo sent as a document, yes, if location tags were on when it was taken."},
       {"q": "Does this tool upload my photo?", "a": "No. It works in your browser on your own device."}])

# ---------------------------------------------------------------- blur
page("blur-face", "blur-license-plate", opt={},
  kw="blur license plate", also=["blur number plate in photo", "hide car number plate", "blur plate before selling car"],
  title="Blur a license plate in a photo before you post or sell",
  desc="Hide a car's number plate in a photo in seconds: draw a box, choose blur or pixelate, download. Free, works on your phone, and nothing is uploaded.",
  summary="Hide number plates before you post or sell.",
  h1="Blur a license plate", lead="A number plate links a photo to a car, an address and an owner. Blur it before posting car photos, selling a vehicle or sharing street pictures.",
  answer="To blur a license plate, choose the photo above, drag a box over the plate, set Pixelate or Blur to high strength, and download. Cover the whole plate, including the edges. Nothing is uploaded.",
  body="""<h2>Step by step</h2>
<ol><li>Choose the photo above.</li><li>Drag a box a little larger than the plate.</li>
<li>Choose Pixelate with a high strength; it's the easiest to judge by eye.</li>
<li>Check the result at full size, then download.</li></ol>
<h2>When to blur plates</h2>
<ul><li>Selling a car online: buyers can see the car without the plate.</li><li>Posting road trip and parking photos.</li>
<li>Dashcam clips and street photography.</li><li>Photos taken outside your home, where a plate links to your address.</li></ul>
{{cta}}
<h2>Don't forget the rest</h2>
<p>Car photos often show more: a house number, a street sign, a parking permit, a reflection. <a href="{{root}}tools/blur-face">Blur those too</a>, and <a href="{{root}}tools/remove-photo-location">remove the hidden GPS location</a> from the file before posting.</p>""",
  faq=[{"q": "Should I blur my number plate when selling a car?", "a": "Many sellers do. It stops strangers linking the photo to your address or using your plate details, and buyers can still see the car."},
       {"q": "Is pixelate or blur better for plates?", "a": "Both work at high strength. Pixelate makes it easier to see that every character is unreadable."},
       {"q": "Can a blurred plate be read again?", "a": "A weak blur sometimes can be. Use a high strength and cover the whole plate, or crop it out entirely."},
       {"q": "Is my photo uploaded?", "a": "No. Blurring happens in your browser on your own device."}])

page("blur-face", "blur-kids-faces", opt={},
  kw="blur kids faces in photos", also=["hide child face in photo", "blur child face before posting", "sharing kids photos online safely"],
  title="Blur kids' faces in photos before you share them online",
  desc="Share family moments without showing your children's faces: blur or pixelate them in seconds, on your phone, without uploading. Free.",
  summary="Share family photos without your children's faces.",
  h1="Blur kids' faces in photos", lead="Plenty of parents want to share the moment without putting their children's faces online for good. Blur or pixelate faces in seconds, and decide later what your kids want public.",
  answer="Choose the photo above, drag a box over each child's face, set Blur or Pixelate to a high strength and download. Check for school logos, names on clothing and house numbers too. The photo never leaves your phone.",
  body="""<h2>Step by step</h2>
<ol><li>Choose the photo above.</li><li>Drag a box over each face, slightly bigger than the face.</li>
<li>Set the strength high, then check the result at full size.</li><li>Download and share the blurred copy.</li></ol>
<h2>What else gives children away</h2>
<ul><li>School uniforms, badges and logos.</li><li>Names on bags, bottles and sports shirts.</li>
<li>House numbers, street signs and car plates.</li><li>The photo's hidden location, which can point to home or school; <a href="{{root}}tools/remove-photo-location">remove it</a> first.</li></ul>
{{cta}}
<h2>Keep the originals private</h2>
<p>The unblurred originals still matter. Family photos sync to cloud accounts and sit in galleries that anyone borrowing your phone can scroll. Keeping the ones you treasure in an encrypted <a href="{{root}}features/hidden-vaults">vault</a> keeps them yours. Our page on <a href="{{root}}scenarios/kids-using-my-phone">kids using your phone</a> has more tips.</p>""",
  faq=[{"q": "Should I blur my child's face on social media?", "a": "It's a personal choice. Many parents do, so their children can decide about their own online presence when they're older."},
       {"q": "Can people unblur a face?", "a": "A light blur can sometimes leave a face recognisable. Use a high strength and cover the whole face, or crop it out."},
       {"q": "Does the tool find faces automatically?", "a": "No, you draw a box over each face. It's quick, accurate and means no face detection runs on your family photos."},
       {"q": "Are my photos uploaded?", "a": "No. Everything happens in your browser on your own device."}])

# ---------------------------------------------------------------- formats
page("heic-to-jpg", "open-heic-on-android", opt={"to": "image/jpeg"},
  kw="open heic on android", also=["heic file android", "view heic photos on android", "heic not opening android"],
  title="Open HEIC photos on Android: view or convert iPhone pictures",
  desc="Got HEIC photos from an iPhone that won't open on your Android phone? Here's why, and how to view or convert them to JPG in seconds, without uploading.",
  summary="View or convert iPhone HEIC photos on Android.",
  h1="Open HEIC photos on Android", lead="HEIC is the format iPhones use for photos. Newer Android phones and Google Photos can often display it, but many apps, older phones and websites can't. Converting to JPG makes it work everywhere.",
  answer="Try opening the HEIC file in Google Photos first; recent Android versions can display it. If it won't open, or an app or website refuses it, choose the files in the converter above and download them as JPG. The conversion happens on your phone.",
  body="""<h2>Why HEIC causes problems</h2>
<p>HEIC (High Efficiency Image Container) stores photos at roughly half the size of JPG at similar quality, which is why iPhones use it. Support on Android depends on the phone's Android version and the app. Gallery apps, messaging apps, editors and upload forms often don't accept it.</p>
<h2>Convert in three steps</h2>
<ol><li>Save the HEIC files to your phone, for example from email or Files.</li>
<li>Choose them in the converter above. They're decoded on your device by a small library this page loads.</li>
<li>Download the JPGs. They open in any app.</li></ol>
{{cta}}
<h2>Ask the sender to send JPG</h2>
<p>iPhone users can share photos as JPG automatically: on the iPhone, Settings → Camera → Formats → Most Compatible. Photos sent through most messaging apps are converted anyway. If they include the location, <a href="{{root}}tools/remove-photo-location">remove it</a> before you pass them on.</p>""",
  faq=[{"q": "Can Android open HEIC files?", "a": "Recent Android versions and Google Photos can often display HEIC, but many apps, older phones and websites can't. Converting to JPG works everywhere."},
       {"q": "Will converting HEIC to JPG reduce quality?", "a": "The JPG is saved at high quality (92%), which looks the same in normal viewing. The file may be a little larger than the HEIC."},
       {"q": "Can I convert many HEIC photos at once?", "a": "Yes. Choose them all; each is converted on your device and gets its own download button."},
       {"q": "Are my photos uploaded?", "a": "No. The conversion runs in your browser on your phone."}])

page("webp-to-png", "what-is-a-webp-file", opt={"to": "image/png"},
  kw="what is a webp file", also=["webp file meaning", "how to open webp", "webp vs png vs jpg"],
  title="What is a WebP file, and how do you open or convert it?",
  desc="WebP is Google's image format for faster websites. Learn why images save as .webp, how to open them, and convert WebP to PNG or JPG free, with no upload.",
  summary="What WebP is, and how to turn it into PNG or JPG.",
  h1="What is a WebP file?", lead="If an image you saved from a website ended in .webp and won't open where you need it, you've met WebP: a format made by Google so web pages load faster.",
  answer="WebP is an image format from Google that makes images smaller than JPG or PNG at similar quality, so websites use it. Browsers open it, but some apps and forms don't. Convert it to PNG above (keeps transparency) or to JPG for photos.",
  body="""<h2>WebP in a nutshell</h2>
<ul><li>Created by Google and released in 2010.</li><li>Supports both lossy (like JPG) and lossless (like PNG) compression.</li>
<li>Supports transparency and animation.</li><li>Files are typically noticeably smaller than JPG or PNG at similar quality.</li></ul>
<h2>Why your download is WebP</h2>
<p>Websites send WebP to browsers that support it, which is almost all of them. When you save the image, you get the format the site sent, even if the page looked like it showed a normal photo.</p>
<h2>Which format to convert to</h2>
<div class="table-wrap"><table><thead><tr><th>Use</th><th>Convert to</th></tr></thead><tbody>
<tr><td>Logos, stickers, screenshots, anything transparent</td><td>PNG (this page)</td></tr>
<tr><td>Photos to send or print</td><td><a href="{{root}}tools/webp-to-jpg">JPG</a></td></tr>
<tr><td>Your own website</td><td>Keep WebP</td></tr></tbody></table></div>
{{cta}}
<p>The converter runs in your browser, so the images you convert stay on your device. For more on formats, see <a href="{{root}}tools/png-to-webp">PNG to WebP</a>.</p>""",
  faq=[{"q": "What is a WebP file?", "a": "An image format by Google that makes images smaller than JPG or PNG at similar quality. It's widely used on websites."},
       {"q": "How do I open a WebP file?", "a": "Any modern browser opens it. For apps that don't, convert it to PNG or JPG with the tool above."},
       {"q": "Is WebP better than PNG?", "a": "For websites, usually: it's smaller. For editing, printing and apps that need wide compatibility, PNG or JPG is easier."},
       {"q": "Is my image uploaded to convert it?", "a": "No. Conversion happens in your browser on your own device."}])

page("jpg-to-pdf", "jpg-to-pdf-on-android", opt={"page": "a4"},
  kw="jpg to pdf on android", also=["convert photo to pdf on phone", "image to pdf android free", "make pdf from photos android"],
  title="Convert JPG to PDF on Android, free and without an app",
  desc="Turn photos on your Android phone into one PDF in your browser: pick, order and save. No app to install, no watermark, and your photos aren't uploaded.",
  summary="Make PDFs from photos on your phone, no app needed.",
  h1="JPG to PDF on Android", lead="Need to send photos of documents as a single PDF from your phone? You don't need to install an app or upload anything. Do it right here in your browser.",
  answer="On your Android phone, choose the photos in the tool above, order them with the arrows, pick A4 or Letter and tap Create PDF. Download it and share it from your Downloads folder. The PDF is made on your phone.",
  body="""<h2>Step by step on Android</h2>
<ol><li>Tap Choose photos above and select them from your gallery or Files.</li>
<li>Use ↑ and ↓ to put the pages in order.</li><li>Choose A4 (most countries) or Letter (US, Canada), or Fit to image.</li>
<li>Tap Create PDF, then Download. It's saved to your Downloads folder.</li>
<li>Share it from Files or attach it to email or WhatsApp as a document.</li></ol>
<h2>Better document photos</h2>
<ul><li>Lay the page flat in good, even light; avoid flash glare.</li><li>Hold the phone directly above, parallel to the page.</li>
<li><a href="{{root}}tools/crop-image">Crop</a> away the table or background first.</li><li>If the PDF must be small, <a href="{{root}}tools/compress-image">compress</a> the photos first.</li></ul>
{{cta}}
<h2>Scanning private documents</h2>
<p>ID cards, bank letters and medical reports shouldn't sit in your gallery or on a converter's server. Sealcloak's <a href="{{root}}features/private-camera-and-scanner">document scanner</a> creates PDFs directly inside an encrypted vault, so the scans never appear in your gallery at all.</p>""",
  faq=[{"q": "How do I convert JPG to PDF on Android without an app?", "a": "Use the tool above in your phone's browser: choose the photos, order them, tap Create PDF and download. No app or account needed."},
       {"q": "Where is the PDF saved?", "a": "In your phone's Downloads folder, which you can open from the Files app."},
       {"q": "Can I make one PDF from many photos?", "a": "Yes. Each photo becomes a page, in the order you set."},
       {"q": "Are my photos uploaded?", "a": "No. The PDF is built in your browser on your own phone."}])

# ---------------------------------------------------------------- security
page("wifi-qr-code", "share-wifi-password-android", opt={"type": "wifi"},
  kw="share wifi password android", also=["show wifi password android", "android wifi qr code share", "find wifi password on android"],
  title="Share your Wi-Fi password from Android with a QR code",
  desc="Find and share your Wi-Fi password on Android with the built-in QR code, or make a printable Wi-Fi QR code for guests. Free, and private.",
  summary="Share Wi-Fi from Android, or print a QR for guests.",
  h1="Share your Wi-Fi password from Android", lead="Android can show your Wi-Fi password as a QR code so a friend can scan and join. For guests who visit often, make a printable code instead.",
  answer="On Android 10 and newer, open Settings → Network & internet (or Connections) → Wi-Fi, tap your network or its gear icon, then Share or QR code. Unlock to show the code; your friend scans it with their camera. For a printed sign, make a code with the tool above.",
  body="""<h2>Using Android's built-in QR</h2>
<ol><li>Open Settings and go to Wi-Fi (Network & internet on Pixel, Connections on Samsung).</li>
<li>Tap the network you're connected to, or its gear icon.</li><li>Tap Share or QR code, and confirm with your fingerprint or PIN.</li>
<li>Your friend points their camera at the code and taps Join. Many phones also show the password in text under the code.</li></ol>
<h2>A printable code for guests</h2>
<ol><li>Type the network name and password in the tool above, and choose WPA.</li><li>Download the PNG and print it, or save the SVG for a sign.</li>
<li>Test it with your phone camera before putting it up.</li></ol>
{{cta}}
<h2>Keep it safe</h2>
<p>Anyone who scans the code can join, so use a guest network if your router supports it. If you change your Wi-Fi password, make a new code. Codes made here are generated on your device; the password isn't sent anywhere. For stronger passwords, try our <a href="{{root}}tools/password-generator">password generator</a>.</p>""",
  faq=[{"q": "How do I see my Wi-Fi password on Android?", "a": "Open Wi-Fi settings, tap your network, then Share. After unlocking, many phones show the password in text below the QR code."},
       {"q": "Can iPhones scan an Android Wi-Fi QR code?", "a": "Yes. The iPhone Camera app recognises Wi-Fi QR codes and offers to join the network."},
       {"q": "Is it safe to put a Wi-Fi QR code on the wall?", "a": "Only where you're happy for anyone present to join. Use a guest network so visitors can't reach your other devices."},
       {"q": "Is my password sent anywhere when I make a code here?", "a": "No. The code is generated in your browser; nothing is sent to a server."}])

page("password-generator", "how-long-should-a-password-be", opt={"kind": "words"},
  kw="how long should a password be", also=["password length recommendation", "is 8 characters enough", "strong password length"],
  title="How long should a password be? The honest answer",
  desc="How long a password needs to be depends on how random it is. See practical lengths for passwords and passphrases, and generate a strong one free.",
  summary="Practical lengths for passwords and passphrases.",
  h1="How long should a password be?", lead="Length matters, but randomness matters more. A random 16-character password or a five-word random passphrase is strong; a long password made of a name and a year is not.",
  answer="Use at least 16 random characters for passwords stored in a password manager, and a passphrase of at least five random words for ones you must remember. Eight characters is the bare minimum many sites accept, and it isn't enough for important accounts.",
  body="""<h2>Practical lengths</h2>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>Good length</th><th>Why</th></tr></thead><tbody>
<tr><td>Random characters (manager)</td><td>16 to 20</td><td>Very strong; you never type it</td></tr>
<tr><td>Random passphrase (memorised)</td><td>5 to 6 words</td><td>Strong and easy to type</td></tr>
<tr><td>PIN for a phone</td><td>6+ digits</td><td>Protected by lockouts, not length alone</td></tr></tbody></table></div>
<h2>Randomness beats tricks</h2>
<p>Attackers try common words, names, dates and substitutions like @ for a first. "Summer2024!" is long-ish but guessable. A passphrase like five random words from a big list has around 65 bits of randomness, and every extra word multiplies the guesses needed by 7,776. The generator above shows the randomness of each password it makes.</p>
{{cta}}
<h2>Length isn't everything</h2>
<ul><li><strong>Never reuse</strong> a password; one leak can unlock everything else.</li><li><strong>Turn on two-step verification</strong> for email and banking.</li>
<li><strong>Use a password manager</strong> so long random passwords cost you no effort.</li></ul>
<p>Sealcloak applies the same idea to vaults: each gets a <a href="{{root}}features/recovery-phrase">9-word random recovery phrase</a>, and your <a href="{{root}}features/pattern-lock">pattern</a> is slowed down with Argon2id so each guess is expensive.</p>""",
  faq=[{"q": "Is an 8-character password enough?", "a": "Not for important accounts. Eight random characters can be cracked offline far faster than 16. Use at least 16 random characters or a passphrase of five or more words."},
       {"q": "Are passphrases better than passwords?", "a": "For passwords you must remember, yes: five or six random words are strong and easy to type. For stored passwords, random characters are just as good."},
       {"q": "Does adding a symbol make a password strong?", "a": "Not by itself. Predictable patterns like a capital first letter and ! at the end are the first things attackers try. Randomness is what counts."},
       {"q": "Is the generated password sent anywhere?", "a": "No. It's created in your browser with secure randomness and never leaves your device."}])

page("encrypt-file", "send-files-securely", opt={"drop": "Drop files here", "choose": "Choose files", "hint": "Any file type. Files never leave this device."},
  kw="send files securely", also=["send sensitive documents securely", "share files with password", "secure file transfer free"],
  title="How to send files securely: lock them before they leave",
  desc="Send sensitive files safely by encrypting them with a password before you email or upload them, then sharing the password another way. Free and private.",
  summary="Encrypt files before sending, share the password separately.",
  h1="How to send files securely", lead="Email, chat apps and cloud links weren't designed for passports, contracts and medical records. The simplest safe habit: encrypt the file with a password first, then send the password a different way.",
  answer="Type a strong password above, choose the file, and send the .locked copy by email, chat or cloud link. Tell the recipient the password by phone call or in person, not in the same message. They open this page, enter the password and get the original file back.",
  body="""<h2>Step by step</h2>
<ol><li>Make a strong password; a <a href="{{root}}tools/password-generator">random passphrase</a> is easy to read out.</li>
<li>Encrypt the file above. You get name.locked, encrypted with AES-256-GCM.</li>
<li>Send the .locked file any way you like.</li><li>Share the password separately: a call, a text to a different app, or in person.</li>
<li>The recipient opens this page, types the password and chooses the .locked file.</li></ol>
<h2>Why encrypt before sending</h2>
<ul><li>Emails sit in inboxes, backups and servers for years.</li><li>Forwarded or misaddressed messages expose attachments.</li>
<li>Cloud links can be shared further than you intended.</li></ul>
<p>An encrypted file stays unreadable in all those places without the password.</p>
{{cta}}
<h2>Good practice</h2>
<ul><li>Never put the password in the same email or chat as the file.</li><li>Use a different password for each recipient or batch.</li>
<li>Delete your unencrypted copy from Downloads once it's sent, or keep it in an encrypted <a href="{{root}}features/hidden-vaults">vault</a>.</li></ul>
<p>Sealcloak can also send files from your vault as a <a href="{{root}}features/secure-sharing">passphrase-locked package</a>.</p>""",
  faq=[{"q": "What is the safest way to send a sensitive file?", "a": "Encrypt it with a strong password before sending, and share the password through a different channel, such as a phone call."},
       {"q": "Does the recipient need special software?", "a": "No. They open this page in any modern browser, type the password and choose the .locked file to get the original back."},
       {"q": "Can I send the password in the same email?", "a": "Don't. Anyone who gets the email would then have both. Use a call, a different app or tell them in person."},
       {"q": "Is my file uploaded when I encrypt it?", "a": "No. Encryption happens in your browser on your own device."}])

page("brighten-photo", "fix-dark-photos", opt={},
  kw="fix dark photos", also=["brighten underexposed photo", "make dark picture brighter", "fix night photo"],
  title="Fix dark photos: brighten underexposed pictures in one tap",
  desc="Rescue photos that came out too dark, indoors, at night or against the light. One-tap auto fix, fine controls, full resolution. Free, nothing uploaded.",
  summary="Rescue photos that came out too dark.",
  h1="Fix dark photos", lead="Indoor parties, evening dinners and photos taken against a window often come out dark. Brightening them with a curve, instead of just turning everything up, brings back faces without washing out the rest.",
  answer="Choose the dark photo above; Auto fix lifts the shadows immediately. Nudge Brightness, Contrast and Colour if you like, then download the full-resolution result. Everything happens on your device.",
  body="""<h2>Why photos come out dark</h2>
<ul><li><strong>Low light:</strong> the camera can't gather enough light without blur.</li>
<li><strong>Backlight:</strong> a bright window or sky behind the subject fools the exposure.</li>
<li><strong>Dark scenes:</strong> cameras sometimes keep night scenes dark on purpose.</li></ul>
<h2>Getting a natural result</h2>
<ol><li>Start with Auto fix.</li><li>Raise Brightness until faces look right; stop before the darkest areas turn grey.</li>
<li>Add a little Contrast to bring back depth.</li><li>Lift Colour slightly if skin looks pale.</li></ol>
{{cta}}
<h2>Next time</h2>
<ul><li>Tap the subject's face on screen before shooting, so the camera exposes for it.</li>
<li>Use Night mode for still scenes, and hold the phone steady.</li><li>Turn so the light is behind you, not behind the subject.</li></ul>
<p>Rescued photos of personal moments deserve a private home; an encrypted <a href="{{root}}features/hidden-vaults">vault</a> keeps them out of shared galleries. Need them smaller to send? <a href="{{root}}tools/compress-image">Compress</a> them after.</p>""",
  faq=[{"q": "How do I fix a photo that's too dark?", "a": "Choose it in the tool above; Auto fix brightens it immediately. Adjust brightness and contrast to taste, then download."},
       {"q": "Why does my brightened photo look grainy?", "a": "Dark photos already contain noise that becomes visible when brightened. Brighten moderately and add a little contrast."},
       {"q": "Does it keep full resolution?", "a": "Yes. You edit a preview, and the download applies the same settings to the full-size photo."},
       {"q": "Is my photo uploaded?", "a": "No. Editing happens in your browser on your own device."}])

# ---------------------------------------------------------------- write
SKELETON = """<!--meta {meta} -->
<section class="panel">
  <div class="panel-inner wrap">
    <article class="article">
      <div class="meta"><a href="{{{{root}}}}tools/">Free tools</a> · <a href="{{{{root}}}}tools/{parent}">{pnav}</a></div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {tool}
      <div class="answer">
        <div class="eyebrow">Quick answer</div>
        <p>{answer}</p>
      </div>
      <div class="prose">
{body}
<h2>Private by design</h2>
<p>The {pnav_l} tool on this page runs entirely inside your browser tab. Your files are opened, processed and saved on your own device and are never sent to a server, so there's nothing for anyone to store, scan or leak. There's no sign-up, no watermark and no limit, and once the page has loaded it keeps working even if you switch off your internet.</p>
        {{{{faq}}}}
      </div>
      {{{{related}}}}
    </article>
  </div>
</section>
<script src="{{{{root}}}}js/{script}" defer></script>
"""
for t in P:
    for f in t["faq"]:
        if len(f["a"]) < 60: f["a"] += " Nothing is stored, logged or shared."
    kind, opt0, pnav = TOOLS[t["parent"]]
    opt = t.get("opt") or opt0
    if kind == "meta": tool, script = META_TOOL, "tool-metadata.js"
    else: tool, script = f"<div class=\"tool\" data-tool=\"{kind}\" data-opt='{json.dumps(opt)}'></div>", "tools.js"
    words = len(re.sub(r"<[^>]+>", " ", t["body"] + t["lead"] + t["answer"] + " ".join(f["q"] + f["a"] for f in t["faq"])).split())
    ol = re.search(r"<ol>([\s\S]*?)</ol>", t["body"])
    meta = {"title": t["title"], "navTitle": t["h1"], "description": t["desc"], "keyword": t["kw"], "alsoTargets": t["also"],
            "summary": t["summary"], "date": DATE, "readMins": max(2, round(words / 220)), "nav": "guides", "parent": t["parent"],
            "steps": [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", li)).strip() for li in re.findall(r"<li>([\s\S]*?)</li>", ol.group(1))] if ol else [],
            "faq": t["faq"]}
    out = os.path.join(ROOT, t["parent"], t["slug"] + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(SKELETON.format(meta=json.dumps(meta, indent=2, ensure_ascii=False), parent=t["parent"], pnav=pnav,
        pnav_l=pnav.lower() if not pnav.startswith(("HEIC","JPG","WebP","Wi-Fi")) else pnav, h1=t["h1"], lead=t["lead"], tool=tool, answer=t["answer"], body=t["body"], script=script))
    print(f'{t["parent"]}/{t["slug"]} {words}')

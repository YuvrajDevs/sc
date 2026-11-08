"""Writes one page per Sealcloak feature into content/features/. Run: python3 seo/features.py

Every claim here comes from the app's own screens (strings.xml) or seo/facts.json. Edit this file, not the
generated pages, so the feature pages stay consistent with each other.
"""
import json, os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "content", "features")
DATE = "2026-11-08"

F = [
 dict(slug="pattern-lock", order=1, pro=False, keyword="pattern lock for photos",
  title="Pattern lock for photos: a 5×5 grid only you know",
  nav="Pattern lock",
  desc="Sealcloak locks your photos behind its own 5×5 pattern, separate from your phone's lock, with optional fingerprint unlock and growing waits after wrong tries.",
  summary="Its own 5×5 pattern, separate from your phone's lock, with optional fingerprint.",
  lead="Your vault opens with a pattern drawn on a 5×5 grid. It's separate from your phone's screen lock, so people who know your phone PIN still can't get in.",
  answer="Sealcloak uses its own pattern on a 5×5 grid, at least 6 dots long. The pattern is never stored: it's turned into the key that unlocks your vault. Fingerprint or face unlock is optional, and the pattern always keeps working.",
  sections=[
   ("Why 5×5 instead of the usual 3×3", "<p>A 3×3 grid, like most phone lock screens, has a small number of possible patterns, and many people pick the same few shapes. A 5×5 grid has 25 dots, so there are vastly more patterns to choose from, and a 6-dot minimum stops the shortest, easiest-to-guess shapes. The setup screen shows how strong your pattern is as you draw it.</p>"),
   ("Separate from your phone's lock, on purpose", "<p>Most built-in private albums open with the same PIN that unlocks your phone. The people most likely to look are often the ones who already know it. Sealcloak's pattern is its own, and each vault can have a different one.</p>"),
   ("What happens after wrong patterns", "<p>The first 4 wrong patterns in a row are free. After that, the app makes you wait before the next try, and the wait grows each time. Changing the phone's clock doesn't skip it. If you want, you can also turn on <a href=\"{{root}}features/intruder-photos\">intruder photos</a> and, with Pro, <a href=\"{{root}}features/erase-after-wrong-patterns\">erase after wrong patterns</a>.</p>"),
   ("Fingerprint or face, if you want it", "<p>Turn on fingerprint unlock in Settings to open the vault with your fingerprint or face instead of drawing. Android checks the biometric; the app never sees your fingerprint. Your pattern always keeps working, and it's still what protects the files.</p>"),
  ],
  steps=["Install Sealcloak and tap Set up my vault.", "Draw a pattern of at least 6 dots on the 5×5 grid, then draw it again.", "Write down the 9-word recovery phrase on paper.", "Optionally, turn on fingerprint unlock in Settings."],
  faq=[("Can I use a PIN instead of a pattern?", "No. Each vault opens with its own pattern, plus optional fingerprint or face unlock. A pattern on a 5×5 grid has far more combinations than a typical 4-digit PIN."),
       ("What if I forget my pattern?", "Tap Forgot your pattern? and enter the 9-word recovery phrase you saved at setup, then draw a new pattern. Without the phrase, nobody can open the vault, including us."),
       ("Can someone see my pattern from the smudges on the screen?", "Smudge and shoulder-surfing attacks are possible with any pattern. Wipe the screen now and then, draw it out of sight, or use fingerprint unlock in public."),
       ("Is the pattern stored on my phone?", "No. The pattern is turned into a key with Argon2id, a deliberately slow function, and only the result is used to unlock your vault's key. The pattern itself isn't saved anywhere.")]),

 dict(slug="encryption", order=2, pro=False, keyword="encrypt photos",
  title="How Sealcloak encrypts your photos and files",
  nav="Encryption",
  desc="Every file in Sealcloak is encrypted on your phone with AES-256-GCM, under a random key per vault protected by your pattern and the Android Keystore.",
  summary="AES-256-GCM on the phone, a random key per vault, unlocked by your pattern.",
  lead="Hiding a photo and encrypting it are different things. Sealcloak encrypts every file on your phone, so even a copy taken out of the app is unreadable without your key.",
  answer="Each vault has its own random master key. Every file is encrypted with AES-256-GCM before it's saved. The master key is wrapped using a key derived from your pattern with Argon2id and a key held in Android's hardware-backed Keystore. Nothing leaves your phone, because the app has no internet permission.",
  sections=[
   ("Hidden is not the same as encrypted", "<p>Many gallery lock apps move photos to a hidden folder and put a password screen in front. Anyone with a file manager or a computer can still find and open the files. With encryption, the files themselves are scrambled. A copy is useless without the key, wherever it ends up.</p>"),
   ("What happens when you add a photo", "<ol><li>The file is read in chunks and each chunk is encrypted with AES-256-GCM, which also detects any tampering.</li><li>The encrypted file is written to the app's private storage, under a random name that says nothing about what it is.</li><li>The vault's index (names, folders, dates) is encrypted too.</li><li>The original stays in your gallery until you delete it yourself, so you can check the vault copy first.</li></ol>"),
   ("How your pattern unlocks it", "<p>Your pattern is run through Argon2id, a slow, memory-hard function made to resist guessing at scale. The result, together with a key that never leaves Android's Keystore, unwraps your vault's master key. When you lock the vault, the keys are cleared from memory.</p>"),
   ("No server to hack", "<p>Sealcloak has no account, no cloud and no internet permission. There's no copy of your files or keys anywhere except your phone and the <a href=\"{{root}}features/encrypted-backups\">backups</a> you choose to make. Read the full picture on the <a href=\"{{root}}security\">security page</a>.</p>"),
   ("The honest limits", "<p>No security is absolute. A guessable pattern, a phone that's already compromised by malware, or a recovery phrase kept in a photo on the same phone can all undo good encryption. The app's Security checkup in Settings points out the common weak spots.</p>"),
  ],
  steps=[],
  faq=[("Is AES-256 really secure?", "AES-256 is the standard used to protect sensitive data worldwide, and there's no practical attack on it. In practice, the weak points are guessable passwords and patterns, not the cipher."),
       ("Can Sealcloak see my photos?", "No. Encryption happens on your phone, the app can't connect to the internet, and we never have your pattern, phrase or keys."),
       ("If someone copies the app's files, can they open them?", "Not without the key. The files are encrypted, and the key needs your pattern or recovery phrase plus, on the original phone, the Keystore."),
       ("Are my backups encrypted too?", "Yes. A backup file is encrypted with your vault's recovery phrase or a passphrase you choose. Without it, the file can't be opened.")]),

 dict(slug="hidden-vaults", order=3, pro=False, keyword="multiple hidden vaults",
  title="Hidden vaults: separate vaults, each with its own pattern",
  nav="Hidden vaults",
  desc="Keep things apart in separate Sealcloak vaults. Each has its own pattern and recovery phrase, and nothing on screen shows how many exist. Up to 3 free.",
  summary="Separate vaults with their own patterns. Nothing shows how many exist.",
  lead="One vault for everyday private things, another for what really matters. Each opens with its own pattern, and none of them appears in any list.",
  answer="Sealcloak can hold several vaults. Each has its own pattern, recovery phrase and files. You open one by drawing its pattern, and nothing on screen says how many vaults exist. The free plan includes up to 3; Pro removes the limit.",
  sections=[
   ("How it works", "<p>At the lock screen, you just draw a pattern. Whichever vault that pattern belongs to opens. There's no vault picker and no list, so someone who sees one vault has no way to tell whether others exist.</p>"),
   ("Each vault stands alone", "<ul><li>Its own pattern, which must differ from every other pattern.</li><li>Its own 9-word recovery phrase.</li><li>Its own files, folders and name.</li><li>Its own settings, such as fingerprint unlock and intruder photos.</li></ul><p>Opening one vault never reveals another one's files or name.</p>"),
   ("Adding a vault", "<ol><li>In Settings, under More vaults, tap Add a vault.</li><li>Draw your current pattern to confirm it's you.</li><li>Draw the new vault's pattern twice.</li><li>Write down its own recovery phrase.</li><li>Lock the app and draw the new pattern to open it.</li></ol>"),
   ("When to use more than one", "<p>Common setups: one vault for documents (IDs, bank papers) and another for personal photos, or a separate vault for things a partner or family member might ask to see. For the specific case of being forced to unlock, use <a href=\"{{root}}features/coerce\">Coerce</a>, which is designed for it.</p>"),
  ],
  steps=[],
  faq=[("How many vaults can I have?", "Up to 3 on the free plan, and as many as you like with Pro. Each one has its own pattern and recovery phrase."),
       ("Can someone tell how many vaults I have?", "Not from the app. There's no list or picker, and each pattern only opens its own vault."),
       ("Do I need a different recovery phrase for each vault?", "Yes. Each vault gets its own 9-word phrase. Keep all of them on paper."),
       ("What's the difference between a hidden vault and Coerce?", "A hidden vault is just another private vault. A Coerce vault is a harmless decoy meant to be shown when someone forces you to unlock, and it can optionally erase the others.")]),

 dict(slug="coerce", order=4, pro=True, keyword="decoy vault",
  title="Coerce: a decoy vault for when you're forced to unlock",
  nav="Coerce decoy vault",
  desc="Coerce adds a harmless decoy vault with its own pattern, for when someone forces you to unlock. It can optionally erase your other vaults, off by default.",
  summary="A harmless decoy vault with its own pattern, for when someone makes you unlock.",
  lead="If someone forces you to open the app, refusing can make things worse. Coerce gives you a pattern that opens a believable, harmless vault instead.",
  answer="Coerce is a Pro feature that adds a decoy vault with its own pattern. Draw it under pressure and the app opens a vault with a few ordinary files, so you can show there was nothing to hide. Your real vaults stay untouched. Optionally, the Coerce pattern can also erase every other vault, but that's off unless you type PERMIT to allow it.",
  sections=[
   ("Setting it up", "<ol><li>In Settings, tap Set up a Coerce vault and read the explanation.</li><li>Draw your current pattern to confirm it's you.</li><li>Draw a Coerce pattern that looks clearly different from your real one (the app rejects ones that are too close).</li><li>Add a few ordinary files, so the vault looks lived in.</li></ol><p>You can test the Coerce pattern at any time from Settings. The test only checks the pattern; nothing opens or changes.</p>"),
   ("Make it believable", "<p>An empty vault looks suspicious. Add some harmless photos, a document or two and a note. Editing the Coerce vault is safe: a banner reminds you it's the Coerce vault, and nothing is erased while you edit it.</p>"),
   ("The optional erase", "<p>You can choose to make the Coerce pattern erase every other vault when it's drawn at the lock screen. It's off by default and needs you to type the word PERMIT. Erasing is permanent and can't be undone on that phone. Backups you made yourself aren't touched. Think carefully before turning it on, and keep a backup somewhere safe.</p>"),
   ("Limits", "<p>Coerce is camouflage, not magic. Someone who knows the app well may suspect a decoy, and anyone who searches the phone with forensic tools works on a different level. Use it as one layer alongside <a href=\"{{root}}features/encryption\">strong encryption</a> and a pattern nobody knows.</p>"),
  ],
  steps=[],
  faq=[("Does the Coerce vault erase my files by default?", "No. By default it only opens the decoy. Erasing other vaults is a separate option you must turn on by typing PERMIT."),
       ("Can someone tell it's a decoy?", "The app shows nothing that says a vault is a decoy at the lock screen, and nothing shows how many vaults exist. Fill it with ordinary files so it looks real."),
       ("Is Coerce free?", "Coerce is part of Sealcloak Pro, along with calculator mode, a custom icon and unlimited files and vaults."),
       ("What's the difference from the duress mode in other apps?", "The idea is similar. In Sealcloak, the decoy is a real, editable vault with its own pattern, and erasing is opt-in rather than automatic.")]),

 dict(slug="calculator-disguise", order=5, pro=True, keyword="calculator vault", also=["calculator vault app", "app lock calculator", "calculator lock"],
  title="Calculator vault: hide Sealcloak as a working calculator",
  nav="Calculator disguise",
  desc="Turn Sealcloak into a working calculator on your home screen. Type your secret code and hold = for 2 seconds to reach the vault. A wrong code just calculates.",
  summary="A working calculator on your home screen. Your secret code opens the vault.",
  lead="With calculator mode on, Sealcloak looks and works like a plain calculator. Only your secret code, then your pattern, gets anyone into the vault.",
  answer="Calculator mode (Pro) changes the app's icon and name to a calculator. It does real sums. To open the vault, type your 4 to 8 digit secret code and hold = for 2 seconds, then draw your pattern. A wrong code just behaves like a calculator.",
  sections=[
   ("Setting it up", "<ol><li>In Settings, under Disguise, tap Set up calculator mode.</li><li>Choose a secret code of 4 to 8 digits and type it again.</li><li>Tap Open calculator, type your code and hold = for 2 seconds.</li><li>Draw your pattern. Calculator mode turns on once you've got in this way.</li></ol><p>The icon changes when you leave the app. Some phones, such as Samsung and Xiaomi, can take a few seconds or a restart to refresh it.</p>"),
   ("Two locks, not one", "<p>The secret code only opens the calculator's door. Your pattern still protects the vault, and the files are still <a href=\"{{root}}features/encryption\">encrypted</a>. Someone who stumbles on the code still needs the pattern.</p>"),
   ("Forgot the code?", "<p>Press and hold the empty calculator display, then enter your recovery phrase. You can also change the code in Settings at any time.</p>"),
   ("What it can't hide", "<p>In Android Settings → Apps, the real name Sealcloak still shows. Calculator mode is camouflage against a quick look at your home screen, not against someone checking the app list in detail. If you'd rather it look like something other than a calculator, use a <a href=\"{{root}}features/custom-icon\">custom icon</a> instead. More on this in <a href=\"{{root}}guides/hide-apps-on-android\">how to hide apps on Android</a>.</p>"),
  ],
  steps=["In Settings, tap Set up calculator mode.", "Choose a 4 to 8 digit secret code.", "Open the calculator, type the code and hold = for 2 seconds.", "Draw your pattern to finish turning it on."],
  faq=[("Does the calculator actually work?", "Yes. It does normal arithmetic, so it looks ordinary to anyone who tries it."),
       ("What happens if someone types a wrong code?", "Nothing unusual. The calculator just shows the number, like any calculator would."),
       ("How do I turn calculator mode off?", "In Settings, tap Turn off calculator mode. The icon and name change back to Sealcloak and the secret code is deleted."),
       ("Is calculator mode free?", "Calculator mode is part of Sealcloak Pro, along with a custom icon, Coerce and unlimited files and vaults.")]),

 dict(slug="custom-icon", order=6, pro=True, keyword="disguise app icon",
  title="Custom icon: disguise Sealcloak as any app you like",
  nav="Custom icon",
  desc="Put your own picture and name on Sealcloak's home screen icon so it blends in with your other apps. It opens straight to your pattern. A Pro feature.",
  summary="Your own picture and name on the home screen. Opens straight to your pattern.",
  lead="A calculator isn't the only disguise. With a custom icon, Sealcloak can look like a notes app, a game or anything that fits your home screen.",
  answer="Custom icon (Pro) puts a picture and name you choose on your home screen. Tapping it opens straight to your pattern. Once it works, the Sealcloak entry in the app list turns into a plain calculator, so neither place shows the real name at a glance.",
  sections=[
   ("Setting it up", "<ol><li>In Settings, under Custom icon, tap Choose a picture.</li><li>Pick an image and type the name to show under it.</li><li>Tap Add to home screen and confirm.</li><li>Tap Lock and try it, go to your home screen and open the new icon.</li><li>Once your pattern opens the vault from there, the custom icon is on.</li></ol>"),
   ("Pick something that blends in", "<p>The best disguise is one nobody looks at twice. Match the style of the apps already on your home screen, and pick a name that fits the picture.</p>"),
   ("If you delete the icon by accident", "<p>The app shows a recovery dial code when you set it up. Dial it in your phone app to bring the normal Sealcloak icon back. Note that your launcher's own confirmation may show the name Sealcloak once when the icon is added.</p>"),
   ("Limits", "<p>Some home screens don't let apps add icons; the app tells you if yours doesn't. And like any disguise, Android's Settings → Apps list still shows the real name. Compare with <a href=\"{{root}}features/calculator-disguise\">calculator mode</a>, or read <a href=\"{{root}}guides/hide-apps-on-android\">how to hide apps on Android</a> for other approaches.</p>"),
  ],
  steps=[],
  faq=[("Can I change the icon later?", "Yes. Turn the custom icon off in Settings and choose a new picture and name."),
       ("Does it still need my pattern?", "Yes. The icon only changes how the app looks. Opening it goes straight to your pattern."),
       ("Why does my phone show the name Sealcloak once?", "Some launchers show the app's real name in their own confirmation when a shortcut is added. After that, only your chosen name shows."),
       ("What happens to the app list entry?", "Once your custom icon is working, the Sealcloak entry in the app list turns into a plain calculator, so the real name doesn't show there at a glance either.")]),

 dict(slug="intruder-photos", order=7, pro=False, keyword="intruder photos", also=["intruder selfie", "intruder selfie app"],
  title="Intruder photos: see who tried to open your vault",
  nav="Intruder photos",
  desc="Turn on intruder photos and Sealcloak's front camera quietly photographs repeated wrong patterns. Only your vault can see the photos, after you unlock.",
  summary="From the 3rd wrong pattern in a row, the front camera photographs each attempt.",
  lead="Wondering whether someone tried to get into your vault? Intruder photos answer that, with a picture of who it was.",
  answer="With intruder photos on, Sealcloak forgives the first two wrong patterns, then takes a front-camera photo of every wrong attempt from the third in a row. The photos are encrypted so that only the vault that turned the feature on can open them, and you see them after you unlock.",
  sections=[
   ("Turning it on", "<ol><li>In Settings, under Security, find Intruder photos and tap Turn on.</li><li>Allow camera access when asked.</li><li>That's it. Settings shows how many photos are waiting.</li></ol>"),
   ("Why the first two are forgiven", "<p>Everyone slips when drawing a pattern sometimes. Photographing every single mistake would fill the folder with pictures of you. The growing waits after wrong tries are explained under <a href=\"{{root}}features/pattern-lock\">pattern lock</a>. From the third wrong pattern in a row, it's much more likely to be someone else.</p>"),
   ("Private even while locked", "<p>While the vault is locked, the app has no key to read your files. Intruder photos are sealed to a public key: the app can add a photo, but only your unlocked vault can open them. They never appear in your gallery or in a notification. After you unlock, a banner tells you how many wrong attempts were photographed.</p>"),
   ("The camera indicator", "<p>On Android 12 and newer, the phone shows its own green camera dot whenever any app uses the camera. That's an Android privacy feature, and no app can hide it. The photo is taken quickly, so the dot only appears briefly.</p>"),
   ("Use it lawfully", "<p>Rules about photographing other people differ by country. You're responsible for using this feature lawfully where you live. More in our <a href=\"{{root}}terms\">terms</a>.</p>"),
  ],
  steps=[],
  faq=[("Does it take a photo on my own mistakes?", "Only from the third wrong pattern in a row. Unlock successfully and the count starts again."),
       ("Where are intruder photos stored?", "Encrypted in the app's private storage. They never go to your gallery and never leave the phone."),
       ("Can the intruder see that a photo was taken?", "There's no sound or message from the app, but Android shows its camera indicator dot briefly while the camera is in use."),
       ("How many photos are kept?", "The newest 20. Older ones are removed so a long attack can't fill your phone.")]),

 dict(slug="recovery-phrase", order=8, pro=False, keyword="vault recovery phrase",
  title="Vault recovery phrase: get back in if you forget your pattern",
  nav="Recovery phrase",
  desc="Every Sealcloak vault has a 9-word recovery phrase. If you forget your pattern, it gets you back in. Without it, nobody can open the vault, us included.",
  summary="9 words that get you back in. Without them, nobody can open the vault.",
  lead="Strong encryption means there's no back door. Your recovery phrase is the way back in that only you hold.",
  answer="When you set up a vault, Sealcloak shows a 9-word recovery phrase and checks you've written it down. If you forget your pattern, tap Forgot your pattern?, enter the phrase and draw a new one. The phrase also unlocks backups. Without the pattern or the phrase, nobody can open the vault, including us.",
  sections=[
   ("Recovering a forgotten pattern", "<ol><li>On the pattern screen, tap Forgot your pattern?</li><li>Enter your 9 recovery words.</li><li>Draw a new pattern, then draw it again.</li><li>Your vault opens with all its files.</li></ol>"),
   ("Why there's no 'reset by email'", "<p>A reset link needs a company that holds a key to your files. Sealcloak has no account and no server, and your files are <a href=\"{{root}}features/encryption\">encrypted</a> on your phone. That's what keeps them private, and it's also why the phrase matters so much.</p>"),
   ("Random words or your own sentence", "<p>At setup, Sealcloak gives you 9 random words. You can choose to write your own sentence of six words or more instead. Random words are harder to guess; a sentence of your own can be easier to remember. Either way, it's the only way back in.</p>"),
   ("Where to keep it", "<ul><li>On paper, somewhere safe at home.</li><li>Not in a note, photo, screenshot or message on the same phone.</li><li>One phrase per vault: label each one so you know which is which.</li></ul>"),
   ("It also protects your backups", "<p>When you <a href=\"{{root}}features/encrypted-backups\">export a backup</a>, the recommended choice locks it with your recovery phrase. Entering it also checks you still have the right words.</p>"),
  ],
  steps=[],
  faq=[("Can Sealcloak reset my pattern if I lose the phrase?", "No. Nobody holds a copy of your keys, so without the pattern or the phrase the vault can't be opened."),
       ("Can I see my recovery phrase again later?", "Write it down at setup. For safety, the phrase isn't something you should store on the same phone as the vault."),
       ("Does each vault have its own phrase?", "Yes. Every vault, including extra hidden vaults, has its own phrase."),
       ("What if a system update resets the phone's security key?", "The app tells you, and your recovery phrase gets you back in.")]),

 dict(slug="encrypted-backups", order=9, pro=False, keyword="photo vault backup",
  title="Encrypted backups: move your vault to a new phone",
  nav="Encrypted backups",
  desc="Back up your Sealcloak vault as one encrypted file, by hand or weekly or monthly, to a folder you choose. Restore it on a new phone with your phrase.",
  summary="One encrypted file, by hand or on a schedule. Restore on any phone.",
  lead="An offline vault needs a plan for lost or broken phones. Sealcloak's backups are single encrypted files you keep wherever you like.",
  answer="Export a backup in Settings and Sealcloak writes one encrypted file to a folder you choose, then checks it can be read back. Lock it with your recovery phrase or a passphrase. To restore, install Sealcloak on the new phone, choose Restore from a backup and enter the same phrase or passphrase. Scheduled backups can run weekly or monthly on their own.",
  sections=[
   ("Making a backup", "<ol><li>In Settings, under Backup, tap Export backup.</li><li>Choose Use my recovery phrase (recommended) or a passphrase of at least 8 characters.</li><li>Pick where to save the file.</li><li>Wait for Backup verified. The app reads the file back to check it.</li></ol>"),
   ("Scheduled backups", "<p>Set up a scheduled backup to save a file by itself every week or month, to a folder you choose. If that folder is one your Drive or another sync app watches, the encrypted file goes off-phone automatically, without Sealcloak itself ever touching the internet.</p>"),
   ("Restoring on a new phone", "<ol><li>Copy the backup file to the new phone.</li><li>Install Sealcloak and tap Restore from a backup.</li><li>Set a pattern for the new vault and note its recovery phrase.</li><li>Choose the backup file and enter its phrase or passphrase.</li></ol><p>Importing is safe to repeat: files you already have are skipped.</p>"),
   ("Keep the file safe", "<p>The file is encrypted, but it's only as private as the place you keep it, and anyone with both the file and its key can open it. Keep the key on paper, separate from the file. The app's Security checkup reminds you if there's no recent backup. Lost the phrase too? See <a href=\"{{root}}features/recovery-phrase\">recovery phrase</a>.</p>"),
  ],
  steps=[],
  faq=[("Does Sealcloak upload my backups?", "No. The app has no internet permission. It saves the file where you choose; moving it anywhere else is up to you."),
       ("Can I open a backup without the phrase?", "No. A backup opens only with the recovery phrase or passphrase used to make it."),
       ("Will restoring twice duplicate my files?", "No. Files that are already in the vault are skipped, so importing the same backup again is safe."),
       ("What happens if a backup is damaged?", "Sealcloak restores everything it can read and tells you how many files couldn't be restored.")]),

 dict(slug="private-camera-and-scanner", order=10, pro=False, keyword="private camera app",
  title="Private camera and document scanner",
  nav="Camera and scanner",
  desc="Take photos and videos from inside Sealcloak and they're saved straight into your encrypted vault, not your gallery. Scan documents into a PDF too.",
  summary="Capture photos, videos and scans straight into the vault.",
  lead="The safest private photo is one that never lands in your gallery in the first place.",
  answer="From the add menu, choose Take a photo, Record a video or Scan a document. The capture is saved straight into your encrypted vault, not your gallery. Sealcloak uses your phone's camera app to capture, and some camera apps keep a copy of their own, so check yours the first time.",
  sections=[
   ("Photos and videos", "<ol><li>Tap + in the vault.</li><li>Choose Take a photo or Record a video.</li><li>Take the shot in your camera app and confirm.</li><li>It appears in the vault, encrypted.</li></ol>"),
   ("Scanning documents", "<ol><li>Tap + and choose Scan a document.</li><li>Take a picture of the page.</li><li>Drag the four dots onto the corners of the paper.</li><li>Choose black and white or colour, then add more pages if you need to.</li><li>Tap Save as PDF.</li></ol><p>Good for IDs, bank papers, medical letters and anything you'd rather not leave as loose photos.</p>"),
   ("Notes too", "<p>Write a note from the same menu. It's encrypted when you save it, like everything else in the vault.</p>"),
   ("Check your camera app once", "<p>Because the capture goes through your phone's camera app, a few camera apps save their own copy as well. Take one test photo and look in your gallery. If a copy appears, delete it and consider a different camera app. Read more in <a href=\"{{root}}guides/how-to-hide-photos-on-android\">how to hide photos on Android</a>.</p>"),
  ],
  steps=[],
  faq=[("Do photos taken in Sealcloak appear in my gallery?", "They're saved into the vault, not the gallery. Some camera apps keep their own copy, so check once with a test photo."),
       ("What format do scans use?", "Scans are saved as a PDF, with one page for each picture you keep, in black and white or colour."),
       ("Can I scan several pages into one PDF?", "Yes. Add as many pages as you need before tapping Save as PDF."),
       ("Are notes encrypted?", "Yes. Notes are encrypted when you save them, like every other file in the vault.")]),

 dict(slug="erase-after-wrong-patterns", order=11, pro=True, keyword="self destruct vault",
  title="Erase after wrong patterns: an optional self-destruct",
  nav="Erase after wrong patterns",
  desc="An optional Pro setting that erases every vault on the phone after a set number of wrong patterns in a row. Off by default; you type PERMIT to turn it on.",
  summary="Optional: erase everything after too many wrong patterns. Off by default.",
  lead="For people who'd rather lose the files than have them found. It's powerful, so it's off unless you deliberately turn it on.",
  answer="Erase after wrong patterns (Pro) wipes every vault and file on the phone if someone draws the wrong pattern a set number of times in a row. It can't be undone, not even with your recovery phrase. It's off by default, and turning it on requires typing the word PERMIT.",
  sections=[
   ("Turning it on", "<ol><li>In Settings, under Security, find Erase after wrong patterns and tap Turn on.</li><li>Read the warning and choose how many wrong patterns in a row should trigger it.</li><li>Type PERMIT to confirm.</li></ol>"),
   ("Think before you do", "<p>You can lock yourself out by mistake, for example if a child plays with your phone. Erasing is immediate and permanent on that phone. Before turning it on, make an <a href=\"{{root}}features/encrypted-backups\">encrypted backup</a> and keep it somewhere safe.</p>"),
   ("What gets erased", "<p>Everything Sealcloak holds on that phone: every vault, every file and every intruder photo. Your recovery phrases can't bring them back afterwards, because the encrypted data itself is gone.</p>"),
   ("How it fits with the other protections", "<p>The first wrong patterns already trigger growing waits, and <a href=\"{{root}}features/intruder-photos\">intruder photos</a> can show you who tried. Erase is the last line, for situations where the risk of exposure is worse than losing the files.</p>"),
  ],
  steps=[],
  faq=[("Can I get my files back after an erase?", "Not on that phone. Only a backup you made beforehand can bring them back."),
       ("Is it on by default?", "No. It stays off until you turn it on in Settings and type the word PERMIT to confirm."),
       ("Does it erase my backups?", "No. Backup files you saved outside the app aren't touched, which is why making one first is so important."),
       ("Can I turn it off later?", "Yes. Turn it off at any time in Settings, under Erase after wrong patterns.")]),

 dict(slug="secure-sharing", order=12, pro=False, keyword="share photos securely",
  title="Share files securely as a passphrase-locked package",
  nav="Secure sharing",
  desc="Share photos and files from Sealcloak as one passphrase-locked package. Send it with any app and the passphrase separately. Only someone with both can open it.",
  summary="One passphrase-locked file. Send it with any app, and the passphrase separately.",
  lead="Sometimes a private file needs to reach one other person. Sealcloak packs it into an encrypted file that only the passphrase opens.",
  answer="Select files or a folder in your vault and choose Share securely. Sealcloak makes one encrypted package locked with a passphrase you choose. Send the file with any app you like, and give the passphrase in a separate message. The other person imports it into Sealcloak with the passphrase.",
  sections=[
   ("Sending", "<ol><li>Press and hold a file, or select several, or open a folder and choose Share this folder.</li><li>Choose Share securely and set a passphrase.</li><li>Send the package with WhatsApp, email, Drive or any other app.</li><li>Give the passphrase another way: in person, by call or in a different app.</li></ol>"),
   ("Receiving", "<p>The other person opens Sealcloak, chooses Import backup in Settings, picks the package and enters the passphrase. The files land in their vault, encrypted.</p>"),
   ("Good uses", "<p>Sending ID scans to a family member, sharing medical documents with someone you trust, or moving a few files from your vault to another phone without making a full backup.</p>"),
   ("Why separate channels matter", "<p>Anyone with both the file and the passphrase can open it. Sending them together in one chat means one leak exposes both. Splitting them across channels is what makes the package safe in transit. For other ways to share privately, see <a href=\"{{root}}guides/photo-vault-app-without-account\">vault apps without an account</a>.</p>"),
  ],
  steps=[],
  faq=[("Does the other person need Sealcloak?", "Yes. The package is opened by importing it into Sealcloak with the passphrase."),
       ("Is the package uploaded anywhere by Sealcloak?", "No. Sealcloak only creates the file. You send it with whatever app you choose."),
       ("Can I share a whole folder?", "Yes. Open the folder and choose Share this folder to pack everything in it into one package."),
       ("What if someone gets the file but not the passphrase?", "They can't open it. The contents are encrypted and only the passphrase unlocks them.")]),
]

def render(f):
    meta = {"title": f["title"], "navTitle": f["nav"], "description": f["desc"], "keyword": f["keyword"],
            **({"alsoTargets": f["also"]} if f.get("also") else {}),
            "summary": f["summary"], "date": DATE, "readMins": 4, "nav": "features", "order": f["order"],
            "faq": [{"q": q, "a": a} for q, a in f["faq"]]}
    if f["steps"]: meta["steps"] = f["steps"]
    pro = ' <span class="pro">PRO</span>' if f["pro"] else ""
    secs = "\n\n".join(f"        <h2>{html.escape(h)}</h2>\n        {b}" for h, b in f["sections"])
    mid = secs.split("\n\n")
    body = "\n\n".join(mid[:2]) + "\n\n        {{cta}}\n\n" + "\n\n".join(mid[2:])
    return f"""<!--meta {json.dumps(meta, ensure_ascii=False, indent=2)} -->
<section class="panel">
  <div class="panel-inner wrap">
    <article class="article">
      <div class="meta"><a href="{{{{root}}}}features">Features</a> · {html.escape(f["nav"])}{pro}</div>
      <h1>{html.escape(f["title"])}</h1>
      <p class="lead">{html.escape(f["lead"])}</p>
      <div class="answer">
        <div class="eyebrow">In short</div>
        <p>{html.escape(f["answer"])}</p>
      </div>
      <div class="prose">
{body}
        {{{{faq}}}}
      </div>
      {{{{related}}}}
    </article>
  </div>
</section>
"""

os.makedirs(OUT, exist_ok=True)
for f in F:
    open(os.path.join(OUT, f["slug"] + ".html"), "w").write(render(f))
print(f"Wrote {len(F)} feature pages.")

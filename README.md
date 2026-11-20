# CivitAI Browser+ (civitai.red edition)

**A fork of [sd-civitai-browser-plus](https://github.com/BlafKing/sd-civitai-browser-plus), updated to keep working after Civitai's 2026 changes.**

This fork is based on [nohupwork/sd-civitai-browser-plus](https://github.com/nohupwork/sd-civitai-browser-plus) (previously TheSlateGray's fork), which merged pending pull requests from the original project. Both upstream repositories are archived, so this fork carries the fixes needed for the current Civitai site and API.

Made and tested for **Stable Diffusion WebUI Forge Neo**.

![CivitAI Browser+](https://github.com/BlafKing/sd-civitai-browser-plus/assets/9644716/95afcc41-56f0-4398-8779-51cb2a9e2f55)

---

## What's new in this fork ✨

### civitai.red support 🔴
In 2026 Civitai split into two sites: `civitai.com` is now SFW only, and the full catalogue moved to `civitai.red`. The original extension still queried `civitai.com`, so most models disappeared from searches and update scans.

* All API requests, model links and downloads now use `civitai.red`.
* Pasting either a `civitai.com` or a `civitai.red` model link in the search box works.

### Smarter update detection 🔄
The original update scan assumed that the first version listed on a model page is the newest one. On Civitai the creator chooses that order, so the scan often showed models as up to date when they weren't, or as outdated when they weren't. The scan now works like this:

1. It identifies the version you have installed by its SHA256 hash (with the version ID from the `.json` file as a fallback).
2. It looks up the model on Civitai and reads the **publish date** of every version.
3. A version counts as an update only if it was **published after the newest version you have** and its **base model is in your Base Model filter** (for example Pony, Illustrious and NoobAI).

So if you have the Pony version of a LoRA and the creator later publishes an Illustrious version, it shows up as an update only if Illustrious is in your filter. New versions for bases you don't use (Flux, Anima, Wan and so on) are ignored.

The orange and green glow on model cards follows the same rule, so the cards always agree with the scan.

### Hides versions you can't download 🔒
Updates are skipped when the newest version can't be downloaded for free:

* **Early Access** versions (timed).
* **Paid** versions sold with Buzz (Civitai's `paidAccess`, including permanent paid access).
* **Site-only** versions, which the creator restricted to on-site generation (`usageControl: "Generation"`).

Paid and Early Access versions are controlled by the existing **"Hide early access models"** option. Site-only versions are always skipped, because they can never be downloaded.

### Bulk updating works ✅
* **Select All** now appears when you load the update results, so you can select every outdated model at once.
* **Download all selected** now downloads the actual update version found by the scan. The original always downloaded the first version on the model page, which was often the version you already had, or one for a different base model.
* If an Aria2 download fails, the extension retries the file with the standard downloader and prints Aria2's error message instead of a generic error.
* The pause between queued downloads was reduced from 2 seconds to 0.5 seconds.

### Download and scan log 📝
Everything the extension prints to the console is also written to `scripts/civitai_browser.log`, including the HTTP status of each download link and errors that used to be silent. Lines older than 7 days are removed automatically when the WebUI starts.

### Security fixes 🛡️
* **Aria2 RPC is no longer exposed to the network.** The original started Aria2 listening on all network interfaces with a hard-coded secret, so anyone on the same network could tell it to download files to any folder. It now listens on localhost only, with a random secret generated at every start.
* **Download certificates are verified.** The original disabled TLS certificate checks in Aria2.
* **Model names and descriptions from Civitai are sanitized** before being shown, so a malicious model name, version name or description can't run scripts in the WebUI.
* **Safe zip extraction.** When "unpack zip" is enabled, zips containing paths outside the model folder are refused, and password-protected zips no longer freeze the WebUI waiting for a password in the console.
* **A failed download only cleans up its own files.** The original searched every subfolder and permanently deleted any file with the same name, which could remove another model.

### Other fixes 🛠️
* Every network request now has a timeout, so a server that stops responding can't freeze a download or scan.
* Fixed a crash when using a proxy with a custom CA bundle.
* Forge Neo: folder options given as lists are handled.
* Fixed `400 Bad Request` errors when scanning many models: model IDs are now sent as a comma-separated list, as the API expects.
* Fixed a startup crash when Civitai returns an empty response while loading the base model list.
* Models whose local `.json` says "Model not found" are skipped instead of showing up as false updates.

---

## How to use the update scan 🔍

1. Open the **CivitAI Browser+** tab and set the **Base model** filter to the bases you use. Save it as your default with **Save settings as default** if you like.
2. Go to **Update Models** and click **Scan for available updates**.
3. Click **Load outdated models to browser**. Outdated models have an orange glow.
4. Click **Select All**, then **Download all selected**.
5. Run the scan again: the models you downloaded disappear from the list.

**Tip:** set your Civitai API key in **Settings → CivitAI Browser+**. Many models on `civitai.red` require it to download.

---

## Known limitations ⚠️

* **Variants count as updates.** Some creators publish different concepts or styles as "versions" of the same model (for example a color and a black-and-white version, or two different epochs). The API has no way to tell those apart from real updates, so a variant published later shows up as an update.
* **Checking for site-only versions needs one extra API request** per update candidate. The requests run in parallel and are cached, but scans with many results take a few seconds longer.
* When a model has several newer versions in your filter, **Download all selected** downloads only the newest one.

### Unable to download / frozen download

If downloads keep failing, check `scripts/civitai_browser.log` for the reason. You can also try:

1. **Disable "Download models using Aria2"** to use the standard downloader.
   ![Revert to old download method](https://github.com/BlafKing/sd-civitai-browser-plus/assets/9644716/982b0ebb-0cac-4053-8060-285533e0e176)
2. **Enable "Disable Async DNS for Aria2"** if you use a DNS manager such as PortMaster.
   ![Disable Async DNS for Aria2](https://github.com/BlafKing/sd-civitai-browser-plus/assets/9644716/3cf7fab3-0df5-4995-9543-d9824b7931ff)

Both options are under **Settings → CivitAI Browser+**.

---

## Installation 📘

### From the WebUI
1. Go to **Extensions → Install from URL**.
2. Paste the URL of this repository and click **Install**.
3. Restart the WebUI.

### Manual
1. Download this repository as a `.zip` and unpack it.
2. Place the folder inside your WebUI's `extensions` folder.
3. If you already have another copy of CivitAI Browser+, remove or disable it, so the two don't conflict.
4. Restart the WebUI completely. **Reload UI** is not enough for the extension's Python files.

---

## Original features 🚀

* Browse all models from Civitai.
* See installed and outdated models while browsing, and scan all installed models for updates.
* Download any model, version and file, with a download queue.
* Automatically assign tags to installed models.
* Load any model card from txt2img/img2img into the extension, and send an image's generation info to txt2img.
* High-speed downloads with Aria2.

---

## Changelog 📋

### 2026-11-19
* Site-only versions (`usageControl: "Generation"`) are no longer offered as updates or downloaded.
* Security review: Aria2 RPC restricted to localhost with a random secret, TLS verification enabled, HTML and JavaScript escaping of Civitai data, safe zip extraction, safer cleanup of failed downloads.
* Stability: timeouts on all network requests, proxy CA bundle fix, Forge Neo folder options.
* Speed: the site-only check runs in one parallel batch per scan or page.

### 2026-11-04
* Switched all API requests and links to `civitai.red`.
* New update detection based on publish date and the Base Model filter.
* Hide paid (`paidAccess`) and Early Access versions from updates.
* Card colors follow the same update rule as the scan.
* **Download all selected** downloads the version found by the scan.
* **Select All** button visible when loading update results.
* Aria2 error messages and automatic retry with the standard downloader.
* Log file `scripts/civitai_browser.log` with 7-day retention.
* Shorter pause between queued downloads.
* Fixed `400` errors on bulk model lookups and a crash on empty API responses.

### Earlier versions
See the [original repository](https://github.com/BlafKing/sd-civitai-browser-plus) for the history up to v3.6.0.

---

## Credits 🙏

* [BlafKing](https://github.com/BlafKing/sd-civitai-browser-plus): original CivitAI Browser+.
* [SignalFlagZ](https://github.com/SignalFlagZ/sd-civitai-browser): the project CivitAI Browser+ was forked from.
* [nohupwork (TheSlateGray)](https://github.com/nohupwork/sd-civitai-browser-plus): fork with merged pull requests that this version is based on.

Licensed under the GNU AGPL v3, the same license as the original project (see [LICENSE](LICENSE)).

from modules.shared import opts  # type: ignore
do_debug_print = getattr(opts, "civitai_debug_prints", False)


def init():
    import warnings
    import os
    import json
    from urllib3.exceptions import InsecureRequestWarning
    warnings.simplefilter('ignore', InsecureRequestWarning)

    # config_folder = os.path.join(os.getcwd(), "config_states")
    # if not os.path.exists(config_folder):
    #     os.mkdir(config_folder)
    config_folder = os.path.dirname(os.path.abspath(__file__))

    global download_queue, last_version, cancel_status, recent_model, last_url, json_data, json_info, main_folder, previous_inputs, download_fail, sortNewest, isDownloading, old_download, scan_files, from_update_tab, url_list, print, subfolder_json

    cancel_status = None
    recent_model = None
    json_data = None
    json_info = None
    main_folder = None
    previous_inputs = None
    last_version = None
    url_list = {}
    download_queue = []

    subfolder_json = os.path.join(config_folder, "civitai_subfolders.json")
    if not os.path.exists(subfolder_json):
        with open(subfolder_json, 'w') as json_file:
            json.dump({}, json_file)

    from_update_tab = False
    scan_files = False
    download_fail = False
    sortNewest = False
    isDownloading = False
    old_download = False


_print = print

# Everything the extension prints is also appended to this file, so problems
# can be diagnosed without copying the console by hand.
import os as _os
import datetime as _dt
_log_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "civitai_browser.log")


_LOG_KEEP_DAYS = 7


def _prune_log():
    # Drop log lines older than _LOG_KEEP_DAYS. Runs once when Forge starts.
    try:
        if not _os.path.exists(_log_path):
            return
        cutoff = _dt.datetime.now() - _dt.timedelta(days=_LOG_KEEP_DAYS)
        with open(_log_path, "r", encoding="utf-8", errors="replace") as _f:
            lines = _f.readlines()
        kept = []
        keep = False
        for line in lines:
            try:
                keep = _dt.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S") >= cutoff
            except ValueError:
                pass  # continuation of a multi-line message: follow the previous line
            if keep:
                kept.append(line)
        if len(kept) != len(lines):
            with open(_log_path, "w", encoding="utf-8") as _f:
                _f.writelines(kept)
    except Exception:
        pass


_prune_log()


def _log(message):
    try:
        with open(_log_path, "a", encoding="utf-8") as _f:
            _f.write(f"{_dt.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
    except Exception:
        pass


def print(print_message):
    _print(f'\033[96mCivitAI Browser+\033[0m: {print_message}')
    _log(print_message)


def debug_print(print_message):
    if do_debug_print:
        _print(f'\033[96m[DEBUG] CivitAI Browser+\033[0m: {print_message}')
    _log(f"[DEBUG] {print_message}")

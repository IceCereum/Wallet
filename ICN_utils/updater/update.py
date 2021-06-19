from tqdm.auto import tqdm
import functools, shutil, requests, pathlib

# upstream = "https://raw.githubusercontent.com/IceCereum/Wallet/main/version.txt"
upstream = "http://127.0.0.1:3001/version.txt"

def get_latest_details():
    response = requests.get(url=upstream)
    details = response.text.split("\n")

    version = details[0]
    url = details[1]
    info = details[2]

    return (version, url, info)

def check_update(current_version : str):
    version, url, info = get_latest_details()

    if version == current_version:
        return (False, version, url, info)
    else:
        return (True, version, url, info)

def download(url, filename):
    """https://stackoverflow.com/a/63831344"""
    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(r.raw.read, decode_content=True)
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)

    return path

def update_wallet(url : str):
    file_name = url.split("/")[-1]
    download(url, file_name)
    return file_name

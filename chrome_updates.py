"""Fetch latest Chrome release versions for multiple channels using ChromiumDash."""

import json
from urllib.request import urlopen
from urllib.error import HTTPError

# New public API replacing the deprecated OmahaProxy service
BASE_URL = "https://chromiumdash.appspot.com/fetch_releases?channel={channel}"

CHANNELS = ["stable", "beta", "dev", "canary"]

def fetch_versions():
    """Return a dict mapping release channels to platform/version pairs."""
    versions = {channel: {} for channel in CHANNELS}

    for channel in CHANNELS:
        url = BASE_URL.format(channel=channel)
        try:
            with urlopen(url) as resp:
                data = json.load(resp)
        except HTTPError as exc:
            raise RuntimeError(f"Failed fetching {channel}: {exc}") from exc

        for item in data:
            platform = item.get("platform") or item.get("os")
            version = item.get("version") or item.get("current_version")
            if platform and version:
                versions[channel][platform] = version

    return versions

if __name__ == "__main__":
    versions = fetch_versions()
    print(json.dumps(versions, indent=2))

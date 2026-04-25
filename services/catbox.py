# Made by @codexnano from scratch.
# If you find any bugs, please let us know in the channel updates.
# You can 'git pull' to stay updated with the latest changes.

import aiohttp
import aiofiles
import logging
import mimetypes
import os
from pathlib import Path

log = logging.getLogger(__name__)


class Catbox:
    CATBOX_API = "https://catbox.moe/user/api.php"
    TELEGRAPH_API = "https://telegra.ph/upload"

    @staticmethod
    async def _upload_catbox(file_path, session):
        """Upload to Catbox. Returns URL on success, else None."""
        try:
            async with aiofiles.open(file_path, "rb") as f:
                file_content = await f.read()

            data = aiohttp.FormData()
            data.add_field("reqtype", "fileupload")

            # Optional authenticated uploads can be more stable than anonymous uploads.
            userhash = os.getenv("CATBOX_USERHASH")
            if userhash:
                data.add_field("userhash", userhash)

            content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            data.add_field(
                "fileToUpload",
                file_content,
                filename=Path(file_path).name,
                content_type=content_type,
            )

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }

            timeout = aiohttp.ClientTimeout(total=45)
            async with session.post(Catbox.CATBOX_API, data=data, headers=headers, timeout=timeout) as resp:
                body = (await resp.text()).strip()
                if resp.status == 200 and body.startswith("http"):
                    return body
                log.warning(f"Catbox upload rejected: HTTP {resp.status}, body={body[:250]}")
                return None
        except Exception as e:
            log.warning(f"Catbox upload exception: {e}")
            return None

    @staticmethod
    async def _upload_telegraph(file_path, session):
        """Fallback upload to telegra.ph. Returns URL on success, else None."""
        try:
            async with aiofiles.open(file_path, "rb") as f:
                file_content = await f.read()

            content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            data = aiohttp.FormData()
            data.add_field(
                "file",
                file_content,
                filename=Path(file_path).name,
                content_type=content_type,
            )
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            timeout = aiohttp.ClientTimeout(total=45)
            async with session.post(Catbox.TELEGRAPH_API, data=data, headers=headers, timeout=timeout) as resp:
                text = (await resp.text()).strip()
                if resp.status != 200:
                    log.warning(f"Telegraph upload rejected: HTTP {resp.status}, body={text[:250]}")
                    return None

                try:
                    payload = await resp.json(content_type=None)
                except Exception:
                    log.warning(f"Telegraph response was not JSON: {text[:250]}")
                    return None

                if isinstance(payload, list) and payload and payload[0].get("src"):
                    src = payload[0]["src"]
                    return src if src.startswith("http") else f"https://telegra.ph{src}"

                if isinstance(payload, dict) and payload.get("src"):
                    src = payload["src"]
                    return src if src.startswith("http") else f"https://telegra.ph{src}"

                log.warning(f"Telegraph upload invalid payload: {str(payload)[:250]}")
                return None
        except Exception as e:
            log.warning(f"Telegraph upload exception: {e}")
            return None

    @staticmethod
    async def upload(file_path, session=None, max_retries=2):
        """
        Upload with provider fallback:
        1) Catbox
        2) Telegraph
        """
        _close = False
        if session is None:
            session = aiohttp.ClientSession()
            _close = True

        try:
            for attempt in range(max_retries):
                url = await Catbox._upload_catbox(file_path, session)
                if url:
                    return url
                log.warning(f"Catbox attempt {attempt + 1}/{max_retries} failed for {Path(file_path).name}")

            # Fallback provider
            t_url = await Catbox._upload_telegraph(file_path, session)
            if t_url:
                log.info(f"Fallback upload succeeded via telegra.ph for {Path(file_path).name}")
                return t_url

            log.error(f"All upload providers failed for {Path(file_path).name}")
            return None
        finally:
            if _close:
                await session.close()

    @staticmethod
    async def download(url, dest_path, session=None, max_retries=3):
        import asyncio

        for attempt in range(max_retries):
            try:
                _close = False
                if session is None:
                    session = aiohttp.ClientSession()
                    _close = True
                try:
                    headers = {
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
                        )
                    }
                    async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        if resp.status == 200:
                            Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
                            async with aiofiles.open(dest_path, "wb") as f:
                                await f.write(await resp.read())
                            return True
                        log.warning(f"Catbox download HTTP {resp.status} (attempt {attempt+1})")
                finally:
                    if _close:
                        await session.close()
            except Exception as e:
                log.warning(f"Catbox download error (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1 * (attempt + 1))
        log.error(f"Catbox download failed after {max_retries} retries: {url}")
        return False

"""Generates OPML file from feeds."""

import os

import aiofiles


from typing import List


def _get_dump_path():
    home_dir = (
        os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        if os.name == "nt"
        else os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
    )
    return os.path.join(home_dir, "zhihu_feeds.xml")


async def dump(feeds: List[str]):
    feed_section = "\n".join([f"<outline xmlUrl='{feed}' />" for feed in feeds])
    opml_text = f"""
        <opml version="2.0">
        	<body>
        		<outline text="Subscriptions" title="Subscriptions">
                    {feed_section}
        		</outline>
        	</body>
        </opml>
        """

    print(opml_text)

    async with aiofiles.open(_get_dump_path(), "wt") as f:
        await f.write(opml_text)

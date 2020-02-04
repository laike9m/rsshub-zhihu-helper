"""Controls headless Chrome."""

import json

import pyppeteer


async def search_users(search_term: str, max_result_num=5):
    """Searches users on zhihu with given search term.

    This function has to be async because pyppeteer only supports async usage.
    """

    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(f"https://www.zhihu.com/api/v4/search_v3?t=people&q={search_term}")
    await page.waitForSelector("pre")

    search_results = await page.evaluate(
        """
        () => {
            return document.querySelector("pre").innerHTML;
        }
        """
    )
    await browser.close()

    search_results = json.loads(search_results)
    users_info = []
    for i, result in enumerate(search_results["data"]):
        if i >= max_result_num:
            break
        user_object = result["object"]
        users_info.append(
            {
                "name": user_object["name"].replace("<em>", "").replace("</em>", ""),
                "url_token": user_object["url_token"],
                "avatar_url": user_object["avatar_url"],
            }
        )

    return users_info

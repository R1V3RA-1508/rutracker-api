from selectolax.lexbor import LexborHTMLParser
import httpx
import re
from models import Topic
from models.errors import NotExistsError, NetworkError
from parser import threadUrl, ajaxUrl


async def getPostBody(client: httpx.AsyncClient, tree: LexborHTMLParser):
    try:
        Id = tree.css('tbody[id^="post_"]')[0].attrs.get("id").split("_")[1]
    except IndexError:
        raise NotExistsError
    csrf = re.search(
        r"form_token:\s*'([^']+)'",
        tree.css_first('script:lexbor-contains("form_token")').text(),
    ).group(1)
    resp = await client.post(
            ajaxUrl,
            data={
                "action": "view_post",
                "post_id": Id,
                "mode": "text",
                "form_token": csrf,
            },
        )
    postbody = resp.json().get("post_text")
    return postbody, Id


async def getTopic(pageId: int, client: httpx.AsyncClient) -> Topic:
        response = await client.get(f"{threadUrl}?t={pageId}")
        if response.status_code != 200:
            raise NetworkError("Unable to fetch topic")
        tree = LexborHTMLParser(response.text)
        try:
            postBody, Id = await getPostBody(client, tree)
        except NotExistsError:
            raise NotExistsError("Topic not found")
        return Topic(
            title=tree.css_first("#topic-title").text(), 
            body=postBody, 
            id=Id
        )

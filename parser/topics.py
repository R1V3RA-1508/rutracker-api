from bs4 import BeautifulSoup
import httpx
import re
from models import Topic
from models.errors import NotExistsError, NetworkError
from parser import threadUrl, ajaxUrl


def get_bb_session():
    pass


async def getPostBody(client: httpx.AsyncClient, soup: BeautifulSoup):
    try:
        Id = soup.select('tbody[id^="post_"]')[0].get("id").split("_")[1]
    except IndexError:
        raise NotExistsError
    csrf = re.search(
        r"form_token:\s*'([^']+)'",
        soup.select_one('script:-soup-contains("form_token")').text,
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
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            postBody, Id = await getPostBody(client, soup)
        except NotExistsError:
            raise NotExistsError("Topic not found")
        return Topic(
            title=soup.select_one("#topic-title").text, 
            body=postBody, 
            id=Id
        )

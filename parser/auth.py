from selectolax.lexbor import LexborHTMLParser
import httpx
from parser import loginUrl
from models import LoginQuery
from models.errors import NetworkError, NeedCaptcha


async def getSession(client: httpx.AsyncClient, query: LoginQuery):
    if not query.capField:
      data = f"login_username={query.username}&login_password={query.password}&login=%C2%F5%EE%E4"
    else:
      data=f"login_username={query.username}&login_password={query.password}&login=%C2%F5%EE%E4&cap_sid={query.capSid}&{query.capField}={query.capValue}&redirect={query.redirect}"
    response = await client.post(loginUrl, data=data)
    if response.status_code != 200:
        raise NetworkError
    if response.text.find("Похоже, вас пытаются обмануть"):
        tree = LexborHTMLParser(response.text)
        try:
            captchaImage = tree.css_first('img[src*="/captcha/"]').attrs.get("src")
        except AttributeError:
            raise NetworkError
        capSid = tree.css_first('input[name="cap_sid"]').attrs.get("value")
        capField = tree.css_first('input[name^="cap_code_"]').attrs.get("name")
        redirect = (
            tree.css_first('input[name="redirect"]').attrs.get("value")
        )
        raise NeedCaptcha(
            imageUrl=captchaImage, capSid=capSid, capField=capField, redirect=redirect
        )
    return response.headers.get("set-cookie").split(";")[0].split("=")[1]
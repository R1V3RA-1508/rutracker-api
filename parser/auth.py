from selectolax.lexbor import LexborHTMLParser
import httpx
from parser import loginUrl
from models import LoginQuery, Session
from models.errors import NetworkError, NeedCaptcha, InvalidPassError


async def getSession(client: httpx.AsyncClient, query: LoginQuery):
    if not query.capField:
        data = f"login_username={query.username}&login_password={query.password}&login=%C2%F5%EE%E4"
    else:
        data = f"login_username={query.username}&login_password={query.password}&login=%C2%F5%EE%E4&cap_sid={query.capSid}&{query.capField}={query.capValue}&redirect={query.redirect}"
    response = await client.post(loginUrl, data=data)
    if response.status_code != 200 and response.status_code != 302:
        raise NetworkError
    elif response.status_code == 302:
        pass
    tree = LexborHTMLParser(response.text)
    nadpis = tree.css_first(".warnColor1")
    if (
        nadpis
        and nadpis.text()
        == "Вы ввели неверное/неактивное имя пользователя или неверный пароль"
    ):
        raise InvalidPassError("Wrong pass or login")
    elif (
        nadpis
        and nadpis.text()
        == "Введите код подтверждения (символы, изображенные на картинке)"
    ):
        try:
            captchaImage = tree.css_first('img[src*="/captcha/"]').attrs.get("src")
        except AttributeError:
            """Иногда бывает такой баг, что он считает подозрительным, но не дает капчу. Здесь это обрабатывается через костыль NetworkError"""
            raise NetworkError
        capSid = tree.css_first('input[name="cap_sid"]').attrs.get("value")
        capField = tree.css_first('input[name^="cap_code_"]').attrs.get("name")
        redirect = tree.css_first('input[name="redirect"]').attrs.get("value")
        raise NeedCaptcha(
            imageUrl=captchaImage, capSid=capSid, capField=capField, redirect=redirect
        )
    return Session(bb_session=response.headers["set-cookie"].split(";")[0].split("=")[1])

import logging
import secrets

from typing import Any, List

import tornado.web

from espyta import configuration

log = logging.getLogger(__name__)


def make_application() -> tornado.web.Application:
    app = tornado.web.Application(
        pages,
        template_path=path.template,
        default_handler_class=handler.website.Base,
        xsrf_cookies=True,
        cookie_secret=secrets.token_hex(),
        static_path=path.static,
    )

    app.configuration = configuration  # type: ignore

    return app

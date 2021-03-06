# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import mandrill
from django.conf import settings
from background_task import background

if settings.TESTING:
    client = None
else:
    client = mandrill.Mandrill(settings.MANDRILL_KEY)
    fake_client = mandrill.Mandrill(settings.MANDRILL_TEST_KEY)


# @params users: a list of User {email, first_name, last_name}
@background()
def send_mail(template_name, content, users, fake=False):
    if not client:
        return

    to = [
        {
            "email": user["email"],
            "name": f"{user['first_name']} {user['last_name']}"
            if user.get("first_name")
            else None,
            "type": "to",
        }
        for user in users
    ]

    content["bimdata_url"] = settings.APP_URL

    formatted_content = [{"name": key, "content": value} for key, value in content.items()]

    message = {"auto_text": True, "to": to, "global_merge_vars": formatted_content}

    print(
        f'sending mail with template "{template_name}" to {[user["email"] for user in users]}'
    )

    if fake:
        fake_client.messages.send_template(
            template_name=template_name,
            template_content=[],
            message=message,
            asynchronous=False,
        )
    else:
        client.messages.send_template(
            template_name=template_name,
            template_content=[],
            message=message,
            asynchronous=False,
        )

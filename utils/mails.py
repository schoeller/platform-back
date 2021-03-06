# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.conf import settings
from externals import mandrill


def send_onboarding(user):
    return
    content = {"bimdata_url": settings.APP_URL}
    mandrill.send_mail("emailing-onboarding", content, [user.to_json()])


def send_invitation_accepted(payload):
    if payload.get("project"):
        mail_content = {
            "user_name": f"{payload['user']['firstname']} {payload['user']['lastname']}",
            "project_name": payload["project"]["name"],
            "cloud_name": payload["cloud"]["name"],
            "project_url": f"{settings.APP_URL}/project/{payload['project']['id']}",
        }
        mandrill.send_mail(
            "invitation-du-user-ok", mail_content, [{"email": payload["invitor_email"]}]
        )
    else:
        invitor_content = {
            "user_name": f"{payload['user']['firstname']} {payload['user']['lastname']}",
            "cloud_name": payload["cloud"]["name"],
            "cloud_url": settings.APP_URL,
        }
        mandrill.send_mail(
            "invitation-du-user-ok-cloud",
            invitor_content,
            [{"email": payload["invitor"]["email"]}],
        )


def send_ifc_ok(payload):
    content = {
        "ifc_name": payload.get("name"),
        "viewer_url": f"{settings.APP_URL}/cloud/{payload['cloud_id']}/project/{payload['project_id']}/ifc/{payload['id']}/viewer",
    }
    mandrill.send_mail(
        "votre-ifc-t-converti", content, [{"email": payload["creator"]["email"]}]
    )


def send_ifc_ko(payload):
    content = {
        "ifc_name": payload.get("name"),
        "project_url": f"{settings.APP_URL}/project/{payload['project_id']}",
    }
    mandrill.send_mail(
        "erreur-la-conversion-de-votre-ifc", content, [{"email": payload["creator"]["email"]}]
    )

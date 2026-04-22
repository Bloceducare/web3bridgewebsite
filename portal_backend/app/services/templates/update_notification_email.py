UPDATE_NOTIFICATION_EMAIL_SUBJECT = "New Web3Bridge Portal Notification"

UPDATE_NOTIFICATION_EMAIL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Notification</title>
</head>
<body style="font-family: Arial, sans-serif; color: #1f2937;">
    <p>Hello,</p>
    <p>You have a new notification from the Web3Bridge student portal.</p>
    <h2 style="margin-bottom: 8px;">{title}</h2>
    <p style="white-space: pre-line;">{body}</p>
</body>
</html>
"""


def render_update_notification_email(*, title: str, body: str) -> tuple[str, str]:
    html_body = UPDATE_NOTIFICATION_EMAIL_HTML.format(title=title, body=body)
    return UPDATE_NOTIFICATION_EMAIL_SUBJECT, html_body

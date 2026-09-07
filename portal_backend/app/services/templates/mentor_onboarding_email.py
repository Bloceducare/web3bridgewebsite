MENTOR_ONBOARDING_EMAIL_SUBJECT = "Welcome to the Web3Bridge Mentor Portal — Set Up Your Account"

MENTOR_ONBOARDING_EMAIL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web3Bridge Mentor Portal — Account Setup</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #007bff;
        }}
        p {{
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        .btn {{
            display: inline-block;
            padding: 16px 36px;
            background-color: #0056d6;
            color: #ffffff !important;
            text-decoration: none !important;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin: 16px 0;
            border: 1px solid #004bb5;
        }}
        .note {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, {name}!</h1>
        <p>Congratulations on your registration as a Mentor with Web3Bridge!</p>
        <p>Your <strong>Mentor Portal</strong> account has been created for the <strong>{programme}</strong> programme on the <strong>{track}</strong> track. The portal is your
           personal hub for managing your classes, generating attendance codes, authoring assessments, and tracking updates.</p>
        <p>To get started, click the button below to set up your password and activate
           your account:</p>
        <p style="text-align: center; margin: 28px 0;">
            <a
                class="btn"
                href="{activation_url}"
                style="display: inline-block; padding: 16px 36px; background-color: #0056d6; color: #ffffff !important; text-decoration: none !important; border-radius: 8px; font-size: 16px; font-weight: 600; font-family: Arial, Helvetica, sans-serif; letter-spacing: 0.02em; border: 1px solid #004bb5;"
            >Activate My Mentor Portal Account</a>
        </p>
        <p class="note">
            If the button above doesn't work, copy and paste this link into your browser:<br>
            <a href="{activation_url}">{activation_url}</a>
        </p>
        <p class="note">
            This link expires in 7 days. If it expires, contact support for a new one.
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p>With Love,</p>
        <p>The Web3Bridge Team</p>
    </div>
</body>
</html>
"""


def render_mentor_onboarding_email(
    *,
    name: str,
    activation_url: str,
    programme: str,
    track: str,
) -> tuple[str, str]:
    """Return (subject, html_body) for the mentor portal onboarding email."""
    html_body = MENTOR_ONBOARDING_EMAIL_HTML.format(
        name=name,
        activation_url=activation_url,
        programme=programme,
        track=track,
    )
    return MENTOR_ONBOARDING_EMAIL_SUBJECT, html_body

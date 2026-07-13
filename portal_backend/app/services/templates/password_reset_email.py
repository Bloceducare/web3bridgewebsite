PASSWORD_RESET_EMAIL_SUBJECT = "Web3Bridge Student Portal — Reset Your Password"

PASSWORD_RESET_EMAIL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
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
        <h1>Reset Your Password</h1>
        <p>Hi {name},</p>
        <p>We received a request to reset the password for your Web3Bridge Student Portal
           account. Click the button below to choose a new password:</p>
        <p style="text-align: center; margin: 28px 0;">
            <a
                class="btn"
                href="{reset_url}"
                style="display: inline-block; padding: 16px 36px; background-color: #0056d6; color: #ffffff !important; text-decoration: none !important; border-radius: 8px; font-size: 16px; font-weight: 600; font-family: Arial, Helvetica, sans-serif; letter-spacing: 0.02em; border: 1px solid #004bb5;"
            >Reset Password</a>
        </p>
        <p class="note">
            If the button above doesn't work, copy and paste this link into your browser:<br>
            <a href="{reset_url}">{reset_url}</a>
        </p>
        <p class="note">
            This link expires in {expire_hours} hour(s). If you did not request a password
            reset, you can safely ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p>With Love,</p>
        <p>The Web3Bridge Team</p>
    </div>
</body>
</html>
"""


def render_password_reset_email(
    *,
    name: str,
    reset_url: str,
    expire_hours: int,
) -> tuple[str, str]:
    """Return (subject, html_body) for the password reset email."""
    html_body = PASSWORD_RESET_EMAIL_HTML.format(
        name=name,
        reset_url=reset_url,
        expire_hours=expire_hours,
    )
    return PASSWORD_RESET_EMAIL_SUBJECT, html_body

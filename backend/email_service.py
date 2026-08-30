import os
from dotenv import load_dotenv
import resend

# --------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------------

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

# --------------------------------------------------------
# SEND VERIFICATION EMAIL
# --------------------------------------------------------

def send_test_email(to_email: str, otp: str):

    try:

        response = resend.Emails.send(
            {
                "from": "NeuroCalc <onboarding@resend.dev>",

                "to": [to_email],

                "subject": "Verify your NeuroCalc Account",

                "html": f"""
                <div style="font-family:Arial,sans-serif;padding:30px">

                    <h2>Welcome to NeuroCalc 🚀</h2>

                    <p>
                        Thank you for creating your account.
                    </p>

                    <p>
                        Your verification code is:
                    </p>

                    <h1 style="
                        color:#2563eb;
                        font-size:48px;
                        letter-spacing:8px;
                    ">
                        {otp}
                    </h1>

                    <p>
                        This OTP is valid for
                        <strong>10 minutes</strong>.
                    </p>

                    <hr>

                    <p style="color:gray;font-size:14px">
                        If you didn't create this account,
                        you can safely ignore this email.
                    </p>

                </div>
                """,
            }
        )

       
        print("EMAIL SENT SUCCESSFULLY")
        print(response)
        

        return response

    except Exception as e:

        
        print("EMAIL ERROR")
        print(type(e).__name__)
        print(e)
        
        raise
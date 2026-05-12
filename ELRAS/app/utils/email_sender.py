class EmailSender:

    @staticmethod
    def send_email(to_email, subject, message):
        """
        Dummy email sender (for demo)
        Replace with real SMTP if needed
        """
        print("------ EMAIL SENT ------")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("------------------------")

        return True
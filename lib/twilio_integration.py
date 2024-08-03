from twilio.rest import Client

def send_whatsapp_message(to, body):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to=to
    )
    return message.sid

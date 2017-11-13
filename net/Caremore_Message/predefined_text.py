TEXT = {
    "successfully-login": {"status": "success", "description": "Login successfully"},
    "bye-bye": {"status": "success", "description": "Bye-bye"},
    "incorrect-device": {"status": "failed", "description": "Incorrect device"},
    "no-device-name": {"status": "failed", "description": "No device name"},

    "duplicated_message": {"status": "failed", "description": "Duplicated message %s"},
    "internal_error": {"status": "failed", "description": "Server internal error"},
    "message_sent": {"status": "success", "description": "Message %s sent"},
}
DEVICE = ["Android","Watch"]



def text(message_id, *kwargs):
    to_return = TEXT[message_id].copy()
    to_return["description"] = to_return["description"] % kwargs
    return to_return

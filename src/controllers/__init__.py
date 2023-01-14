# import ordering matters!

# first handler - photos (most commonly)
from src.controllers.photo_controllers.photo_download_controller import send_photo_to_user

# next in descending order of importance (in my opinion)
from src.controllers.term_controller import choose_term, set_term_from_button
from src.controllers.subject_controller import choose_subject, set_subject_from_button
from src.controllers.tickets_list_controller import get_tickets_list

from src.controllers.photo_controllers.uploader.cancel_controller import cancel
from src.controllers.photo_controllers.uploader.photo_bad_controller import photo_bad
from src.controllers.photo_controllers.uploader.photo_ok_controller import photo_ok
from src.controllers.photo_controllers.uploader.photo_uploader_controller import ask_secret_key, \
    check_key, ticket_number, upload_photo, finish, rate_waiting

from src.controllers.greeting_controller import greeting_message

from src.controllers.any_text_controller import any_text_handler  # most not commonly

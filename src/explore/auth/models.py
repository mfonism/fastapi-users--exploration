from .email_changes import models as email_change_models
from .users import manager as user_manager
from .users import models as user_models

User = user_models.User
UserManager = user_manager.UserManager
UserEmailChange = email_change_models.UserEmailChange

get_user_db = user_manager.get_user_db
get_user_manager = user_manager.get_user_manager
generate_email_change_token = email_change_models.generate_email_change_token
hash_email_change_token = email_change_models.hash_email_change_token

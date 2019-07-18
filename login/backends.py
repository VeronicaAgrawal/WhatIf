from login.models import Users
import logging


class MyAuthBackend(object):
    def authenticate(self, request, email, password):
        try:
            user = Users.objects.get(EmailId=email)
            if user.check_pwd(user,password):
                return user
            else:
                return None
        except Users.DoesNotExist:
            logging.getLogger("error_logger").error("user with login details does not exists " )
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = Users.objects.get(sys_id=user_id)
            if user.is_active:
                return user
            return None
        except Users.DoesNotExist:
            logging.getLogger("error_logger").error("user not found")
            return None
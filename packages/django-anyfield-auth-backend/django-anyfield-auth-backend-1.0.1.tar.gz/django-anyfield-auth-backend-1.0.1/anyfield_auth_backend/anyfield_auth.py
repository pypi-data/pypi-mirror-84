import logging

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

import anyfield_auth_backend

logger = logging.getLogger("mail.auth.backend")


class AnyfieldAuthBackend(ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, request, username, password):
        """ Authenticate a user based on email address as the user name. """
        for fld in anyfield_auth_backend.AUTH_ANYFIELDS:
            try:
                pars = {fld: username}
                users = User.objects.filter(**pars)
                if len(users) > 1 and anyfield_auth_backend.AUTH_ANYFIELDS_ONLY_UNIQUE_USERS:
                    logger.debug("The filter '%s' match more than one user. "
                                 "Ignoring these (check AUTH_ANYFIELDS_ONLY_UNIQUE_USERS)." % pars)
                    continue

                if len(users) == 0:
                    logger.debug("No user found with filter '%s'." % pars)

                for usr in users:
                    if usr.check_password(password):
                        return usr
                    else:
                        logger.debug("Wrong password for userid: %s." % usr.id)

            except User.DoesNotExist:
                return None
            except FieldError as ex:
                logger.error("The field '%s' is not in user table available. "
                             "Please check the AUTH_ANYFIELDS config in settings")
                raise

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

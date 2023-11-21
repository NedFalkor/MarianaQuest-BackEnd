from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CharacterTypeValidator:
    def validate(self, password, user=None):
        types = 0
        if any(char.isdigit() for char in password):
            types += 1
        if any(char.isalpha() and char.islower() for char in password):
            types += 1
        if any(char.isalpha() and char.isupper() for char in password):
            types += 1
        if any(char in "!@#$%^&*()_-+=<>?/,.:;{}[]|\"'~" for char in password):
            types += 1

        if types < 4:
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère de chaque type : majuscules, minuscules, "
                  "chiffres et caractères spéciaux."),
                code='password_no_variation',
            )

    @staticmethod
    def get_help_text():
        return _(
            "Your password must contain at least one digit, one lowercase letter, "
            "one uppercase letter, and one special character."
        )

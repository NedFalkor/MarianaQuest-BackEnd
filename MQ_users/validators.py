from django.core.exceptions import ValidationError


def validate_character_types(value):
    types = 0
    if any(char.isdigit() for char in value):
        types += 1
    if any(char.isalpha() and char.islower() for char in value):
        types += 1
    if any(char.isalpha() and char.isupper() for char in value):
        types += 1
    if any(char in "!@#$%^&*()_-+=<>?/,.:;{}[]|\"'~" for char in value):
        types += 1

    if types < 4:
        raise ValidationError(
            ("Le mot de passe doit contenir au moins un caractère de chaque type : majuscules, minuscules, "
             "chiffres et caractères spéciaux."),
            code='password_no_variation',
        )

# Si vous avez besoin d'un validateur d'anonymat, vous pouvez l'ajouter ici.

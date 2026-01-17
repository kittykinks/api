import nanoid

from tortoise import fields


def IDField():
    return fields.CharField(
        max_length=21,
        default=nanoid.generate,
        primary_key=True,
    )

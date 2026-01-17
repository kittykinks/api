from tortoise import fields
from tortoise.models import Model

from kittyk.db.fields import IDField


class Kink(Model):
    id = IDField()

    name = fields.CharField(max_length=64)
    description = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

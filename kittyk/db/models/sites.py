from enum import Enum

from tortoise import fields
from tortoise.models import Model

from kittyk.db.fields import IDField


class Site(Model):
    id = IDField()

    user = fields.OneToOneField("models.User", related_name="site")
    user_id: str

    slug = fields.CharField(max_length=32, unique=True)

    name = fields.CharField(max_length=64)
    bio = fields.CharField(max_length=128, null=True)

    kink_ratings: fields.ReverseRelation["KinkRating"]
    links: fields.ReverseRelation["Link"]

    avatar_url = fields.CharField(max_length=256, null=True)
    banner_url = fields.CharField(max_length=256, null=True)


class KinkRating(Model):
    id = IDField()

    user = fields.ForeignKeyField("models.User", related_name="kink_ratings")
    user_id: str
    kink = fields.ForeignKeyField("models.Kink", related_name="kink_ratings")
    kink_id: str
    site = fields.ForeignKeyField("models.Site", related_name="kink_ratings")
    site_id: str

    rating = fields.IntField()  # 0-10 scale, rating / 2 = stars
    comment = fields.CharField(max_length=32, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class LinkSource(str, Enum):
    DISCORD = "discord"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    WATTPAD = "wattpad"
    SESSION = "session"
    REDDIT = "reddit"
    TELEGRAM = "telegram"
    TUMBLR = "tumblr"
    BLUESKY = "bluesky"
    MASTODON = "mastodon"
    SIGNAL = "signal"
    MATRIX = "matrix"
    OTHER = "other"


class Link(Model):
    id = IDField()

    site = fields.ForeignKeyField("models.Site", related_name="links")
    site_id: str
    user = fields.ForeignKeyField("models.User", related_name="links")
    user_id: str

    source = fields.CharEnumField(LinkSource)
    pointer = fields.CharField(max_length=128)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

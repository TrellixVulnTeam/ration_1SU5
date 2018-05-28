from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


def get_user_tag_list(self):
    user_tag_list = User_Tag.objects.filter(user=self).order_by('-item_count')
    return user_tag_list


def get_tag_list(self):
    rating_list = User_Item.objects.filter(user=self)
    tag_list = []

    for rating in rating_list:
        for tag in rating.item.tags.all():
            if not tag in tag_list:
                tag_list.append(tag)

    return tag_list


def get_ratings_by_tag(self, tag):
    rating_query_set = User_Item.objects.filter(user=self)
    ratings = []

    for rating in rating_query_set:
        if rating.has_tag(tag):
            ratings.append(rating)
    return ratings


User.add_to_class("get_user_tag_list", get_user_tag_list)
User.add_to_class("get_tag_list", get_tag_list)
User.add_to_class("get_ratings_by_tag", get_ratings_by_tag)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
        primary_key=True
    )
    fullname = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile_pics', blank=True, default="profile_pics/default.png")
    bio = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    website = models.TextField(null=True, blank=True)


class Tag(models.Model):
    name = models.TextField()
    is_official = models.BooleanField()

class User_Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    item_count = models.IntegerField()
    is_private = models.NullBooleanField()

    def get_update_list(self):
        user_update_list = Update.objects.filter(user=self.user)
        update_list = []

        for update in user_update_list:
            try:
                item = update.interaction.item
                for tag in item.tags.all():
                    if tag == self.tag:
                        update_list.append(update)
            except:
                pass

        update_list.sort(key=lambda x: x.timestamp, reverse=True)

        return update_list


class Favorite_User_Tag(models.Model):
    user = models.ForeignKey(User, related_name='favorite_user_tags', on_delete=models.CASCADE)
    user_tag = models.ForeignKey(User_Tag, on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='items')

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='item_icons', blank=True, default="item_icons/default.png")

    avg_rating = models.FloatField(null=True)
    avg_interest = models.FloatField(null=True)

    def calc_average(self):
        self.avg_rating = self.user_items.all().aggregate(Avg('rating')).get('rating__avg')
        self.avg_interest = self.user_items.all().aggregate(Avg('interest')).get('interest__avg')
        self.save()


class User_Item(models.Model):
    user = models.ForeignKey(User, related_name='user_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='user_items', on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    interest = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True, blank=True)

    def has_tag(self, tag):
        for x in self.item.tags.all():
            if tag == x:
                return True
        return False





class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    user_tag = models.ForeignKey(User_Tag, on_delete=models.CASCADE)


class Update(models.Model):
    user = models.ForeignKey(User, related_name='updates', on_delete=models.CASCADE)
    interaction = models.ForeignKey(User_Item, related_name='updates', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    is_visible = models.BooleanField()

from django.contrib.auth import login as auth_login, authenticate
from django.db.models import Q
from django.shortcuts import redirect

from core.forms import SignUpForm, ItemForm, UserItemForm
from core.models import User_Item, User_Item_Log, Item, Tag, Taglist, Log, Update


def create_and_authenticate_user(request):
    form = SignUpForm(request.POST)
    form.save()

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')

    user = authenticate(username=username, password=password)
    auth_login(request, user)

    return


def get_logs_by_user(user):
    user_item_list = User_Item.objects.filter(user=user)

    logs = []
    for user_item in user_item_list:
        for log in user_item.logs.all():
            logs.append(log)
        logs.sort(key=lambda x: x.timestamp, reverse=True)

    return logs


def get_tag(name):
    if Tag.objects.filter(name=name).count() > 0:
        tag = Tag.objects.filter(name=name).first()
        return tag
    else:
        tag = Tag.objects.create(name=name)
        return tag


def generate_taglist_logs(user, item, tag_name):
    if Taglist.objects.filter(user=user).count() > 0:
        user_taglists = Taglist.objects.filter(user=user)
        for user_taglist in user_taglists:
            for tag in user_taglist.tags.all():
                if tag.name == tag_name:
                    message = "@" + user.username + "  -> item: " + item.name
                    Log.objects.create(taglist=user_taglist, message=message)
                    break



def update_user_item(user, item, form):
    if User_Item.objects.filter(user=user, item=item).count() > 0:
        user_item = User_Item.objects.filter(user=user, item=item).first()
        user_item.rating = form.cleaned_data['rating']
        user_item.interest = form.cleaned_data['interest']
    else:
        user_item = form.save(commit=False)
        user_item.user = user
        user_item.item = item

    user_item.save()
    item.calc_average()

    message = "Updated an item's ratings: " + item.name + " ( Score: "+ str(user_item.rating) +\
              " | Interest: " + str(user_item.interest) + " )"
    Update.objects.create(user=user, message=message, interaction=user_item)

    user_taglists = user.taglists.all()
    for user_taglist in user_taglists:
        for tag in user_taglist.tags.all():
            if tag in user_item.item.tags.all():
                message = "@" + user.username + "  -> item: " + item.name + \
                          " (rating: " + str(user_item.rating) + \
                          " | interest: " + str(user_item.interest) + ")"
                Log.objects.create(taglist=user_taglist, message=message)
                break

    return redirect('item', item.id)


def get_log_message(user_item):
    rating_log = ""
    if not user_item.rating == None:
        rating_log = "Rating: " + str(int(user_item.rating)) + ""

    interest_log = ""
    if not user_item.interest == None:
        interest_log = " || Interest: " + str(int(user_item.interest))

    message = user_item.user.username + " updated '" + user_item.item.name + "' (" + rating_log + interest_log + ")"

    return message


def get_latest_items(n):
    item_list = Item.objects.all().order_by('-created_at')[:n]
    return item_list


class Comparison:
    def __init__(self, user_item, your_user, their_user):
        self.item = user_item.item
        if User_Item.objects.filter(user=your_user, item=user_item.item).count() > 0:
            self.your_rating = User_Item.objects.filter(user=your_user, item=user_item.item).first().rating
            self.your_interest = User_Item.objects.filter(user=your_user, item=user_item.item).first().interest
        else:
            self.your_rating = None
            self.your_interest = None
        if User_Item.objects.filter(user=their_user, item=user_item.item).count() > 0:
            self.their_rating = User_Item.objects.filter(user=their_user, item=user_item.item).first().rating
            self.their_interest = User_Item.objects.filter(user=their_user, item=user_item.item).first().interest
        else:
            self.their_rating = None
            self.their_interest = None

    def equals(self, other):
        if self.item == other.item:
            if self.your_rating == other.your_rating:
                if self.your_interest == other.your_interest:
                    if self.their_rating == other.their_rating:
                        if self.their_interest == other.their_interest:
                            return 1
        return 0


def get_comparison_list(your_user, their_user):
    comparison_list = []

    user_item_list = User_Item.objects.filter(Q(user=your_user) | Q(user=their_user))

    for user_item in user_item_list:
        comparison = Comparison(user_item, your_user, their_user)
        comparison_exists = False

        for other in comparison_list:

            if comparison.equals(other):
                comparison_exists = True

        if not comparison_exists:
            comparison_list.append(comparison)

    return comparison_list

def get_updates_by_taglist(taglist):
    user = taglist.user
    tags = taglist.tags.all()
    user_updates = Update.objects.filter(user=user)

    updates = []

    for update in user_updates:
        for tag in tags:
            try:
                if tag in update.interaction.item.tags.all():
                    updates.append(update)
            except:
                pass

    updates.sort(key=lambda x: x.timestamp, reverse=True)

    return updates

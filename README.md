# ***CHAT SYSTEM***

*This will covers the features:* 

- Django Channels
- Websockets
- Redis
- Display number of connected users in the chat room
- Send / receive messages in real time
- Pagination of messages, display the last 10 messages, show more messages on scroll with progress indicator
- Asynchronous load profile images of the users in the chat room
- Markdown support for messages, code snippets

...

# ***DATABASE MODELS FOR PUBLIC CHAT ROOM***

*Designing the database models*

1. `PublicChatRoom`, DB model for the chat itself. It will contain user count and title.
2. `PublicRoomChatMessage` model for public chat messages (separate with foreign key to the chat model)
*So that we have `PublicChatMessages` model with a foreign key to the `Chat` or `Room` model*  
*The `PublicChatMessages` model will also have the message content, the user who sent the message, and the timestamp, etc.*  


1. Creating new directory for the project and install Django with pipenv

```bash
mkdir django_channels
cd django_channels
```

2. Install Django with pipenv

```bash
pipenv install django
```

3. Activate the virtual environment

**NOTE:** *In VSCode use the command `Ctrl + Shift + P` and type `Python: Select Interpreter` to select the virtual environment with the path returned by the previous command `pipenv install django` and restart the VSCode*  

*This will activate the virtual environment automatically in the VSCode terminal*  

Otherwise activate the virtual environment manually with the command:  

```bash
pipenv shell
```

4. Create a new Django project in the current directory

```bash
django-admin startproject _main .
```

5. Create a new Django app

```bash
python manage.py startapp _public_chat
```

6. Add the app to the `INSTALLED_APPS` in the `settings.py` file

```python
INSTALLED_APPS = [
	...
	'_public_chat',
]
```

7. Create the database models in the `_public_chat/models.py` file

```python
from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):

	title = models.CharField(max_length=100, unique=True, blank=False) # sets title parameters
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text='users in this chat room.') # sets users parameters

	def __str__(self):
		return self.title
	
	def connect_user(self, user):
		# returns True if user is added
		is_user_added = False
		if not user in self.users.all():
			self.users.add(user)
			is_user_added = True
		elif user in self.users.all():
			is_user_added = True
		return is_user_added

	def disconnect_user(self, user):
		# returns True if user is removed
		is_user_removed = False
		if user in self.users.all():
			self.users.remove(user)
			is_user_removed = True
		return is_user_removed

	@property
	def group_name(self):
		# Returns the Channels Group name that sockets should subscribe to to get sent messages
		return "PublicChatRoom-%s" % self.id


class PublicRoomChatMessageManager(models.Manager):
	def by_room(self, room):
		# qs = PublicChatRoomMessage.objects.filter(room=room).order_by('-timestamp')
		qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
		return qs


class PublicRoomChatMessage(models.Model):
	# Chat message created by a user inside a PublicChatRoom (foreign key)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # sets user parameters (if user is deleted, all messages are deleted)
	room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE) # sets room parameters (if room is deleted, all messages are deleted)
	timestamp = models.DateTimeField(auto_now_add=True) # sets timestamp parameters
	content = models.TextField(unique=False, blank=False) # sets content parameters

	object = PublicRoomChatMessageManager()

	def __str__(self):
		return self.content

```

8. Create the database tables

```bash
python manage.py makemigrations
python manage.py migrate
```

9. Register the models in the Django admin

*In the `_public_chat/admin.py` file*:  

```python
from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from _public_chat.models import PublicChatRoom, PublicRoomChatMessage


class PublicChatRoomAdmin(admin.ModelAdmin):
	list_display = ['id', 'title']
	search_fields = ['id', 'title']
	readonly_fields = ['id']

	class Meta:
		model = PublicChatRoom


admin.site.register(PublicChatRoom, PublicChatRoomAdmin)


# Resource: http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class PublicRoomChatMessageAdmin(admin.ModelAdmin):
	list_filter = ['room', 'user', 'timestamp']
	list_display = ['room', 'user', 'content', 'timestamp']
	search_fields = ['room__title', 'user__username', 'content']
	readonly_fields = ['id', 'user', 'room', 'timestamp']

	show_full_result_count = False
	paginator = CachingPaginator

	class Meta:
		model = PublicRoomChatMessage


admin.site.register(PublicRoomChatMessage, PublicRoomChatMessageAdmin)
```

10. Create a superuser

```bash
python manage.py createsuperuser
```

11. Run the Django development server

```bash
python manage.py runserver
```

12. Open the Django admin in the browser and login with the superuser credentials

*At this point the database models are created and can be managed in the Django admin. The database tables are empty and can be populated with data once frontend views are created*    


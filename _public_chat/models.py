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


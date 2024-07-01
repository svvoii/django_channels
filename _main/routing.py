from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path


application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(

			# URLRouter([...]) # This is the routing configuration for the chat app
		)
	),
})

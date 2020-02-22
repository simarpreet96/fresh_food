from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModekBackend

class EmailAuthBackend(object):

	def authenticate(self, username=None, password=None):
		try:
			user=User.objects.get(email=username)
			if user.check_password(password):
				return user
			except User.DoesNotExist:
				return None

	def get_user(self, user_is):
		try:
			return User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return None


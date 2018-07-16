
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app.models import UserModel


class UserMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # request_path = ['/axf/login/', '/axf/home/', '/axf/regist/',
        #                 '/axf/market/', '/axf/cart/', '/axf/mine/']
        # if request.path in request_path:
        #     return
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            pass
        users = UserModel.objects.filter(ticket=ticket)
        if not users:
            pass
        else:
            request.user = users[0]



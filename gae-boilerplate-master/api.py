# from models import OrderStore, Order, OrderList, Item, ItemList, ItemStore
# from google.appengine.ext import ndb

# import endpoints
# from protorpc import messages
# from protorpc import message_types
# from protorpc import remote



# package = 'easy'

# WEB_CLIENT_ID = 'replace this with your web client application ID'
# ANDROID_CLIENT_ID = 'replace this with your Android client ID'
# IOS_CLIENT_ID = 'replace this with your iOS client ID'
# ANDROID_AUDIENCE = WEB_CLIENT_ID


# @endpoints.api(name='laundry', version='v1',
#                allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
#                                    IOS_CLIENT_ID,
#                                    endpoints.API_EXPLORER_CLIENT_ID],
#                audiences=[ANDROID_AUDIENCE],
#                scopes=[endpoints.EMAIL_SCOPE])
# class LaundryApi(remote.Service):
#     """Laundry API v1."""

import Cookie
import logging
import endpoints
import os
from google.appengine.ext import ndb
from protorpc import remote
from protorpc import message_types
from protorpc import messages
import time
from webapp2_extras.sessions import SessionDict
from bp_includes.models import User
from webapp2_extras import sessions, securecookie, auth
from bp_content.themes.default.handlers.models import OrderStore, Order, OrderList, Item, ItemList, ItemStore


package = 'easy'

TOKEN_CONFIG = {
    'token_max_age': 86400 * 7 * 3,
    'token_new_age': 86400,
    'token_cache_age': 3600,
}

SESSION_ATTRIBUTES = ['user_id', 'remember',
                      'token', 'token_ts', 'cache_ts']

SESSION_SECRET_KEY = '9C3155EFEEB9D9A66A22EDC16AEDA'

class TestMessage(messages.Message):
    username = messages.StringField(2)


@endpoints.api(name='laundry_api', version='v1',
               description='Laundry API')
class LaundryApi(remote.Service):
    user = None
    token = None

    @classmethod
    def get_user_from_cookie(cls):
        serializer = securecookie.SecureCookieSerializer(SESSION_SECRET_KEY)
        cookie_string = os.environ.get('HTTP_COOKIE')
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        session = cookie['session'].value
        session_name = cookie['session_name'].value
        session_name_data = serializer.deserialize('session_name', session_name)
        session_dict = SessionDict(cls, data=session_name_data, new=False)

        if session_dict:
            session_final = dict(zip(SESSION_ATTRIBUTES, session_dict.get('_user')))
            _user, _token = cls.validate_token(session_final.get('user_id'), session_final.get('token'),
                                               token_ts=session_final.get('token_ts'))
            cls.user = _user
            cls.token = _token

    @classmethod
    def user_to_dict(cls, user):
        """Returns a dictionary based on a user object.

        Extra attributes to be retrieved must be set in this module's
        configuration.

        :param user:
            User object: an instance the custom user model.
        :returns:
            A dictionary with user data.
        """
        if not user:
            return None

        user_dict = dict((a, getattr(user, a)) for a in [])
        user_dict['user_id'] = user.get_id()
        return user_dict

    @classmethod
    def get_user_by_auth_token(cls, user_id, token):
        """Returns a user dict based on user_id and auth token.

        :param user_id:
            User id.
        :param token:
            Authentication token.
        :returns:
            A tuple ``(user_dict, token_timestamp)``. Both values can be None.
            The token timestamp will be None if the user is invalid or it
            is valid but the token requires renewal.
        """
        user, ts = User.get_by_auth_token(user_id, token)
        return cls.user_to_dict(user), ts

    @classmethod
    def validate_token(cls, user_id, token, token_ts=None):
        """Validates a token.

        Tokens are random strings used to authenticate temporarily. They are
        used to validate sessions or service requests.

        :param user_id:
            User id.
        :param token:
            Token to be checked.
        :param token_ts:
            Optional token timestamp used to pre-validate the token age.
        :returns:
            A tuple ``(user_dict, token)``.
        """
        now = int(time.time())
        delete = token_ts and ((now - token_ts) > TOKEN_CONFIG['token_max_age'])
        create = False

        if not delete:
            # Try to fetch the user.
            user, ts = cls.get_user_by_auth_token(user_id, token)
            if user:
                # Now validate the real timestamp.
                delete = (now - ts) > TOKEN_CONFIG['token_max_age']
                create = (now - ts) > TOKEN_CONFIG['token_new_age']

        if delete or create or not user:
            if delete or create:
                # Delete token from db.
                User.delete_auth_token(user_id, token)

                if delete:
                    user = None

            token = None

        return user, token

    @endpoints.method(message_types.VoidMessage, OrderList,
                      path='orders', http_method='GET',
                      name='laundry.getAllOrders')
    def order_list(self, request):

            # if orderstorelist:
        self.get_user_from_cookie()

        if not self.user:
            raise endpoints.UnauthorizedException('Invalid token.')

        userkey_id = self.user['user_id']
        user_key = ndb.Key('User', userkey_id)
        current_user = user_key.get()
        print current_user.username

        q = [o.to_message(idx+1) for idx, o in enumerate(OrderStore.query(OrderStore.user.username == current_user.username).order(OrderStore.orderplacedtime).fetch())]
        print q
        o_list = OrderList(orderlist=q)
        return o_list

    @endpoints.method(message_types.VoidMessage, ItemList,
                      path='items', http_method='GET',
                      name='laundry.getAllItems')
    def item_list(self, unused_request):
        q = [i.to_message() for i in ItemStore.query().fetch()]
        print q
        i_list = ItemList(itemlist=q)
        return i_list

# ---- POST METHODS-----#

    @endpoints.method(Item, message_types.VoidMessage,
                      path='additem', http_method='POST',
                      name='laundry.addItem')
    def add_item(self, request):

        i = ItemStore.put_from_message(request, current_user)
        if i:
            return message_types.VoidMessage()

    @endpoints.method(Order, OrderList,
                      path='placeorder', http_method='POST',
                      name='laundry.placeOrder')
    def place_order(self, request):

        self.get_user_from_cookie()

        if not self.user:
            raise endpoints.UnauthorizedException('Invalid token.')

        userkey_id = self.user['user_id']
        user_key = ndb.Key('User', userkey_id)
        current_user = user_key.get()
        print current_user.username
        o = OrderStore.put_from_message(request, current_user)
        if o:
            import time
            time.sleep(1)
            q = [o.to_message(idx+1) for idx, o in enumerate(OrderStore.query(OrderStore.user.username == current_user.username).order(OrderStore.orderplacedtime).fetch())]
            print q
            o_list = OrderList(orderlist=q)
            return o_list

    @endpoints.method(message_types.VoidMessage, TestMessage,
                      path='testing', http_method='GET',
                      name='testit')
    def testit(self, request):
        # return Item(username='testit')
        self.get_user_from_cookie()

        if not self.user:
            raise endpoints.UnauthorizedException('Invalid token.')

        userkey_id = self.user['user_id']
        user_key = ndb.Key('User', userkey_id)
        user = user_key.get()

        return TestMessage(username=user.username)


APPLICATION = endpoints.api_server([LaundryApi], restricted=False)

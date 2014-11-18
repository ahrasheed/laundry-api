import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from datetime import datetime

package = 'easy'

WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


class Item(messages.Message):
    """Individual clothing items"""
    itemid = messages.IntegerField(1, required=True)
    name = messages.StringField(2, required=True)
    number = messages.IntegerField(3, default=1, required=True)
    weight = messages.FloatField(4)
    rate = messages.FloatField(5)


class Order(messages.Message):
    """Collection of clothes ordered by a user"""
    orderid = messages.IntegerField(1, required=True)
    userid = messages.IntegerField(2, required=True)
    items = messages.MessageField(Item, 3, repeated=True)
    pickuplocation = messages.StringField(4, required=True)
    pickuptime = message_types.DateTimeField(5, required=True)
    droplocation = messages.StringField(6, required=True)
    droptime = message_types.DateTimeField(7, required=True)
    orderplacedtime = message_types.DateTimeField(8, required=True)
    comments = messages.StringField(9)


class ItemList(messages.Message):
    """Item list"""
    itemlist = messages.MessageField(Item, 1, repeated=True)


class OrderList(messages.Message):
    """Order list for user"""
    orderlist = messages.MessageField(Order, 1, repeated=True)
    userid = messages.IntegerField(2)


class ItemStore(ndb.Model):
    """Save Items"""
    item = msgprop.MessageProperty(Item, indexed_fields=['itemid'], required=True)
    status = ndb.BooleanProperty(required=True, default=True)


class OrderStore(ndb.Model):
    """Save order against user objects"""
    order = msgprop.MessageProperty(Order, indexed_fields=['orderid'], required=True)
    completed = ndb.BooleanProperty(required=True)

    # user = ndb.UserProperty(required=True)

TEST_ITEM = Item(itemid=1, name='Shirt', number=3, weight=9.2, rate=1.5)

TEST_ORDER_1 = Order(orderid=2, userid=5, items=[TEST_ITEM], pickuplocation='Ghar', pickuptime=datetime.utcnow(), droplocation='ghar', droptime=datetime.utcnow(), orderplacedtime=datetime.utcnow(), comments='bring in one piece')

TEST_ORDER_2 = Order(orderid=3, userid=6, items=[TEST_ITEM], pickuplocation='Ghar', pickuptime=datetime.utcnow(), droplocation='ghar', droptime=datetime.utcnow(), orderplacedtime=datetime.utcnow(), comments='bring in one piece')

TEST_LIST = OrderList(orderlist=[TEST_ORDER_1, TEST_ORDER_2], userid=5)


@endpoints.api(name='laundry', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class LaundryApi(remote.Service):
    """Laundry API v1."""


    @endpoints.method(message_types.VoidMessage, OrderList,
                      path='orders', http_method='GET',
                      name='laundry.getAllOrders')
    def order_list(self, unused_request):
        q = [o.order for o in OrderStore.query().fetch()]
        o_list = OrderList(orderlist=q)

        return o_list

    @endpoints.method(message_types.VoidMessage, ItemList,
                      path='items', http_method='GET',
                      name='laundry.getAllItems')
    def item_list(self, unused_request):
        q = [i.item for i in ItemStore.query().fetch()]
        i_list = ItemList(itemlist=q)

        return i_list


    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Order,
                      path='orders/{id}', http_method='GET',
                      name='laundry.getOrder')
    def order_get(self, request):

        q = OrderStore.query(OrderStore.order.orderid == request.id).get()
        if q is None:
            raise endpoints.NotFoundException('Order %s not found.' %
                                              (request.id,))
        else:
            return q.order


    @endpoints.method(Order, message_types.VoidMessage,
                      path='placeorder', http_method='POST',
                      name='laundry.placeOrder')
    def place_order(self, request):
        o = OrderStore(order=request, completed=True)
        o.put()
        return message_types.VoidMessage()


    @endpoints.method(Item, message_types.VoidMessage,
                      path='additem', http_method='POST',
                      name='laundry.addItem')
    def add_item(self, request):
        i = ItemStore(item=request)
        i.put()
        return message_types.VoidMessage()


APPLICATION = endpoints.api_server([LaundryApi])

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from bp_includes.models import User

# ----- MESSAGES ------


class Item(messages.Message):
    """Individual clothing items"""
    itemkey = messages.IntegerField(1)
    name = messages.StringField(2)
    weight = messages.FloatField(3)
    rate = messages.FloatField(4)


class ItemCount(messages.Message):
    """Individual clothing items"""
    itemkey = messages.IntegerField(1)
    name = messages.StringField(2)
    number = messages.IntegerField(3, default=1, required=True)
    weight = messages.FloatField(4)
    rate = messages.FloatField(5)


class Order(messages.Message):
    """Collection of clothes ordered by a user"""
    orderkey = messages.IntegerField(1)
    items = messages.MessageField(ItemCount, 2, repeated=True)
    pickuplocation = messages.StringField(3)
    pickuptime = message_types.DateTimeField(4)
    droplocation = messages.StringField(5)
    droptime = message_types.DateTimeField(6)
    orderplacedtime = message_types.DateTimeField(7)
    status = messages.StringField(8)
    comments = messages.StringField(9)
    ordercounter = messages.IntegerField(10)


# class StatusChange(messages.Message):
#     """Status change message"""
#     status = messages.EnumField(OrderStatus, 1, required=True)


class ItemList(messages.Message):
    """Item list"""
    itemlist = messages.MessageField(Item, 1, repeated=True)


class OrderList(messages.Message):
    """Order list for user"""
    orderlist = messages.MessageField(Order, 1, repeated=True)
    userid = messages.IntegerField(2)


# ----- DATE STORE MODELS ------

class ItemCountStore(ndb.Model):
    """Structured Property for Orders"""
    name = ndb.StringProperty()
    number = ndb.IntegerProperty(default=1)
    weight = ndb.FloatProperty()
    rate = ndb.FloatProperty()


class ItemStore(ndb.Model):
    """Save Items"""
    name = ndb.StringProperty()
    weight = ndb.FloatProperty()
    rate = ndb.FloatProperty()

    def to_message(self):
        """Turns the Order into a message"""

        item = Item(itemkey=self.key.id(),
                    name=self.name,
                    weight=self.weight,
                    rate=self.rate
                    )
        return item

    @classmethod
    def put_from_message(cls, message):
        """Insert order from message."""

        item = cls(name=message.name,
                   weight=message.weight,
                   rate=message.rate
                   )
        item.put()

        return item


class OrderStore(ndb.Model):
    """Save Orders"""
    user = ndb.StructuredProperty(User)
    items = ndb.StructuredProperty(ItemCountStore, repeated=True)
    pickuplocation = ndb.StringProperty()
    pickuptime = ndb.DateTimeProperty()
    droplocation = ndb.StringProperty()
    droptime = ndb.DateTimeProperty()
    orderplacedtime = ndb.DateTimeProperty()
    status = ndb.StringProperty(default='INCOMPLETE', choices=['INCOMPLETE', 'INIT', 'PROCESSING', 'ENROUTE', 'COMPLETED'])
    comments = ndb.TextProperty()

    @property
    def orderweight(self):
        """Property to calculate total weight"""
        total = 0
        for item in self.items:
            total += item.weight
        return total

    def to_message(self, index):
        """Turns the Order into a message"""
        itemsie = [ItemCount(name=item.name, number=item.number, weight=item.weight, rate=item.rate) for item in self.items]

        order = Order(orderkey=self.key.id(),
                      items=itemsie,
                      pickuplocation=self.pickuplocation,
                      pickuptime=self.pickuptime,
                      droplocation=self.droplocation,
                      droptime=self.droptime,
                      orderplacedtime=self.orderplacedtime,
                      status=self.status,
                      comments=self.comments,
                      ordercounter=index
                      )
        return order

    def update_status(self, status):
        """Update order stataus"""
        # add checks for completion here if necessary
        self.status = status

    # def update_from_message(self, message):
    #     """Update incomplete orders"""
    #     if message.items:
    #         itemsie = []
    #         for item in message.items:
    #             i = ItemStore.query(ItemStore.itemid == item.itemid).get()
    #             if i:
    #                 itemsie.append(ItemCountStore(name=i.name, number=item.number, weight=i.weight, rate=i.rate))
    #         self.items = itemsie

    #     if message.pickuplocation:
    #         self.pickuplocation = message.pickuplocation

    #     if message.pickuptime:
    #         self.pickuptime = message.pickuptime

    #     if message.droplocation:
    #         self.droplocation = message.droplocation

    #     if message.droptime:
    #         self.droptime = message.droptime

    #     if message.orderplacedtime:
    #         self.orderplacedtime = message.orderplacedtime

    #     if message.comments:
    #         self.comments = message.comments

    @classmethod
    def put_from_message(cls, message, user):
        """Insert order from message."""
        itemsie = []
        if message.items:
            for item in message.items:
                print item.itemkey
                i_key = ndb.Key('ItemStore', item.itemkey)
                i = i_key.get()
                if i:
                    itemsie.append(ItemCountStore(name=i.name, number=item.number, weight=i.weight, rate=i.rate))

        order = cls(user=user,
                    items=itemsie,
                    pickuplocation=message.pickuplocation,
                    pickuptime=message.pickuptime,
                    droplocation=message.droplocation,
                    droptime=message.droptime,
                    orderplacedtime=message.orderplacedtime,
                    status=message.status,
                    comments=message.comments
                    )
        order.put()
        return order


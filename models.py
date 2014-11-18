from google.appengine.ext import endpoints
from google.appengine.ext import ndb


def get_endpoints_current_user(raise_unauthorized=True):
    """Returns a current user and (optionally) causes an HTTP 401 if no user."""

current_user = endpoints.get_current_user()
if raise_unauthorized and current_user is None:
    raise endpoints.UnauthorizedException('Invalid token.')
return current_user


class Order(ndb.Model):
    """Model to store scores that have been inserted by users.
Since the played property is auto_now_add=True, Scores will document when
they were inserted immediately after being stored.
"""
    orderid = ndb.IntegerProperty(required=True)
    outcome = ndb.StringProperty()
    played = ndb.DateTimeProperty(auto_now_add=True)
    # player = ndb.UserProperty(required=True)

    # @property
    # def timestamp(self):
    #     """Property to format a datetime object to string."""
    #     return self.played.strftime(TIME_FORMAT_STRING)

    # def to_message(self):
    #     """Turns the Score entity into a ProtoRPC object.
    # This is necessary so the entity can be returned in an API request.
    # Returns:
    # An instance of ScoreResponseMessage with the ID set to the datastore
    # ID of the current entity, the outcome simply the entity's outcome
    # value and the played value equal to the string version of played
    # from the property 'timestamp'.
    # """
    #     return ScoreResponseMessage(id=self.key.id(),
    #                                 outcome=self.outcome,
    #                                 played=self.timestamp)

    # @classmethod
    # def put_from_message(cls, message):
    #     """Gets the current user and inserts a score.
    # Args:
    # message: A ScoreRequestMessage instance to be inserted.
    # Returns:
    # The Score entity that was inserted.
    # """
    #     current_user = get_endpoints_current_user()
    #     entity = cls(outcome=message.outcome, player=current_user)
    #     entity.put()
    #     return entity

    # @classmethod
    # def query_current_user(cls):
    #     """Creates a query for the scores of the current user.
    # Returns:
    # An ndb.Query object bound to the current user. This can be used
    # to filter for other properties or order by them.
    # """
    #     current_user = get_endpoints_current_user()
    #     return cls.query(cls.player == current_user)



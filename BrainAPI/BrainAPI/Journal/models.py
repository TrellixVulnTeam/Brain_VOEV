from django_neomodel import DjangoNode
from neomodel import StringProperty, DateTimeProperty, UniqueIdProperty, ArrayProperty, IntegerProperty


class Journal(DjangoNode):
    uid = UniqueIdProperty()
    anxiety = StringProperty(required=True)
    body = StringProperty(required=True)
    depression = StringProperty(required=True)
    energy = StringProperty(required=True)
    is_journal_created_today = IntegerProperty(required=True)
    mood = StringProperty(required=True)
    name = StringProperty(required=True)


    class Meta:
        app_label = 'Journal'

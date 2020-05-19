from mongoengine import DynamicField, EmbeddedDocument, LongField, Document, EmbeddedDocumentListField


class EmbeddedValueDocument(EmbeddedDocument):
    timestamp = LongField()
    value = DynamicField()


class ValueDocumentList(Document):
    values = EmbeddedDocumentListField(EmbeddedValueDocument, instance=EmbeddedDocument, name='values')

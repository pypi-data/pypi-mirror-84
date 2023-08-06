from flask import make_response
from invenio_access.permissions import Permission, any_user, authenticated_user
from invenio_records.api import Record
from invenio_records_rest.utils import allow_all
from oarepo_validate import MarshmallowValidatedRecordMixin, SchemaKeepingRecordMixin

from oarepo_actions.decorators import action

from .constants import SAMPLE_ALLOWED_SCHEMAS, SAMPLE_PREFERRED_SCHEMA
from .marshmallow import SampleSchemaV1


def neco():
    return {"xx": "yy"}
def pf(record = None):
    return Permission(any_user)
class SampleRecord(SchemaKeepingRecordMixin,
                   MarshmallowValidatedRecordMixin,
                   Record):
    ALLOWED_SCHEMAS = SAMPLE_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = SAMPLE_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = SampleSchemaV1

    @action(url_path="blah", permissions = allow_all)
    def send_email(self, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(detail=False, url_path="jej", permissions = allow_all)
    def blah1(cls, **kwargs):
        return neco()

    @classmethod
    @action(detail=False, permissions=pf)
    def blah(cls, **kwargs):
        return neco()

    @classmethod
    @action(detail=False, url_path="test/<int:param>",  permissions=pf)
    def blah2(cls, param = None, **kwargs):
        return {param: "yy"}

    @classmethod
    @action(detail=False, url_path='test', permissions=allow_all)
    def test3(cls, param=None, **kwargs):
        return {param: "yy"}

    @classmethod
    @action(detail=False, url_path='test',permissions=allow_all, method='post')
    def test2(cls, param=None, **kwargs):
        return {param: "yy"}

    @action(url_path="blahx", permissions=allow_all, method = 'post')
    def x(self, **kwargs):
        return {"title": self["title"]}

    @action(url_path="blahx", permissions=allow_all)
    def x2(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all, method='get')
    def b(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all,url_path = 'b', method='put')
    def b1(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all,url_path = 'b', method='delete')
    def b2(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all, url_path = 'b', method='post', serializers = {'application/json': make_response})
    def b3(self, **kwargs):
        return {"title": self["title"]}

    _schema = "sample/sample-v1.0.0.json"
    def validate(self, **kwargs):
        return super().validate(**kwargs)

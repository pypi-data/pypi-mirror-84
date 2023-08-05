import logging

from django.db.models import Q, UniqueConstraint, CheckConstraint, F

from isc_common import Wrapper
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditQuerySet, AuditManager, AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations

logger = logging.getLogger(__name__)


class Item_refs_locationQuerySet(AuditQuerySet):
    pass


class Item_refs_locationManager(AuditManager):
    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'child_id': record.child.id,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return Item_refs_locationQuerySet(self.model, using=self._db)

    def updateFromRequest(self, request, removed=None, function=None):
        request = DSRequest(request=request)
        data = request.get_data()

        _data = data.copy()
        _data = Wrapper(**data)
        targetRecord = Wrapper(**_data.targetRecord)
        dropRecords = list(map(lambda dropRecord: Wrapper(**dropRecord), _data.dropRecords))
        return _data


class Item_refs_location(AuditModel):
    location = ForeignKeyProtect(Locations)
    child = ForeignKeyProtect(Item, related_name='Item_refs_location_child')
    parent = ForeignKeyProtect(Item, related_name='Item_refs_location_parent', blank=True, null=True)

    objects = Item_refs_locationManager()
    objects1 = TreeAuditModelManager()

    def __str__(self):
        return f'\nID={self.id}, child=[{self.child}], parent=[{self.parent}]'

    class Meta:
        verbose_name = 'Item_refs_location'
        constraints = [
            CheckConstraint(check=~Q(child=F('parent')), name='Item_refs_location_not_circulate_refs'),
            UniqueConstraint(fields=['child_id'], condition=Q(parent_id=None), name='Item_refs_location_unique_constraint_0'),
            UniqueConstraint(fields=['child_id', 'parent_id'], name='Item_refs_location_unique_constraint_1'),
        ]

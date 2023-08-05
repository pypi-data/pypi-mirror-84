import logging

from django.db.models import Q, UniqueConstraint, CheckConstraint, F

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditQuerySet, AuditManager, AuditModel
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DelProps
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.kd.models.document_attributes import Document_attributes

logger = logging.getLogger(__name__)


class Item_refs_location_viewQuerySet(AuditQuerySet):
    pass


class Item_refs_location_viewManager(AuditManager):
    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_1__value_str': record.STMP_1.value_str if record.STMP_1 else None,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'STMP_2__value_str': record.STMP_2.value_str if record.STMP_2 else None,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return Item_refs_location_viewQuerySet(self.model, using=self._db)


class Item_refs_location_view(AuditModel):
    location = ForeignKeyProtect(Locations)
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='Item_refs_location_view_STMP_1_view', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='Item_refs_location_view_STMP_2_view', null=True, blank=True)
    parent = ForeignKeyProtect(Item, related_name='Item_refs_location_view_parent', blank=True, null=True)

    objects = Item_refs_location_viewManager()
    objects1 = TreeAuditModelManager()

    def __str__(self):
        return f'\nID={self.id}, child=[{self.child}], parent=[{self.parent}]'

    class Meta:
        verbose_name = 'Item_refs_location_view'
        constraints = [
            CheckConstraint(check=~Q(child=F('parent')), name='Item_refs_location_view_not_circulate_refs'),
            UniqueConstraint(fields=['child_id'], condition=Q(parent_id=None), name='Item_refs_location_view_unique_constraint_0'),
            UniqueConstraint(fields=['child_id', 'parent_id'], name='Item_refs_location_view_unique_constraint_1'),
        ]

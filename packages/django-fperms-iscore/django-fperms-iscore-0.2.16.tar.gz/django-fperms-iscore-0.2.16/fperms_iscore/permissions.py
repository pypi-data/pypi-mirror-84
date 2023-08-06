from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

from fperms import get_perm_model

from fperms_iscore import enums

from is_core.auth.permissions import IsAuthenticated


Perm = get_perm_model()


permissions = {}


GENERAL_CACHE_NAME = '__all__'


def _get_perm_slug_from_data(perm_type, perm_codename, object_ct=None, object_id=None):
    slug = '{}|{}'.format(perm_type, perm_codename)
    if object_ct and object_id:
        return '{}|{}|{}'.format(slug, object_ct.pk, object_id)
    return slug


def _get_perm_slug_from_obj(perm_type, perm_codename, obj=None):
    from django.contrib.contenttypes.models import ContentType

    object_ct = object_id = None
    if obj is not None:
        object_ct = ContentType.objects.get_for_model(obj)
        object_id = obj.pk
    return _get_perm_slug_from_data(perm_type, perm_codename, object_ct, object_id)


def _get_perm_slug(perm):
    return _get_perm_slug_from_data(perm.type, perm.codename, perm.content_type, perm.object_id)


class FPermPermission(IsAuthenticated):

    def __init__(self, name, verbose_name=None, register=True):
        """
        :param name: name of the permission stored as codename in `Perm` model
        :param verbose_name: verbose name of the permission
        """
        self.name = name
        self.verbose_name = verbose_name
        if register:
            self._register()

    def _register(self):
        if self.name in permissions:
            raise ImproperlyConfigured('Duplicite permission with name {}'.format(self.name))
        permissions[self.name] = self

    def has_permission(self, name, request, view, obj=None):
        """
        Return `True` if user has set permission of is superuser
        """
        if not super().has_permission(name, request, view, obj):
            return False

        user = request.user
        if user.is_superuser:
            return True

        if not hasattr(user, '_fperms_is_core_user_perm_slugs'):
            user._fperms_is_core_user_perm_slugs = set(
                _get_perm_slug(p) for p in user.fperms.all_perms()
            )

        user_perm_slugs = user._fperms_is_core_user_perm_slugs
        return (
            _get_perm_slug_from_obj(enums.PERM_TYPE_CORE, self.name) in user_perm_slugs
            or (
                obj is not None
                and _get_perm_slug_from_obj(enums.PERM_TYPE_CORE, self.name, obj=obj) in user_perm_slugs
            )
        )

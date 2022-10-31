from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


class MainModel(models.Model):
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField("更新时间", auto_now=True, null=True, blank=True)
    is_deleted = models.IntegerField("是否删除", default=0)
    deleted = models.DateTimeField("删除时间", auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, name, username,  password=None):
        if not username:
            raise ValueError("用户名为必填")
        user = self.model(name=name, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, password=None):
        user = self.model(name=name, username=username)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, blank=True)

    groups = None
    user_permissions = None
    first_name = None
    last_name = None
    email = None

    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name or self.username

    class Meta:
        verbose_name = "账号"
        verbose_name_plural = verbose_name

    def get_user_permissions(self, obj=None):
        return None

    def get_group_permissions(self, obj=None):
        return None

    def get_all_permissions(self, obj=None):
        return None

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



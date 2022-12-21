from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from ckeditor.fields import RichTextField


class MainModel(models.Model):
    created = models.DateTimeField("创建时间", auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField("更新时间", auto_now=True, null=True, blank=True)
    is_deleted = models.IntegerField("是否删除", default=0)
    deleted = models.DateTimeField("删除时间", auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Grade(MainModel):
    name = models.CharField('名称', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name


class UserManager(BaseUserManager):
    def create_user(self, name, username, password=None):
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
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
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


STATUS = (
    (0, '禁用'),
    (1, '正常'),
)

BOOLEAN_STATUS = (
    (0, '否'),
    (1, '是'),
)


class Feedback(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = RichTextField('内容', null=True, blank=True)
    is_private = models.IntegerField("保密信息", choices=((0, "否"), (1, '是')), default=0, help_text="保密信息只有老师能看到")
    feedback = RichTextField('回复', null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS, default=1)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "意见与建议"
        verbose_name_plural = verbose_name

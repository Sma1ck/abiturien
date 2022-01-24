from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from transliterate.utils import _
from .models import CustomUser, DocumentUser, AdditionalInfo, PublishTab, PublishRecTab
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

"""
    Модель пользователя и inline 
"""


class UserInline(admin.StackedInline):
    """Доп. форма для пользователей с информацией из models.CustomUser"""
    model = CustomUser
    can_delete = False
    # fields = ('phone_number','work_flag',' agreement_flag', 'complete_flag',
    # 'sending_status', 'date_of_birth', 'patronymic')
    verbose_name_plural = 'Доп. информация'


class UserInlineInfo(admin.TabularInline):
    """Доп. форма для пользователей с информацией из models.AdditionalInfo"""
    model = AdditionalInfo
    verbose_name_plural = 'Информация о формах'
    extra = 0


class UserInlinePublish(admin.StackedInline):
    """Доп. форма для пользователей с информацией из models.PublishTab"""
    model = PublishTab
    can_delete = False
    verbose_name_plural = 'Опубликовать в Списки подавших'
    extra = 0


class UserInlineRec(admin.StackedInline):
    """Доп. форма для пользователей с информацией из models.PublishTab"""
    model = PublishRecTab
    can_delete = False
    verbose_name_plural = 'Опубликовать в Списки Рекомендованных к зачислению'
    extra = 0


class UserInlineDoc(admin.TabularInline):
    """Доп. форма для пользователей с информацией из models.DocumentUser"""
    model = DocumentUser
    can_delete = False
    verbose_name_plural = 'Документы'
    readonly_fields = ['name_doc', 'doc', 'date_pub']
    ordering = ('-date_pub', )
    extra = 1


class UserAdmin(UserAdmin):
    """Представление модели User"""
    model = DocumentUser
    inlines = (UserInline, UserInlineInfo, UserInlinePublish, UserInlineRec, UserInlineDoc)
    list_display = ('id', 'username', 'first_name', 'last_name', 'date_joined',
                    'email',  'status_doc', 'comment')
    list_display_links = ('id', 'username', )
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Персональная информация'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('id', 'username', 'first_name', 'last_name',)

    readonly_fields = [
        'user_permissions',
        'groups',
        'is_active',
        'password',
        'last_login',
        'is_superuser',
        'is_staff'
    ]

    def comment(self, obj):
        """Выводим в list_display комментарий"""
        comment = obj.custom.comment_admin
        return comment

    def status_doc(self, obj):
        status = obj.custom.complete_flag
        work = obj.custom.work_flag
        success = obj.custom.success_flag
        result = None
        if obj.custom.sending_status == 'back':
            return('Заявка отозвана')
        if status:
            result = "Документы поданы"
        elif status != 'True':
            result = " Не поданы "
        if success:
            return mark_safe(
                '<div style="width:100%%; height:100%%; '
                'background-color:green;">{0}</div>'.format(result))
        if work:
            return mark_safe('<div style="width:100%%; height:100%%; '
                             'background-color:orange;">{0}</div>'.format(result))

        return mark_safe(result)


"""
    Регистрация остальных моделей 
"""


class DocUser(admin.ModelAdmin):
    """Модель Документов пользователей"""
    list_display = ('user_id', 'user', 'name_doc', 'doc')
    list_filter = ('date_pub',)
    readonly_fields = ('user', )


class CustomUserResource(resources.ModelResource):
    """Класс, формирующий dateset из админ-панели"""
    class Meta:
        model = CustomUser


class CustomUserResource(ImportExportModelAdmin):
    """Класс, реализующий выгрузку из админ-панели"""
    resource_class = CustomUserResource


# Register your models here.
admin.site.register(DocumentUser, DocUser)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(CustomUser, UserAdmin)
# admin.site.register(CustomUser, CustomUserResource)


# class DocumentUserResource(resources.ModelResource):
#     """Класс, формирующий dateset из админ-панели"""
#     class Meta:
#         model = DocumentUser
#
#
# class DocumentUserResource(ImportExportModelAdmin):
#     """Класс, реализующий выгрузку из админ-панели"""
#     resource_class = DocumentUserResource


# class DocUserInline(admin.StackedInline):
#     model = User
#     fk_name = 'id'
#     can_delete = False
#     verbose_name = 'Абитуриент'
#     fields = ['first_name', 'last_name', ]
#
#     #, 'patronymic', 'date_of_birth', 'sending_status', 'phone_number'

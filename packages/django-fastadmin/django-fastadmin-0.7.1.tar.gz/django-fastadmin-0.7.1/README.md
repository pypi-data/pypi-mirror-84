# django-fastadmin

django admin extensions.

## Install

```shell
pip install django-fastadmin
```

## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    "django_static_jquery3",
    "django_static_ace_builds",
    "django_apiview",
    'django_fastadmin',
    ...
]
```

- Add dependence package names in INSTALLED_APPS.


## Installed Admin Extensions

### Admin extends

- UuidFieldSearchableAdmin
- InlineBooleanFieldsAllowOnlyOneCheckedMixin
- InlineUniqueChoiceFieldsMixin # @todo
- DisableDeleteActionMixin
- InlineEditingHideOriginalMixin
- DisableInlineEditingInAddingMixin
- DisableAddPermissionMixin
- DisableDeletePermissionMixin
- DisableChangePermissionMixin
- MarkPermissionsMixin
- TextFieldAutoHeightMixin
- TextFieldSetRowColumnMixin
- ResetToRandomPasswordField
- EditablePasswordField
- HideShowField
- AddAdminViewHelper
- ToggleFieldStateAdmin
- SetTopModelAdmin
- DjangoAdminGlobalMedia
- DjangoWithExtraContextAdmin
- DjangoDynamicMediaAdmin
- HiddenFieldsAdmin
- HideShowFieldsOnValueAdmin

### Widgets

- AceWidget
- TitleToCodeWidget

### Services

- SimpleTaskService

### Forms

### Filters


## admin.InlineBooleanFieldsAllowOnlyOneCheckedMixin Usage

- `django_static_jquery3` required in INSTALLED_APPS.
- Add this mixin to inline class, and put it before TabularInline.
- Add classes property
    - Add class InlineBooleanFieldsAllowOnlyOneCheckedMixin.special_class_name
    - Add class InlineBooleanFieldsAllowOnlyOneCheckedMixin.field_name_prefix + {field name},
- Example:
    ```
    from django.contrib import admin
    from django_fastadmin.admin import InlineBooleanFieldsAllowOnlyOneCheckedMixin

    from .models import Book
    from .models import Category

    class BookInline(InlineBooleanFieldsAllowOnlyOneCheckedMixin, admin.TabularInline):
        model = Book
        extra = 0
        classes = [
            InlineBooleanFieldsAllowOnlyOneCheckedMixin.special_class_name,
            InlineBooleanFieldsAllowOnlyOneCheckedMixin.field_name_prefix + "is_best_seller",
            ]


    class CategoryAdmin(admin.ModelAdmin):
        inlines = [
            BookInline,
        ]

    admin.site.register(Category, CategoryAdmin)
    ```



## widget.AceWidget Usage

- `django_static_jquery3` and `django_static_ace_builds` required in INSTALLED_APPS.
- Create a model_form, and set the admin's form to the model_form.
- Set the field to use AceWidget in the model_form.
- Example:
```
class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "description": AceWidget(ace_options={
                "mode": "ace/mode/yaml",
                "theme": "ace/theme/twilight",
            }),
        }

class BookAdmin(admin.ModelAdmin):
    form = BookModelForm
    list_display = ["title", "published"]

```

## Bug report

Please report any issues at https://github.com/zencore-cn/zencore-issues.

## Releases

### v0.7.1 2020/11/08

- Fix missing django-static-ace-builds problem.

### v0.7.0 2020/10/27

- Remove abstract models, so that django_fastadmin can forcus on admin extensions.
- SimpleTask moved to django_simpletask.
- SimplePublishModel and SimplePublishModelAdmin moved to django_simple_publish_model.


### v0.6.2 2020/10/24

- Fix DjangoWithExtraContextAdmin problem.

### v0.6.1 2020/10/21

- Upgrade django-db-lock, fix missing requests in setup problem.

### v0.6.0 2020/10/13

- Add admin.DjangoAdminGlobalMedia.
- Add admin.DjangoWithExtraContextAdmin.
- Add admin.DjangoDynamicMediaAdmin.
- Add admin.HiddenFieldsAdmin.
- Add admin.HideShowFieldsOnValueAdmin.
- Add admin.DjangoObjectToolbarAdmin.
- Add admin.DjangoSortableAdmin.
- Add depends.

### v0.5.0 2020/10/01

- Add admin.AddAdminViewHelper.
- Add admin.ToggleFieldStateAdmin.
- Add admin.SimplePublishModelAdmin.
- Add admin.SetTopModelAdmin.

### v0.4.0 2020/09/23

- Add widgets.TitleToCodeWidget.
- Add models.SimplePublishModel.
- Add many admin mixins.
- Add app_requires.

### v0.3.2 2020/09/08

- Add SimpleTaskService.
- Move service functions from model to service.
- Upgrade django_db_lock depends.

### v0.3.1 2020/09/01

- Rename zh_hans to zh_Hans.
- Depends on django-db-lock>=0.3.1.
- Add django-static-xxx depends.

### v0.3.0 2020/09/01

- Change the directory structure of static files.
- Add models.SimpleTask. It's an abstract model.
- jQuery and jQuery plugins are moved to django-static-jquery3>=5.0.0.

### v0.2.0 2020/08/25

- Add widgets.AceWidget.

### v0.1.1 2020/08/13

- Fix jquery.js and jquery.init.js including orders, so that we don't need to change js plugin's source to use django.jQuery.

### v0.1.0 2020/08/12

- First release.
- Add UuidFieldSearchableAdmin.
- Add InlineBooleanFieldsAllowOnlyOneCheckedMixin.
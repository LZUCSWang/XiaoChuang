from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import (
    account,
    datasets,
    dataset,
    explore,
    category,
    subcategory,
    item,
    diary,
    music,
    Questionnaire,
    Question,
    Option,
)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "result"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["questionnaire", "text", "option1", "option2", "option3", "option4", "option5", "option6", "option7"]


class OptionAdmin(admin.ModelAdmin):
    list_display = [ "text", "value"]


class categoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class subcategoryadmin(admin.ModelAdmin):
    list_display = ["category", "name"]


class itemAdmin(admin.ModelAdmin):
    list_display = ["category", "subcategory", "name", "description"]


class diaryAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "weather", "mood", "background"]


class musicAdmin(admin.ModelAdmin):

    list_display = ["src", "poster", "name", "artist", "lyric", "sublyric"]


# class dataAdmin(admin.ModelAdmin):
#     list_display = ['username', 'password_md5', 'dataset_id', 'dataset_name', 'dataset_created_time',
#                     'dataset_updated_time', 'img_id', 'img_name', 'img_created_time', 'img_class', 'img_show']
#     list_filter = ['username', 'dataset_name']
#     # readonly_fields = ["password_md5", 'dataset_created_time',
#     #                    'dataset_updated_time', 'img_created_time', 'img_class','dataset_id','img_id']
#     # def delete_selected(self, request, queryset):
#     #     # 自定义的删除选择的操作
#     #     for obj in queryset:
#     #         obj.delete()
#     #     self.message_user(request, "Articles successfully deleted.")


class exploreAdmin(admin.ModelAdmin):
    list_display = ["id", "parent", "post_time", "content"]


# class accountAdmin(admin.ModelAdmin):
#     list_display = ["username", "password_md5"]
#     # list_filter = ['username']


# class datasetsAdmin(admin.ModelAdmin):
#     list_display = [
#         "dataset_id",
#         "dataset_name",
#         "dataset_created_time",
#         "dataset_updated_time",
#         "account",
#     ]
#     list_filter = ["account"]


# class datasetAdmin(admin.ModelAdmin):
#     list_display = [
#         "data_id",
#         "data_name",
#         "data_created_time",
#         "data_class",
#         "dataset",
#         "account",
#         "data_path",
#     ]
#     list_filter = ["dataset", "data_class", "account"]
#     # readonly_fields = ('data_path',)  # 必须加这行 否则访问编辑页面会报错
#     # def data_path(self, obj):
#     #     return mark_safe(u'< img src="%s" width="100px" />' % obj.file.url)
#     # # def data_path(self, obj):
#     # #     return obj.image.url if obj.image else ''

#     # data_path.short_description = 'Image'
#     # # 页面显示的字段名称
#     # # image_data.short_description = u'品牌图片'


# admin.site.register(data, dataAdmin)
# admin.site.register(account, accountAdmin)
# admin.site.register(datasets, datasetsAdmin)
# admin.site.register(dataset, datasetAdmin)
admin.site.register(explore, exploreAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(subcategory, subcategoryadmin)
admin.site.register(item, itemAdmin)
admin.site.register(diary, diaryAdmin)
admin.site.register(music, musicAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)

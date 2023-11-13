from sre_parse import State
from django.contrib import admin
from django.contrib import messages
from registration.coach_models import CoachModel, MasterCoachLabels

from registration.modelhome import SocialMediaLink
from .models import Clubs,RazorpayPlayerRelation,MasterAmount, MasterCategory, MasterDateLimit, MasterRoles, MasterSeason, MasterState,MasterCity,MasterGroup,MasterPosition,MasterLabels, FailedPayment,Player,MasterGroupCity,Upload,Uploadfile,MasterDocument, MasterPartner ,MasterColumn,Lang,ScoutCourse,ScoutCourseDiscount,ScoutDiscountType,WorkShopsReg_Images,WorkShopsRegButton,WorkShopsRegExperts,WorkShopsRegFeatureStrip,TabelWorkshopsReg,TrialsAndInitiativeNav,TrialsAndInitiativeType,ActiveStatusNav,AttendanceStatus,HomeBanner,Winners_Workshop_Images,Previous_Workshop_Images,Testimonials
# Register your models here.
import csv
from django.http import HttpResponse
def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response
admin.site.add_action(export_as_csv)

@admin.register(MasterState)
class MasterStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'include',)
    search_fields = ('id', 'name',)

@admin.register(MasterDateLimit)
class MasterDateLimitAdmin(admin.ModelAdmin):
    list_display = ('id', 'lowerlimit', 'upperlimit','season')

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('unique', 'image',)
    search_fields = ('unique',)


@admin.register(Uploadfile)
class UploadfileAdmin(admin.ModelAdmin):
    list_display = ('unique', 'file')
    search_fields = ('unique',)


@admin.register(MasterCity)
class MasterCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'state', 'include')
    search_fields = ('id', 'city',)


@admin.register(MasterGroupCity)
class MasterGroupCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'cityid_id', 'groupid_id',
                    'include', 'get_city','get_group')
    search_fields = ('id', 'cityid_id__city')

    def get_city(self, obj):
        result = MasterCity.objects.filter(
            id=obj.cityid_id).select_related().values()
        return result[0]['city']

    def get_group(self, obj):
        result = MasterGroup.objects.filter(
            id=obj.groupid_id).select_related().values()
        finalgroup = result[0]['group'] + " "+result[0]['gender']
        return finalgroup
    get_city.short_description = 'City'
    get_group.short_description = 'Group'


@admin.register(MasterGroup)
class MasterGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'gender', 'year',
                    'start', 'end', 'include', 'orderid')
    search_fields = ('group', 'gender', 'year', 'start', 'end',)


@admin.register(MasterPosition)
class MasterPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'label')
    search_fields = ('position', 'label',)


@admin.register(MasterLabels)
class MasterLabelsAdmin(admin.ModelAdmin):
    list_display=('id','keydata','en','extrainfo','hi','mr','asm','ben','odia','bodo')
    search_fields=('keydata','en',)

@admin.register(MasterDocument)
class MasterDocumentsAdmin(admin.ModelAdmin):
    list_display=('id','keydata','en','hi','mr','asm','ben','odia','bodo','include')
    search_fields=('keydata','en',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    
    list_filter = ('status','team',"position1",'error_description','gender','group_id','tournament_state', 'tournament_city_id','whatsapp_sent','player_added_interakt',
                   'primary_position', 'secondary_position','coach_id','extrafield1','discount',)
    list_display = ('id', 'ikfuniqueid',  'first_name',  'last_name','present', 'gender', 'mobile', 'email', 'dob','selection', 'height', 'weight','primary_position', 'secondary_position', 'tournament_city', "tournament_state",
                    'group_id','whatsapp_sent','player_added_interakt', 'season_id', 'category_id', 'whoisfilling_id', 'status','order_id', 'razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature', 'error_code', 'error_description', 'error_source', 'error_reason', 'error_meta_order_id', 'error_meta_payment_id','document_id_selected','document_id_number','pic_file','document_id_file','created_at','updated_at','team',"position1",'playeruploadid','extrafield1',)
    search_fields = ('ikfuniqueid', 'playeruploadid', 'first_name', 'last_name','razorpay_order_id','razorpay_payment_id','error_meta_payment_id','coach_id')
    list_editable = ['present', 'selection']
    # def has_delete_permission(self, request, obj=None):
    #     return False
    # list_filter=('tournament_state',CityListFilter)

    # def make_active(modeladmin, request, queryset):
    #     queryset.update(is_active=1)
    #     messages.success(
    #         request, "Selected Record(s) Marked as Active Successfully !!")

    # def make_inactive(modeladmin, request, queryset):
    #     queryset.update(is_active=0)
    #     messages.success(
    #         request, "Selected Record(s) Marked as Inactive Successfully !!")
    # admin.site.add_action(make_active, "Make Active")
    # admin.site.add_action(make_inactive, "Make Inactive")


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'url', 'type_of_link', 'include')
    search_fields = ('name',)


# @admin.register(NoticeBoard)
# class NoticeBoardAdmin(admin.ModelAdmin):
#     list_display=('id','title','description','include','isHeading')
#     search_fields=('title',)




@admin.register(MasterSeason)
class MasterSeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'en', 'year')
    search_fields = ('id',)


@admin.register(MasterCategory)
class MasterCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'en',)
    search_fields = ('id',)


@admin.register(MasterRoles)
class MasterRolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'en', 'include')
    search_fields = ('id',)


@admin.register(MasterAmount)
class MasterAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'season', 'category',
                    'group_id', 'coach_or_player_id', 'amount', 'discount')
    search_fields = ('id','city__city')


@admin.register(FailedPayment)
class FailedPaymentAdmin(admin.ModelAdmin):
    list_display=('id','ikfuniqueid','playeruploadid','status','razorpay_payment_id','razorpay_order_id','razorpay_signature','error_code','error_description','error_source','error_reason','error_meta_order_id','error_meta_payment_id')
    

@admin.register(MasterPartner)
class MasterPartnerAdmin(admin.ModelAdmin):
    list_display=('id','partner_name','mobile','city_id','city','season_id','category_id','email','address','include')
    search_fields=('id','city__city')
    def get_city(self, obj):
        result = MasterCity.objects.filter(
            id=obj.cityid_id).select_related().values()
        return result[0]['city']
    
@admin.register(MasterCoachLabels)
class MasterCoachLabelsAdmin(admin.ModelAdmin):
    list_display=('id','keydata','en','extrainfo','hi','mr','asm','ben','odia','bodo')
    search_fields=('keydata','en',)

@admin.register(CoachModel)
class CoachModelAdmin(admin.ModelAdmin):
    list_display=('id','coach_id','coach_name','coach_email','coach_mobile','tournament_city','tournament_state','academy_name','academy_mobile','academy_email','barcode_url')
    search_fields=('id','coach_id','coach_mobile')

@admin.register(MasterColumn)
class MasterColumnAdmin(admin.ModelAdmin):
    list_display=('id','columnid','label_key','includep1','includep2','type','orderid')
    search_fields=('columnid','label_key',)

@admin.register(RazorpayPlayerRelation)
class RazorpayPlayerRelationAdmin(admin.ModelAdmin):
    list_display=('id','order_id')
    search_fields=('id','order_id')


@admin.register(ScoutCourse)
class ScoutCourseAdmin(admin.ModelAdmin):
    list_display=('id','course','amount')
    

@admin.register(ScoutDiscountType)
class ScoutDiscountTypeAdmin(admin.ModelAdmin):
    list_display=('id','type','length')
    

@admin.register(ScoutCourseDiscount)
class ScoutCourseDiscountAdmin(admin.ModelAdmin):
    list_display=('id','course','type','discount')






@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang')
    search_fields = ('id', 'lang',)

@admin.register(TabelWorkshopsReg)
class TabelWorkshopsReg(admin.ModelAdmin):
    list_display = ('id', 'keydata',  'First_Column', 'Second_Column', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(WorkShopsRegButton)
class WorkShopsRegButton(admin.ModelAdmin):
    list_display = ('id', 'keydata',  'button_text', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(WorkShopsRegFeatureStrip)
class WorkShopsRegFeatureStrip(admin.ModelAdmin):
    list_display = ('id', 'keydata',  'heading', 'paragraph', 'pic', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(WorkShopsRegExperts)
class WorkShopsRegExperts(admin.ModelAdmin):
    list_display = ('id', 'keydata',  'heading1', 'heading2', 'button_text', 'paragraph', 'pic', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(WorkShopsReg_Images)
class WorkShopsReg_Images(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic', 'name', 'lang',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(ActiveStatusNav)
class ActiveStatusNavAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id', )


@admin.register(TrialsAndInitiativeType)
class TrialsAndInitiativeTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'keydata')
    search_fields = ('id', 'keydata',)


@admin.register(TrialsAndInitiativeNav)
class TrialsAndInitiativeNavAdmin(admin.ModelAdmin):
    list_display = ('id', 'keydata',  'name', 'href', 'description', 'bottomtext', 'listtext', 'pagetype', 'activestatus', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    list_filter = ('pagetype',)
    search_fields = ('id', 'keydata', 'name')
@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic', 'name', 'heading_1', 'heading_2_colored', 'description', 'button1_text', 'button2_text', 'lang', 'attr1', 'attr2', 'attr3', 'attr4',
                    )
    search_fields = ('id', 'keydata', 'name')


@admin.register(Previous_Workshop_Images)
class Previous_Workshop_Images(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic', 'lang',
                    )
    search_fields = ('id', 'keydata', 'name')

@admin.register(Winners_Workshop_Images)
class Winners_Workshop_Images(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic', 'lang',
                    )
    search_fields = ('id', 'keydata', 'name')

@admin.register(Testimonials)
class Testimonials(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic','description', 'lang',
                    )
    search_fields = ('id', 'keydata', 'name')




@admin.register(Clubs)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'keydata', 'size', 'pic', 'lang',
                    )
    search_fields = ('id', 'keydata',)
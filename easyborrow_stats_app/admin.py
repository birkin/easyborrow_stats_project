from django.contrib import admin
from easyborrow_stats_app.models import RequestEntry, HistoryEntry




# <https://docs.djangoproject.com/en/2.2/topics/db/multi-db/>

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'ezborrow_legacy'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

    ## end class MultiDBModelAdmin()




# class RequestEntryAdmin(admin.ModelAdmin):
class RequestEntryAdmin( MultiDBModelAdmin ):

    using = 'ezborrow_legacy'

    list_display = [ 'title', 'wc_accession_num', 'create_date' ]
    # list_filter = [
    #     'project_contact_email',
    #     'code_versioned',
    #     'has_public_code_url',
    #     'responsive',
    #     'contains_lightweight_data_reporting',
    #     'accessibility_check_run',
    #     'data_discoverable',
    #     'has_sitechecker_entry',
    #     'framework_supported',
    #     'https_enforced',
    #     'admin_links_shib_protected',
    #     'logs_rotated',
    #     'patron_data_expiration_process',
    #     'django_session_data_expired',
    #     'emails_admin_on_error',
    #     'vulnerabilities_fixed'
    # ]
    ordering = [ 'title' ]

    readonly_fields = [ 'create_date' ]

    # prepopulated_fields = { "slug": ("project_name",) }

    save_on_top = True

    ## class TrackerAdmin()


admin.site.register( RequestEntry, RequestEntryAdmin )

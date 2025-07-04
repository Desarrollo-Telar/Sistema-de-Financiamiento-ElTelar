from django.contrib import admin

# Modelos
from .models import Document, DocumentCustomer, DocumentAddress, DocumentGuarantee, DocumentOther, DocumentBank

# Formularios
from .forms import DocumentForms

# Register your models here.
admin.site.register(DocumentBank)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForms
    list_display = ('document', 'description')
    search_fields = ('document', 'description')
    

@admin.register(DocumentAddress)
class DocumentAddressAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'address_id','customer_id')
    search_fields = ('document_id','address_id' ,'customer_id')
    list_filter=('customer_id',)

@admin.register(DocumentCustomer)
class DocumentCustomerAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'customer_id')
    search_fields = ('document_id', 'customer_id')
    list_filter=('customer_id',)

@admin.register(DocumentGuarantee)
class DocumentGuaranteeAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'investment_plan_id','customer_id')
    search_fields = ('document','investment_plan_id' ,'customer_id')
    list_filter=('customer_id',)

@admin.register(DocumentOther)
class DocumentOtherAdmin(admin.ModelAdmin):
    list_display = ('document_id','description', 'customer_id')
    search_fields = ('document_id','description' ,'customer_id')
    list_filter = ('customer_id',)
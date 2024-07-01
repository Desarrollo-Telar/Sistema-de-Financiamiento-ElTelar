from django.shortcuts import render, get_object_or_404, redirect
# FORMULARIO
from .forms import DocumentForms

# MODELOS
from .models import Document, DocumentAddress, DocumentCustomer, DocumentGuarantee, DocumentOther
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan


# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
@usuario_activo
def create_document_customer(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'documents/create/create_documents_customers.html'
    if request.method == 'POST':
        form = DocumentForms(request.POST, request.FILES)

        if form.is_valid():
            documento = Document()
            documento.document = form.cleaned_data.get('document')
            documento.description = form.cleaned_data.get('description')
            documento.save()
            document_customer = DocumentCustomer(document_id=documento, customer_id=customer_id)
            document_customer.save()
            return redirect('customers:detail',customer_code)

    form = DocumentForms
    context = {
        'form':form,
        'customer_code':customer_code
    } 

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_documente_address(request, addrress_id ,customer_code):
    addrress_id = get_object_or_404(Address, id = addrress_id)
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'documents/create/create_documents_address.html'
    if request.method == 'POST':
        form = DocumentForms(request.POST, request.FILES)

        if form.is_valid():
            documento = Document()
            documento.document = form.cleaned_data.get('document')
            documento.description = form.cleaned_data.get('description')
            documento.save()
            document_customer = DocumentAddress(document_id=documento, customer_id=customer_id, addrress_id=addrress_id)
            document_customer.save()
            return redirect('customers:detail',customer_code)

    form = DocumentForms
    context = {
        'form':form,
        'addrress_id':addrress_id.id,
        'customer_code':customer_code
    } 

    return render(request, template_name, context)   
 
@login_required
@usuario_activo
def create_documente_guarantee(request, investment_plan_id ,customer_code):
    investment_plan_id = get_object_or_404(InvestmentPlan, id = investment_plan_id)
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'documents/create/create_documents_guarantee.html'
    if request.method == 'POST':
        form = DocumentForms(request.POST, request.FILES)

        if form.is_valid():
            documento = Document()
            documento.document = form.cleaned_data.get('document')
            documento.description = form.cleaned_data.get('description')
            documento.save()
            document_customer = DocumentGuarantee(document_id=documento, customer_id=customer_id, investment_plan_id=investment_plan_id)
            document_customer.save()
            return redirect('customers:detail',customer_code)

    form = DocumentForms
    context = {
        'form':form
    } 

    return render(request, template_name, context) 

@login_required
@usuario_activo
def delete(request, id, customer_code):    
    document = get_object_or_404(Document, id=id)
    document.delete()
    return redirect('customers:detail',customer_code)

@login_required
@usuario_activo
def update_document(request, id, customer_code):
    documento = get_object_or_404(Document, id=id)
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    template_name = 'documents/update/update_documents.html'

    if request.method == 'POST':
        form = DocumentForms(request.POST, request.FILES)
        if form.is_valid():
            documento.document = form.cleaned_data.get('document')
            documento.description = form.cleaned_data.get('description')
            documento.save()
            return redirect('customers:detail',customer_code)
    initial_data = {
        'description':documento.document,
        'document':documento.description, 
    }
    form = DocumentForms(initial=initial_data)

    context = {
        'form':form,
        'document_id':id,
        'customer_code':customer_code
    }

    return render(request, template_name, context)

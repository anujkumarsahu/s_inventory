from datetime import timezone
from django.db import  connections,transaction
from django.db.models import Sum,F
from django.shortcuts import render, redirect
from django .http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from inventry_app.forms import *
from .models import *
from  django.contrib import messages

# Create your views here.

def index(request):
    return render(request,'dashboard/index.html')

#....................supplier.................
def supplier(request):
    supplier = Supplier.objects.all()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_mast')
    else:
        form = SupplierForm()
    return render(request,
                  'dashboard/supplier_mast.html',
                  {'form':form,'supplier':supplier})

            
def edit_supplier(request, id):
    supplier1=  get_object_or_404(Supplier,pk=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier1)
        if form.is_valid():
            form.save()
            return redirect('supplier_mast')
    else:
        form=SupplierForm(instance=supplier1)
    return render(request,'dashboard/edit_supplier.html',
                  {'form':form ,'supplier1':supplier1})
        
        
def delete_supplier(request,id):
    id = get_object_or_404(Supplier,id= id)
    id.delete()
    return redirect('supplier_mast') 

    
# .............end supplier..............


#.................. items ...............
def items(request):
    items = Item.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm()
    return render(request, 
                  'dashboard/items.html', 
                  {'form': form, 'items': items})



def edit_item(request, id):
    item = get_object_or_404(Item, pk=id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'dashboard/edit_item.html',
                   {'form': form, 'item': item})

#delete item data
def delete_items(request, id):
    item = get_object_or_404(Item, pk=id)  
    item.delete()
    return redirect('items')
#...............end item ..........................



#.......... purchase .......................

def purchase(request):
    pmform = PurchaseForm()
    pdform = PurchaseDetailForm()
    
    if request.method == 'POST':
        pmform = PurchaseForm(request.POST)
        pdform = PurchaseDetailForm(request.POST)
        if pmform.is_valid() and pdform.is_valid():
            invoice = pmform.cleaned_data['invoice']
            supplier = pmform.cleaned_data['supplier']
            datetime = pmform.cleaned_data['datetime']
            #total_amount = pmform.cleaned_data['total_amount']
            
            item = pdform.cleaned_data['item']
            quantity = pdform.cleaned_data['quantity']
            price = pdform.cleaned_data['price']
            amount = pdform.cleaned_data['amount']

            Temppurchase.objects.create(
                 supplier=supplier,invoice=invoice,
                 datetime=datetime,
                 item=item, quantity=quantity,price=price, amount=amount
            )
            
            pdform = PurchaseDetailForm()
    pdobj = Temppurchase.objects.all()
    

       
    if 'finalSubmit' in request.POST:
        if request.method == 'POST':
            # Access the default database using 'connections'
            with connections['default'].cursor() as cursor:
                InsertPurchase_sql = '''
                INSERT INTO inventry_app_purchase(invoice, datetime, supplier_id, total_amount)
                SELECT invoice, datetime, supplier_id, SUM(amount) as total_amount FROM inventry_app_temppurchase GROUP BY invoice, datetime
                '''
                cursor.execute(InsertPurchase_sql)

                purchase = Purchase.objects.latest('id')
                purchase_id = purchase.id
                InsertPurchaseDetails_sql = ''' 
                INSERT INTO inventry_app_purchasedetails(quantity, price, amount, item_id, purchase_id)
                SELECT quantity, price, amount, item_id, %s FROM inventry_app_temppurchase
                '''
                cursor.execute(InsertPurchaseDetails_sql, [purchase_id])

                clear_Temppurchase_sql = '''
                DELETE FROM inventry_app_temppurchase
                '''
                cursor.execute(clear_Temppurchase_sql)

        return redirect('temp_purchase')

    return render(request, 'dashboard/purchase.html',
                    {'pmform': pmform,
                     'pdform':pdform,
                      'pdobj': pdobj})

def get_item_price(request):
    if request.method == 'GET':
        item_id= request.GET.get('item_id')
        product =get_object_or_404(Item,id=item_id)
        # print(product.price)
        price = product.price
        
        data = {'price': price}
        return JsonResponse(data)
    
def purchase_details(request):
    all_data = Purchase.objects.prefetch_related('purchasedetails_set').all()
    return render(request, 'dashboard/purchase_details.html', {'data': all_data,})

#.....................Sale...........................


def sale_mast(request):
    smform = SaleForm()
    sdform = SaleDetailForm()
    
    if request.method == 'POST':
        smform = SaleForm(request.POST)
        sdform = SaleDetailForm(request.POST)
        if smform.is_valid() and sdform.is_valid():
            # invoice_no = smform.cleaned_data['invoice_no']
            # datetime = smform.cleaned_data['datetime']
            customer = smform.cleaned_data['customer']
            contact_no = smform.cleaned_data['contact_no']
            #total  _amount = smform.cleaned_data['total_amount']
            item = sdform.cleaned_data['item']
            quantity = sdform.cleaned_data['quantity']
            price = sdform.cleaned_data['price']
            amount = sdform.cleaned_data['amount']  

           # Calculate stock quantity
            purchase_quantity = PurchaseDetails.objects.filter(item=item).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            sale_quantity = SaleDetail.objects.filter(item=item).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            stock_quantity = purchase_quantity - sale_quantity

            if stock_quantity >= quantity:
                Temsale.objects.create(
                    customer=customer, contact_no=contact_no, item=item,
                    quantity=quantity, price=price, amount=amount
                )
                sdform = SaleDetailForm()
            else:
                 messages.error(request, "Not enough stock quantity")
    
    tsobj =Temsale.objects.all()
    if 'finalSubmit' in request.POST:
        if request.method == 'POST':
            with transaction.atomic():
                #  Sale.objects.all().delete()
                #  SaleDetail.objects.all().delete()
                 total_values = Temsale.objects.values('invoice_no','customer', 'contact_no') \
                 .annotate(total_amount=Sum(F('amount')))

        for total_amount_data in total_values:
             customer = total_amount_data['customer']
             contact_no = total_amount_data['contact_no']
             total_amount = total_amount_data['total_amount']
             invoice_no = total_amount_data['invoice_no']


             # Insert a Sale record with generated invoice and datetime
             sale = Sale.objects.create(
                 customer=customer,
                 contact_no=contact_no,
                 total_amount=total_amount,
                 invoice_no=invoice_no
             )
             sale_id = sale.id
      
        #     # Insert SaleDetail data for this customer
             sale_details = Temsale.objects.filter(
                 customer=customer,
                 contact_no=contact_no
             )
        #       # store filter customer data in saledetails
             for sale_detail in sale_details:
                 SaleDetail.objects.create(
                     quantity=sale_detail.quantity,
                     price=sale_detail.price,
                    amount=sale_detail.amount,
                    item=sale_detail.item,
                    sale_id=sale_id 
                )

        #     # Clear Temsale data for this customer

             Temsale.objects.all().delete()

             return redirect('sale_mast')

    return render(request, 'dashboard/sale.html', 
                  {'smform': smform, 'sdform': sdform, 'tsobj': tsobj})



def sale_details(request):
    all_data = Sale.objects.prefetch_related('saledetail_set').all()
    return render(request, 'dashboard/sale_details.html', {'data': all_data})


#....................reports...............
def purchase_report(request):
    if request.method == 'POST':
        form1 = PurchaseReportForm(request.POST)
        if form1.is_valid():  
            startdate = form1.cleaned_data['start_date']
            enddate = form1.cleaned_data['end_date']
            pbetween = Purchase.objects.filter(datetime__range=[startdate, enddate]).prefetch_related('purchasedetails_set').all()

            return render(request, 'dashboard/purchase_report.html', 
                          {'pbetween': pbetween})

    else:
        form1 = PurchaseReportForm() 

    return render(request, 'dashboard/purchase_report.html', {'form': form1})



def sale_report(request):
    if request.method == 'POST':
        form = SaleReportForm(request.POST)
        if form.is_valid():
            startdate = form.cleaned_data['start_date']
            enddate = form.cleaned_data['end_date']
            # sbetween =Sale.objects.prefetch_related('saledetails_set').all()
            sbetween = Sale.objects.filter(datetime__range=[startdate, enddate]).prefetch_related('saledetail_set').all()
            #print(sbetween)
            return render(request, 'dashboard/sale_report.html', {'sbetween': sbetween})
    else:
        form = SaleReportForm() 

    return render(request, 'dashboard/sale_report.html', {'form': form})



def stock_report(request):
    items = Item.objects.all()

    stock_quantities = []

    for item in items:
        purchase_quantity = 0
        sale_quantity = 0

        # Calculate total purchase quantity
        purchase_details = PurchaseDetails.objects.filter(item=item)
        for purchase_detail in purchase_details:
            purchase_quantity += purchase_detail.quantity

        # Calculate total sale quantity
        sale_details = SaleDetail.objects.filter(item=item)
        for sale_detail in sale_details:
            sale_quantity += sale_detail.quantity

        stock_quantity = purchase_quantity - sale_quantity
        # print(stock_quantity)

        stock_quantities.append({
            'item': item,
            'purchase_quantity': purchase_quantity,
            'sale_quantity': sale_quantity,
            'available_quantity': stock_quantity,
        })

    return render(request, 'dashboard/stock_report.html',{'stock_quantities':stock_quantities})
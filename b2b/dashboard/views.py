from django.shortcuts import render,redirect,get_object_or_404
from store.models import  Product,ProductAttribute,Profile
from django.contrib.auth.decorators import  login_required
from .forms import NewProductForm,ProductAttributeFormSet
# Create your views here.

@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_seller:  # Check if the user is not a seller
        print('not seller')
        return redirect('home')
    products=Product.objects.filter(created_by=request.user)

    return render(request,'index.html',{'products':products})


@login_required
def dashboard_add_product(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the main product
            new_product = form.save(commit=False)
            new_product.created_by = request.user
            new_product.save()

            # Save custom attributes
            attribute_names = request.POST.getlist('attribute_name[]')
            attribute_values = request.POST.getlist('attribute_value[]')
            for name, value in zip(attribute_names, attribute_values):
                ProductAttribute.objects.create(
                    product=new_product,
                    attribute_name=name,
                    attribute_value=value
                )
            return redirect('dashboard:index')  # Redirect to dashboard index or appropriate page
    else:
        form = NewProductForm()

    return render(request, 'dashboard_add_product.html', {'form': form})
from django.shortcuts import render,redirect,get_object_or_404
from . models import Product,Category,Profile,SubCategory,Festival,ProductAttribute,Enquiry,BestPriceRequest,City
from datetime import date
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import  User
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm,EnquiryForm
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta


def about(request):
    return render(request,'about.html')





@login_required
def delete_product(request,pk):

    product=get_object_or_404(Product,pk=pk,created_by=request.user)
    product.delete()

    return redirect('dashboard:index')



def filter_dropdown(request):

    category_filter = request.GET.get('category', None)
    location_filter = request.GET.get('location', None)


    query = Q()


    if category_filter:
        query &= Q(category__name=category_filter)


    if location_filter:
        query &= Q(created_by__profile__city__icontains=location_filter)


    products = Product.objects.filter(query)
    categories = Category.objects.all()

    return render(request, 'filter_search.html', {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
        'current_location': location_filter,
    })




def home(request):

    # Fetch all categories, subcategories, and locations
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    # all_locations = Profile.objects.values_list('city', flat=True).distinct()
    all_city=City.objects.all()
    recent_products = Product.objects.filter(created_at__gte=now() - timedelta(days=30)).order_by('-created_at')[:10]

    # Get user-selected category or search query
    category = request.GET.get('category', None)
    search_query = request.GET.get('search', None)

    # Default to all products and apply category or search filter
    if category:
        products = Product.objects.filter(category__name=category)
    elif search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()

    # Seasonal products (only show if no category or search filter is applied)
    summer_products = Product.objects.filter(season='summer')
    winter_products = Product.objects.filter(season='winter')
    rainy_products = Product.objects.filter(season='rainy')

    # Festival products
    today = date.today()
    active_festival = Festival.objects.filter(is_active=True, start_date__lte=today, end_date__gte=today).first()
    if active_festival:
        # Fetch only on-sale products for the active festival
        festival_products = Product.objects.filter(festival=active_festival, on_sale=True)
    else:
        festival_products = []

    # On-sale products (globally)
    on_sale_products = Product.objects.filter(on_sale=True)

    # Pass all necessary context to the template
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
       
        'all_cities':all_city,
        'festival_products': festival_products,  # Pass festival_products to the template
        'recent_products': recent_products,
    }
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        context['current_user'] = current_user

    # Include seasonal products in the context if no filter is applied
    if not category and not search_query:
        context['summer_products'] = summer_products
        context['winter_products'] = winter_products
        context['rainy_products'] = rainy_products

    # Add festival products to the context if a festival is active
    if active_festival:
        context['festival'] = active_festival
        context['festival_products'] = festival_products

    # Add the carousel locations
    context['all_cities'] = all_city
    

    return render(request, 'home.html', context)




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been Logged In')

            # Check user role to determine redirection
            profile = Profile.objects.get(user=user)
            if profile.is_admin:  # Redirect admin to the seller_req page
                return redirect('seller_req')
            elif profile.is_seller:  # Redirect seller to the dashboard
                return redirect('dashboard:index')
            else:  # Redirect non-admin/non-seller users to the home page
                return redirect('home')
        else:
            messages.error(request, 'There was an error, please try again')
            return redirect('login')
    else: 
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out ....."))
    return redirect('home')

def product(request, pk):
    # Get the product based on primary key (pk)
    product = get_object_or_404(Product, id=pk)

    # Check if the user is authenticated and fetch the current user profile
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        is_owner = request.user == product.created_by
    else:
        current_user = None
        is_owner = False

    # Fetch products by the same seller, excluding the current product
    same_seller_products = Product.objects.filter(
        created_by=product.created_by
    ).exclude(id=product.id)

    # Fetch products in the same category from all sellers, excluding the current product
    same_category_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)

    # Render the template with all the necessary context
    return render(request, 'product.html', {
        'product': product,
        'current_user': current_user,
        'is_owner': is_owner,
        'same_seller_products': same_seller_products,
        'same_category_products': same_category_products,
    })
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm

def register_user(request):
    """
    Handles user registration with password matching validation.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Get the cleaned data for password and confirm password
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            # Check if the password and confirm password match
            if password1 != password2:
                messages.error(request, "Password and Confirm Password do not match.")
                return render(request, 'register.html', {'form': form})

            # Save the user instance
            user = form.save()

            # Automatically log in the user after successful registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have registered successfully!")
                return redirect('home')
            else:
                messages.error(request, "Authentication failed. Please try logging in manually.")
                return redirect('login')

        else:
            # Display error messages from form validation
            messages.error(request, "There was a problem with your registration. Please check the form for errors.")
            return render(request, 'register.html', {'form': form})

    else:
        # Render the registration form for a GET request
        form = SignUpForm()
        return render(request, 'register.html', {'form': form}) 





def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user
        # Did they fill out the form
        if request.method=='POST':
            form=ChangePasswordForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,('Your Password has been updated, Please Login Again'))
                # login(request,current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form=ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request, ('You have to LogIn first!!'))
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request,('User has been updated!!'))
            return redirect('home')
        else:
            return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request, ('You have to LogIn first!!'))
        return redirect('home')







from django.db.models import Q
from .models import Product, Category, SubCategory, Profile

def subcategory_view(request, subcategory_id):
    location_filter = request.GET.get('location', '').strip()  # Get location from GET if available
    query = Q(subcategory_id=subcategory_id)  # Filter by subcategory

    # Apply location filter if provided
    if location_filter:
        query &= Q(created_by__profile__city__name__icontains=location_filter)  # Fixed lookup

    products = Product.objects.filter(query)

    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category_id__in=[cat.id for cat in categories])
    # all_locations = Profile.objects.values_list('city__name', flat=True).distinct()  # Get city names
    all_city=City.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        
        'all_cities':all_city,
        'current_location': location_filter,
    }

    return render(request, 'home.html', context)


def catfilter(request, category_id):
    # Get filter parameters from GET request
    location_filter = request.GET.get('location', '').strip()
    query = Q(category_id=category_id)

    # Apply location filter if provided
    if location_filter:
        query &= Q(created_by__profile__city__name__icontains=location_filter)  # Fixed lookup

    # Get products based on the filter
    products = Product.objects.filter(query)

    # Get categories, subcategories, and locations for the sidebar
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category_id=category_id)
    # all_locations = Profile.objects.values_list('city__name', flat=True).distinct()  # Get city names
    all_city=City.objects.all()

    # Get attributes for the selected category
    category_name = Category.objects.get(id=category_id).name
    attributes = ProductAttribute.objects.filter(product__category__name=category_name).values('attribute_name').distinct()

    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'all_cities':all_city,
        'current_location': location_filter,
        'attributes': attributes,
    }

    return render(request, 'home.html', context)


from django.db.models import Q
from django.shortcuts import render
from .models import Product, Category, City, Profile


def search(request):
    categories = Category.objects.all()
    all_cities = City.objects.all()

    # Get data from the request
    searched = request.POST.get('searched', '').strip() if request.method == 'POST' else request.GET.get('searched', '').strip()
    location = request.POST.get('location', '').strip() if request.method == 'POST' else request.GET.get('location', '').strip()
    min_price = request.GET.get('min', '')
    max_price = request.GET.get('max', '')
    sort_by = request.GET.get('sort_by', '0')  # Default to Low to High

    # Default products queryset
    query = Q()
    
    # Filter products by search term
    if searched:
        query &= Q(name__icontains=searched) | Q(description__icontains=searched) | Q(keywords__icontains=searched)
    
    # Filter by location
    if location:
        query &= Q(created_by__profile__city__name__icontains=location)
    
    # Filter by price range
    if min_price:
        try:
            min_price = float(min_price)
            query &= Q(price__gte=min_price)
        except ValueError:
            min_price = 0
    if max_price:
        try:
            max_price = float(max_price)
            query &= Q(price__lte=max_price)
        except ValueError:
            max_price = 1000000

    # Apply filters to products queryset
    products = Product.objects.filter(query)

    # Sort products
    if sort_by == '1':
        products = products.order_by('-price')  # High to Low
    else:
        products = products.order_by('price')  # Low to High

    # Context for rendering
    context = {
        'products': products,
        'categories': categories,
        'all_cities': all_cities,
        'searched': searched,
        'current_location': location,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'filter_search.html', context)

from django.db import transaction

def seller_req(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_admin:  # Check if the user is not an admin
        print('not admin')
        return redirect('home')

    if request.method == "POST":
        # Handle the update of seller_req
        profile_id = request.POST.get('profile_id')
        seller_req = request.POST.get('seller_req')

        profile = get_object_or_404(Profile, id=profile_id)

        with transaction.atomic():  # Ensure atomicity for database operations
            profile.seller_req = seller_req

            if profile.seller_req == 'accept':
                profile.is_seller = True
                profile.save()
                # Send email notification
                send_mail(
                    'Seller Request Approved',
                    f'Congratulations {profile.user.username}, your request to become a seller has been approved!',
                    settings.EMAIL_HOST_USER,
                    [profile.user.email],
                    fail_silently=False,
                )
            elif profile.seller_req == 'reject':
                user = profile.user
                # Send email notification before deleting the user
                send_mail(
                    'Seller Request Rejected',
                    f'Sorry {profile.user.username}, your request to become a seller has been rejected.',
                    settings.EMAIL_HOST_USER,
                    [profile.user.email],
                    fail_silently=False,
                )
                # Optionally, delete related objects or handle orphaned references
                user.delete()  # Delete the user, cascades to profile and other related objects
            else:
                profile.is_seller = False
                profile.save()

        return redirect('seller_req')  # Redirect back to the same page after updating

    # Display the profile table for pending requests
    profiles = Profile.objects.filter(want_to_prime=True).order_by(
        '-seller_req')  # Sort by seller_req to show pending first
    return render(request, 'seller_req.html', {'profiles': profiles})


from django.contrib import messages

def cityfilter(request, city_id):
    try:
        # Get the city object using the provided city_id
        city = City.objects.get(id=city_id)

        # Get all users who have the specified city in their profile
        users_in_city = Profile.objects.filter(city=city).values_list('user', flat=True)

        # Get products created by users from this city
        products = Product.objects.filter(created_by__in=users_in_city)

        # Group products by category
        categories = Category.objects.all()  # Fetch all categories
        products_by_category = {}
        subcategories = SubCategory.objects.all()  # Fetch all subcategories
        products_by_subcategory = {}

        for category in categories:
            # Filter products by category
            products_by_category[category] = products.filter(category=category)

        for subcategory in subcategories:
            # Filter products by subcategory
            products_by_subcategory[subcategory] = products.filter(subcategory=subcategory)

        return render(request, 'location_product.html', {
            'city': city,  # Pass the city object for display purposes
            'products_by_category': products_by_category,
            'categories': categories,
            'products_by_subcategory': products_by_subcategory,  # Pass the subcategory products
        })

    except City.DoesNotExist:
        # Add an error message to the request using Django messages
        messages.error(request, 'City not found.')

        # Redirect to a relevant page (e.g., a product listing page or homepage)
        return redirect('home')  # Replace 'product_list' with the actual name of your view


 
from django.contrib import messages

def product_filter(request, location, category_id, subcategory_id=None):
    try:
        # Get the city object using the location (city_id)
        city = City.objects.get(id=location)  # location is passed as city_id
        
        # Get the selected category by id
        category = Category.objects.get(id=category_id)
        
        # Get products filtered by the city and category
        products = Product.objects.filter(created_by__profile__city=city, category=category)

        # If subcategory_id is provided, filter products by subcategory
        if subcategory_id:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            products = products.filter(subcategory=subcategory)

        # Fetch all categories and subcategories to display in the filter menu
        categories = Category.objects.all()
        subcategories = SubCategory.objects.filter(category=category)

        return render(request, 'city_filter_product.html', {
            'city': city,
            'category': category,
            'subcategory_id': subcategory_id,
            'products': products,
            'categories': categories,
            'subcategories': subcategories,
        })
    
    except City.DoesNotExist:
        messages.error(request, 'City not found.')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found.')
    except SubCategory.DoesNotExist:
        messages.error(request, 'Subcategory not found.')

    # Fetch categories and subcategories for the filter menu even if there's an error
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category_id=category_id) if Category.objects.filter(id=category_id).exists() else []

    return render(request, 'city_filter_product.html', {
        'categories': categories,
        'subcategories': subcategories,
    })





def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            # Prepare email content
            subject = "Seller Request Submitted"
            message = f"""
            User {request.user.username} has requested seller status:
            
            Name: {current_user.user}
            Address: {current_user.address1}, {current_user.address2}, {current_user.city}, {current_user.state}, {current_user.country} - {current_user.zipcode}
            Phone: {current_user.phone}
            GST Number: {current_user.GST_number}
            Work Days: {current_user.work_days}
            Business Type: {', '.join(bt.name for bt in current_user.business_type.all())}
            Establishment: {current_user.establishment}
            Employee Count: {current_user.employee_count}
            Company Details: {current_user.company_details}
            """
            from_mail = settings.EMAIL_HOST_USER
            recipient_list = ["monismomin123@gmail.com"]

            try:
                send_mail(subject, message, from_mail, recipient_list)
                messages.success(request, "Your info has been updated and a request has been sent to the admin.")
                form.save()
                current_user.want_to_prime=True
                current_user.save()

                
            except Exception as e:
                messages.error(request, f"Info updated but email failed to send: {e}")
            
            return redirect('home')
        else:
            return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, "You have to LogIn first!")
        return redirect('home')


def send_enquiry(request):
    product = None
    product_id = request.GET.get('product_id') or request.POST.get('product_id')  # Get product_id from both GET and POST

    print("Product ID from GET/POST:", product_id)  # Debugging line to check both GET and POST values

    if product_id:
        try:
            product = get_object_or_404(Product, id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('home')  # Redirect to the home page if product not found
    else:
        messages.error(request, "Product ID is missing.")
        return redirect('home')  # Redirect to home or show an error

    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()  # Save the enquiry

            if product:
                seller_profile = get_object_or_404(Profile, user=product.created_by)
                recipient_email = seller_profile.user.email

                subject = f"New Enquiry for {product.name}"
                message = f"""
                You have received a new enquiry:
                
                Name: {enquiry.name}
                Email: {enquiry.email}
                Phone: {enquiry.phone}
                Message: {enquiry.message}
                """
                from_email = 'kp7734855@gmail.com'
                recipient_list = [recipient_email]

                try:
                    send_mail(subject, message, from_email, recipient_list)
                    messages.success(request, "Your enquiry has been sent successfully!")
                except Exception as e:
                    messages.error(request, f"Failed to send email: {str(e)}")

            return redirect('send_enquiry')
        else:
            messages.error(request, "There was an error sending your enquiry. Please try again.")
    else:
        form = EnquiryForm()

    return render(request, 'Enquiry.html', {'form': form, 'product': product})



from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .forms import EmailForm, OTPForm, NewPasswordForm
from .models import PasswordResetOTP

User = get_user_model()

def forgot_password_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp = PasswordResetOTP.generate_otp()
                PasswordResetOTP.objects.create(user=user, otp=otp)

                # Send OTP email
                send_mail(
                    subject="Your OTP for Password Reset",
                    message=f"Your OTP is {otp}. It is valid for 10 minutes.",
                    from_email="your_email@example.com",
                    recipient_list=[email],
                )
                request.session['reset_user_id'] = user.id
                return redirect('verify_otp')
            else:
                form.add_error('email', "Email does not exist.")
    else:
        form = EmailForm()
    return render(request, 'forgot_password.html', {'form': form})


def verify_otp_view(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user_id = request.session.get('reset_user_id')
            otp_record = PasswordResetOTP.objects.filter(user_id=user_id, otp=otp, is_verified=False).first()

            if otp_record and not otp_record.is_expired():
                otp_record.is_verified = True
                otp_record.save()
                return redirect('reset_password')
            else:
                form.add_error('otp', "Invalid or expired OTP.")
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from .forms import NewPasswordForm

def reset_password_view(request):
    user_id = request.session.get('reset_user_id')  # Retrieve user_id from session
    if not user_id:
        messages.error(request, "Session expired or invalid request.")
        return redirect('forgot_password')

    user = get_object_or_404(User, id=user_id)  # Ensure user exists

    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']

            # Update the user's password
            user.set_password(password1)
            user.save()

            # Clear the session data
            del request.session['reset_user_id']

            # Send a success email
            try:
                send_mail(
                    subject="Password Successfully Changed",
                    message="Your password has been successfully updated.",
                    from_email="your_email@example.com",
                    recipient_list=[user.email],
                )
            except Exception as e:
                # Log the exception (you can replace with actual logging)
                print(f"Error sending email: {e}")

            messages.success(request, "Your password has been successfully updated. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewPasswordForm()

    return render(request, 'reset_password.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Profile, BestPriceRequest  # Adjust imports as needed
from .forms import BestPriceForm  # Assuming you have a form for the best price request

def best_price(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to submit a best price request.")
        return redirect('login')  # Redirect to login page if not authenticated

    products = Product.objects.all()  # Get all products to display in the form

    if request.method == 'POST':
        form = BestPriceForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            product_id = request.POST.get('product_id')

            # Fetch the selected product
            product = get_object_or_404(Product, id=product_id)

            # Save the request in the database
            BestPriceRequest.objects.create(
                product=product,
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            # Fetch all sellers associated with the product's category
            sellers = Profile.objects.filter(
                is_seller=True,  # Only sellers
                user__products__category=product.category  # Match product's category
            ).values_list('user__email', flat=True).distinct()

            if sellers:
                # Send email to sellers in the matching category
                subject = f"Best Price Request for {product.name}"
                email_message = f"""
                A new best price request has been made for your product "{product.name}".
                
                User Details:
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Message: {message or "No additional message provided."}
                """
                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, list(sellers))

                # Add success message
                messages.success(request, f"Your request for the best price of '{product.name}' has been sent to sellers in the same category!")
            else:
                # Log error if no sellers are found in the category
                messages.error(request, f"No sellers found for the category of '{product.name}'.")

            return redirect('home')
        else:
            messages.error(request, "There was an error with your submission. Please check the form and try again.")
    else:
        form = BestPriceForm()  # Empty form for GET requests

    return render(request, 'best_price.html', {'products': products, 'form': form})



from django.shortcuts import render
from .models import Category
#view_all category for sidebar
def view_categories(request):
    # Fetch all categories with their subcategories
    categories = Category.objects.all()
    return render(request, 'view_category.html', {'categories': categories})


#filter sorting
from django.shortcuts import render
from .models import Product

def sort(request, sv):
    # Get the location from the request (either from GET or a hidden input)
    location = request.GET.get('location', '')  # Location from the query string
    searched = request.GET.get('searched', '')  # Search term from the query string

    # Apply location filter if a location is provided
    products = Product.objects.all()

    # Search functionality if search term is provided
    if searched:
        products = products.filter(name__icontains=searched)

    # Apply location filter if a location is provided
    if location:
        products = products.filter(created_by__profile__city__name=location)

    # Determine the sorting order (ascending or descending)
    if sv == '1':
        # Sorting in descending order by price
        products = products.order_by('-price')
    else:
        # Sorting in ascending order by price
        products = products.order_by('price')

    context = {
        'products': products,
        'searched': searched,
        'current_location': location
    }
    return render(request, 'filter_search.html', context)




from django.shortcuts import render
from django.db.models import Q
from .models import Product

def filterbyprice(request):
    # Get the location, min, and max values from the GET request
    location = request.GET.get('location', '')  # Location from dropdown
    searched = request.GET.get('searched', '')  # Search term from query string
    min_price = request.GET.get('min', '')
    max_price = request.GET.get('max', '')

    # Default values in case fields are empty or invalid
    if min_price == '':
        min_price = 0  # Default to 0 if empty
    else:
        try:
            min_price = float(min_price)  # Convert to float if not empty
        except ValueError:
            min_price = 0  # Default to 0 if conversion fails

    if max_price == '':
        max_price = 1000000  # A high value for max (you can adjust this based on your max product price)
    else:
        try:
            max_price = float(max_price)  # Convert to float if not empty
        except ValueError:
            max_price = 1000000  # Default to a high value if conversion fails

    # Create the query for products within the price range
    query = Q(price__gte=min_price, price__lte=max_price)
    
    # Apply location filter if a location is selected
    if location:
        query &= Q(created_by__profile__city__name=location)  # Correct the filter for city

    # Apply search filter if search term is provided
    if searched:
        query &= Q(name__icontains=searched)  # Filter by the search term

    # Get the filtered products
    products = Product.objects.filter(query)

    context = {
        'products': products,
        'current_location': location,
        'searched': searched
    }

    return render(request, 'filter_search.html', context)

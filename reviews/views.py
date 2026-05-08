from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reviews.models import Review
from users.models import User
from apartments.models import Apartment


@login_required
def add_review(request):
    if request.method == 'POST':
        reviewed_user_id = request.POST.get('reviewed_user_id')
        reviewed_apartment_id = request.POST.get('reviewed_apartment_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            if reviewed_user_id:
                reviewed_user = get_object_or_404(User, id=reviewed_user_id)

                if reviewed_user == request.user:
                    messages.error(request, "You cannot review yourself.")
                else:
                    Review.objects.update_or_create(
                        reviewer=request.user,
                        reviewed_user=reviewed_user,
                        defaults={
                            'rating': int(rating),
                            'comment': comment
                        }
                    )
                    messages.success(request,
                                     f"Review for {reviewed_user.get_full_name() or reviewed_user.username} submitted successfully!")

            elif reviewed_apartment_id:
                reviewed_apartment = get_object_or_404(Apartment, id=reviewed_apartment_id)
                Review.objects.update_or_create(
                    reviewer=request.user,
                    reviewed_apartment=reviewed_apartment,
                    defaults={
                        'rating': int(rating),
                        'comment': comment
                    }
                )
                messages.success(request, f"Review for {reviewed_apartment.name} submitted successfully!")

            else:
                messages.error(request, "Invalid review target.")
        else:
            messages.error(request, "Please provide rating and comment.")

        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    return redirect('dashboard')

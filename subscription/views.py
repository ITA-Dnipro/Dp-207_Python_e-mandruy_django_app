from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from subscription.utils.utils_for_subscription import create_subsciptions, ServiceHandler
from django.contrib import messages
from subscription.models import NotUniqueSubscription
from subscription.utils.utils_for_forms import ControllerForm


def add(request):
    if request.method == 'POST':
        subsciptions = create_subsciptions(post_dict=request.POST, user=request.user)
        for subsciption in subsciptions:
            if isinstance(subsciption, NotUniqueSubscription):
                messages.error(request, subsciption)
            else:
                messages.success(request, f"{subsciption} was created")
        return HttpResponseRedirect(reverse('user_profile:user_profile'))
    return render(request, 'subscription/add_subscription.html')


def delete(request, pk):
    ServiceHandler().delete_subscription_by_id(pk)
    return redirect('user_profile:user_profile')


def update(request, pk):
    subscription = ServiceHandler().get_by_id(pk)
    form = ControllerForm(subscription).get_proper_form()(instance=subscription)
    if request.method == 'POST':
        bound_form = ControllerForm(subscription).get_proper_form()(request.POST, instance=subscription)
        if bound_form.is_valid():
            update_subscription = bound_form.save(commit=False)
            update_subscription.update(pk)
            return redirect('user_profile:user_profile')
        return render(request, 'subscription/update_subscription.html', {"form": bound_form, "subscription": subscription})
    return render(request, 'subscription/update_subscription.html', {"form": form, "subscription": subscription})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render

from .forms import CommentForm
from .models import Comment


@login_required
def comment_delete(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if obj.author != request.user:
        response = HttpResponse(
            "You do not have permission to do this. You may only delete your own comments.")
        response.status_code = 403
        return response

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Your comment has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {}
    context['comment'] = obj
    return render(request, "comments/confirm_delete.html", context)

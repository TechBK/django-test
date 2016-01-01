from django.views import generic
from django.http import JsonResponse
from .models import Comment


class IndexView(generic.TemplateView):
    template_name = 'react/index.html'


def handle_comments(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        if not comments:
            return JsonResponse([], safe=False)
        else:
            data = [{"id": cm.id, "author": cm.author, "text": cm.text} for cm in comments]
            return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        new_comment = Comment(author=request.POST['author'], text=request.POST['text'])
        try:
            new_comment.save()
        finally:
            comments = Comment.objects.all()
            data = [{"id": cm.id, "author": cm.author, "text": cm.text} for cm in comments]
            return JsonResponse(data, safe=False)

            # data = [
            #     {"author": "Pete Hunt", "text": "This is one \n comment"},
            #     {"author": "Jordan Walke", "text": "This is *another* comment"},
            #     {"author": "TechBK", "text": "TechBk comment"},
            #     {"author": "TechBK", "text": "GOGO QTV my idol"},
            #     {"author": "TechBK", "text": "GOGO QTV \n my idol"},
            #
            # ]
            # return JsonResponse(data,safe=False)

class ThinkingView(generic.TemplateView):
    template_name = 'react/thinking.html'


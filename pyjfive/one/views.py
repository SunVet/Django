from django.shortcuts import render

from django.views import View

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
import markdown

from comments.forms import CommentForm

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.views.generic import ListView

# Create your views here.

# 主页
# def index(request):
	# 无分页功能
	# post_list = Post.objects.all().order_by('-created_time')
	# return render(request,'index.html',context={
	# 	'post_list':post_list
	# })

# 	可分页
# 	post_list = Post.objects.all().order_by('-created_time')
# 	paginator = Paginator(post_list,3)
# 	page = request.GET.get('page')
#
# 	try:
# 		post_list = paginator.page(page)
# 	except PageNotAnInteger:
# 		post_list = paginator.page(1)
# 	except EmptyPage:
# 		post_list = paginator.page(paginator.num_pages)
#
# 	return render(request,'index.html',context={
# 		'post_list':post_list})

class IndexView(ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'post_list'
	paginate_by = 3

# 详情页
def detail(request,pk):
	post = get_object_or_404(Post,pk=pk)

	# 阅读量+1
	post.increase_views()

	post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc'],)

	form = CommentForm()
	comment_list = post.comment_set.all()

	context = {'post':post,'form':form,'comment_list':comment_list}
	return render(request,'detail.html',context=context)

# 作者页
def about(request):

	return render(request,'about.html')

# 联系我们
def contact(request):
	return render(request,'contact.html')


# 归档
def archives(request,year,month):
	post_list = Post.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
	return render(request,'index.html',context={'post_list':post_list})


# 分类
# def category(request,pk):
# 	cate = get_object_or_404(Category,pk=pk)
# 	post_list = Post.objects.filter(category=cate).order_by('-created_time')
# 	return render(request,'index.html',context={'post_list':post_list})

class CategoryView(IndexView):

	def get_queryset(self):
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)

# 标签
class TagView(ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
		return super(TagView,self).get_queryset().filter(tags=tag)



# 搜索功能
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'index.html', {'error_msg': error_msg,
                                               'post_list': post_list})

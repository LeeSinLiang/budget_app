from django.shortcuts import render,redirect
from .models import Category,Expense,Project
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.utils.text import slugify
from django.urls import reverse
from .forms import ExpenseForm
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import json
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
# Create your views here.
@login_required
def project_list(request):

    project_list = Project.objects.all()
    projects_lists = []
    for projects in project_list:
        if request.user == projects.user:
            projects_lists.append(projects)


    return render(request, 'budget/project-list.html',{'project_list':projects_lists})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'GET':
        if request.user == project.user:
            expense_list = project.expenses.all()
            # success = []
            # seen = set()
            # uniq = []
            # successss = []
            # for expense in expense_list:
            #     success.append(expense.category)
            #     for x in success:
            #         if x not in seen:
            #             uniq.append(x)
            #             seen.add(x)
            #             successss.append(expense.test)
            seen = []
            seen1 = []
            expense = False
            for expense in expense_list:
                seen = expense.seen()
                break
            for expense in expense_list:
                seen1.append(expense.test())
            # print(seen)
            names = zip(seen,seen1)
            category_list = Category.objects.filter(project=project)
            return render(request, 'budget/project-detail.html',{
            'project' : project,
            'expense_list' : project.expenses.all(),
            'names' : names,
            # 'successss' : successss,
            'category_list' : category_list
        })
        else:
            raise Http404
        
    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            print(amount)
            category = get_object_or_404(Category, project=project, name=category_name)
            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()
        else:
            raise Http404
        
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(reverse('budget:detail' , kwargs={'slug':slug}))
    

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ['name','budget']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project=Project.objects.get(id=self.object.id),
                name=category
            ).save()
        
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        slug = slugify(self.request.POST['name'])
        return reverse('budget:detail' , kwargs={'slug':slug})

def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # if request.method == 'DELETE':
    project.delete()
    return redirect('budget:list')
    
    # context = {'project' : project}

    # return render(request,'budget/delete-project.html', context)
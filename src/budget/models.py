from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
# Create your models here.
    
class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.DecimalField(max_digits=10,decimal_places=2)

    def get_absolute_url(self):
        return reverse('budget:detail' , kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount

        return self.budget - total_expense_amount

    def total_transaction(self):
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list)

    
    
    def __str__(self):
        return self.name

    


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    # def same_category(self):
    #     not_same_category = []
    #     for row in Expense.objects.all():
    #         if Expense.objects.filter(project=self.project, category=self.category).count() > 1:
    #             pass
    #         else:
    #             not_same_category.append(row)
    #     return not_same_category.order_by('category')

    def seen(self):
        expense_list = Expense.objects.filter(project=self.project)
        success = []
        seen = set()
        uniq = []
        for expense in expense_list:
            success.append(expense.category)
            for x in success:
                if x not in seen:
                    uniq.append(x)
                    seen.add(x)
        return seen

    def test(self):
        expenses_list = Expense.objects.filter(project=self.project,category=self.category)
        
        total_expenses_amount = 0
        for expenses in expenses_list:
            total_expenses_amount += expenses.amount
        return total_expenses_amount

    def __str__(self):
        return self.title

    
        
    class Meta:
        ordering = ['-amount']



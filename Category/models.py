from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from Product.models import ProductPage


class ProductCategory(Page):
    cate_title = models.CharField(max_length=255,blank=True,null=True)
    content_panels = Page.content_panels + [
        FieldPanel("cate_title"),
       
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['Product.ProductPage']
    def get_context(self, request):
        context = super().get_context(request)
        context['products'] = ProductPage.objects.child_of(self).live()  
        return context

    def __str__(self):
        return self.title
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from wagtail import blocks

class HomePage(Page):
    content = StreamField([
        ('welcome_message', blocks.RichTextBlock(help_text="Enter a welcome message or introduction text.")),
    ], use_json_field=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    template = "home/home.html"  

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

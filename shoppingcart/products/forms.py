import itertools

from django import forms
from django.utils.text import slugify

from .models import Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'title',
            'content',
        )

    def save(self):
        instance = super(ProductsForm, self).save(commit=False)

        max_length = Products._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.title)[:max_length]

        for x in itertools.count(1):
            if not Products.objects.filter(slug=instance.slug).exists():
                break

            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        instance.save()

        return instance
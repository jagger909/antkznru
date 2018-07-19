from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name="Порядковый номер")
    image = models.ImageField(upload_to="categories/list", verbose_name="Изображение")

    def save(self, *args, **kwargs):
        try:
            this_record = Category.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Category, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "категория"
        verbose_name_plural = "категории"

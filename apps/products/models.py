from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Seller(models.Model):
    name = models.CharField(
        verbose_name='название организации',
        max_length=255
        )
    rate: float = models.FloatField(
        verbose_name='рейтинг',
        max_length=5,
        default=0
    )
    latitude = models.FloatField(
        verbose_name= 'широта',
    )
    longitude = models.FloatField(
        verbose_name= 'долгота',
    )
    poster: str = models.ImageField(
        verbose_name='постер',
        upload_to='posters',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='описание к продавцу',
        max_length=200,
        null=True,
        blank=True
    )

    
    class Meta:
        ordering = ('-id',)
        verbose_name = 'организация'
        verbose_name_plural = 'организации'
        
        

    def __str__(self) -> str:
        return f'{self.name}'



class Product(models.Model):
    name = models.CharField(
        verbose_name= 'название товара',
        max_length=255)
    price = models.DecimalField(
        verbose_name= 'цена',
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0, message='Цена не может быть ниже нуля')
        ]
        )
    seller = models.ForeignKey(
        verbose_name= 'продавец',
        to=Seller, 
        on_delete=models.CASCADE)
    
    poster: str = models.ImageField(
        verbose_name='постер',
        upload_to='posters',
        null=True,
        blank=True
    )
    rate: float = models.FloatField(
        verbose_name='рейтинг',
        max_length=5,
        default=0
    )
    description = models.TextField(
        verbose_name='описание к товару',
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        return f'{self.name} | {self.price:.2f}$'



class ProductComment(models.Model):
    user = models.ForeignKey(
        verbose_name='пользователь',
        to=User, 
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        verbose_name='комментарии к продукту',
        to=Product, 
        on_delete=models.CASCADE, 
        related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'комментарии к продукту'
        verbose_name_plural = 'комментарии к продуктам'

    def __str__(self) -> str:
        return f'{self.user} | {self.product}'


class ProductRating(models.Model):
    user = models.ForeignKey(
        verbose_name='пользователь',
        to=User, 
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        verbose_name='рейтинг к продукту',
        to=Product, 
        on_delete=models.CASCADE, 
        related_name='ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'рейтинг к продукту'
        verbose_name_plural = 'рейтинг к продуктам'

    def __str__(self) -> str:
        return f'{self.user} | {self.product} | {self.rating}'


class SellerComment(models.Model):
    user = models.ForeignKey(
        verbose_name='пользователь',
        to=User, 
        on_delete=models.CASCADE)
    seller = models.ForeignKey(
        verbose_name='комментарии к продавцу',
        to=Seller, 
        on_delete=models.CASCADE, 
        related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'комментарии к продавцу'
        verbose_name_plural = 'комментарии к продавцам'

    def __str__(self) -> str:
        return f'{self.user} | {self.seller}'


class SellerRating(models.Model):
    user = models.ForeignKey(
        verbose_name='пользователь',
        to=User, 
        on_delete=models.CASCADE)
    seller = models.ForeignKey(
        verbose_name='рейтинг к продавцу',
        to=Seller, 
        on_delete=models.CASCADE, 
        related_name='ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'рейтинг к продавцу'
        verbose_name_plural = 'рейтинг к продавцам'

    def __str__(self) -> str:
        return f'{self.user} | {self.seller} | {self.rating}'

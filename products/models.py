from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
import stripe

class Category(models.Model):
    name = models.CharField(max_length=30 ,null=False, blank=False, unique=True)

    def __str__(self):
        return f'{self.name}'



class Product(models.Model):
    product_name = models.CharField(max_length=60 ,null=False, blank=False)
    age = models.CharField(max_length=30 ,null=True, blank=True)
    type = models.CharField(max_length=50 ,null=True, blank=True)
    abv = models.FloatField(null=False, blank=False) 
    price = models.FloatField(null=True, blank=True) 
    picture = models.ImageField(null=True, 
                                      validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], blank=True)     
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    date_posted = models.DateTimeField(auto_now=True)
    product_stripe_id = models.CharField(max_length=100, null=True, blank=True)
    product_price_id   = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.product_name}'


# run after every product save method call
def post_save_product(sender, instance, created, *args, **kwargs):

    product = Product.objects.get(pk=instance.pk)
    product_price = int(product.price*100)
    
    # When new product is created, object of product and price is created.
    if product.product_stripe_id is None or product.product_stripe_id == '':
        print("if")
        new_product_stripe_id = stripe.Product.create(name=product.product_name, images=[product.picture, ])

        new_product_price_id = stripe.Price.create(
                                unit_amount=product_price,
                                currency="usd",
                                recurring={"interval": "month"},
                                product=new_product_stripe_id.id,
                            )

        product.product_stripe_id = new_product_stripe_id.id
        product.product_price_id = new_product_price_id.id
        product.save()

    # if the product is already created, else block run
    else:
        get_price_object = stripe.Price.retrieve(product.product_price_id) 
        amount           = get_price_object.unit_amount
        print("else")
        # when price is changed, new object of price is created
        if product_price != amount:
            print("else / if")
            new_product_price_id = stripe.Price.create(
                                unit_amount=product_price,
                                currency="usd",
                                recurring={"interval": "month"},
                                product=product.product_stripe_id,
                            )
            
            product.product_price_id = new_product_price_id.id
            product.save()
            

post_save.connect(post_save_product, sender=Product)
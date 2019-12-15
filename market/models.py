from django.db import models
from django.contrib.auth.models import User

class UserType (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='type')
    type = models.CharField(max_length=20)

class UserInfo (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    student_id = models.CharField(max_length=20)
    pw = models.CharField(max_length=50)

class Product(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    view = models.IntegerField(default=0)

    name = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=20)      # 경매인지 그냥인지
    price = models.IntegerField(default=0)      # 가격
    seller_name = models.CharField(max_length=20, blank=True) # 판매자 이름
    phone = models.CharField(max_length=20, blank=True) # 판매자 전화번호
    place = models.CharField(max_length=60, blank=True)    # 거래장소
    seller = models.ForeignKey(User, on_delete=models.CASCADE) #판매자 정보
    status = models.CharField(max_length=20)    # 판매중인지 종료인지
    photo = models.ImageField(blank=True)

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 위시리스트 해놓은 사람 정보
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 위시리스트 한 상품


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 거래 한 사람 정보
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 거래 한 상품
    price = models.IntegerField(default=0)  # 거래 한 가격 또는 auction bid
    status = models.CharField(max_length=20)  # 거래가 성공해서 샀는지, 진행중인지 실패했는지 등

from django.db import models
from django.contrib.auth.models import User

class حساب(models.Model):

    المالك = models.OneToOneField(User,on_delete=models.CASCADE)
    الرصيد = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'حساب ' + str(self.المالك)
    class Meta:
        
        verbose_name_plural = 'حساب'

class فرع (models.Model):
    الاسم = models.CharField(max_length=50)
    الرصيد = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.الاسم
    class Meta:
        
        verbose_name_plural = 'فروع'

class موظف (models.Model):
    المستخدم = models.OneToOneField(User,on_delete=models.CASCADE)
    الفرع = models.ForeignKey(فرع,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.المستخدم)

    class Meta:
        
        verbose_name_plural = 'موظفين'


class شحن(models.Model):
    الفرع = models.ForeignKey(فرع,on_delete=models.CASCADE)
    لصالح = models.ForeignKey(User,on_delete=models.CASCADE)
    المبلغ = models.PositiveIntegerField(default=0)


    def __str__(self):
        return 'شحن ' + str(self.لصالح) + ' ' + str(self.المبلغ) + ' جنيه'

    class Meta:
        verbose_name_plural = 'شحن'

    def save(self, *args, **kwargs):
        self.لصالح.حساب.الرصيد+=self.المبلغ
        self.لصالح.حساب.save()
        self.الفرع.الرصيد+=self.المبلغ
        self.الفرع.save()
        super(شحن, self).save(*args, **kwargs)

class سحب(models.Model):
    الفرع = models.ForeignKey(فرع,on_delete=models.CASCADE)
    لصالح = models.ForeignKey(User,on_delete=models.CASCADE)
    المبلغ = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'سحب'

    def save(self, *args, **kwargs):
        self.لصالح.حساب.الرصيد-=self.المبلغ
        self.الفرع.الرصيد-=self.المبلغ
        self.لصالح.حساب.save()
        self.الفرع.save()
        super(سحب, self).save(*args, **kwargs)
    def __str__(self):
        return 'سحب ' + str(self.لصالح) + ' ' + str(self.المبلغ) + ' جنيه'

class تحويل(models.Model):
    من = models.ForeignKey(User,on_delete=models.CASCADE, related_name='تحويل_خارج')
    إلى = models.ForeignKey(User,on_delete=models.CASCADE, related_name='تحويل_داخل')
    المبلغ = models.IntegerField(default=0)
    def __str__(self):
        return 'تحويل ' + str(self.من) + ' الى ' + str(self.إلى) + ' '+ str(self.المبلغ) + ' جنيه'

    class Meta:
        verbose_name_plural = 'تحويل'
    # from django.core.exceptions import ValidationError

    def save(self, *args, **kwargs):
        self.من.حساب.الرصيد-=self.المبلغ+5
        self.من.حساب.save()
        u=حساب.objects.get(المالك__username='كلمات')
        u.الرصيد+=5
        u.save()
        self.إلى.حساب.الرصيد+=self.المبلغ
        self.إلى.حساب.save()
        super(تحويل, self).save(*args, **kwargs)
from django.db import models
import random
import re


class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, default=-1)
    name_fa = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    country_id = models.IntegerField(default=1)   # 1 for iran

    class Meta:
        app_label = 'utils'

    def save(self, *args, **kwargs):
        # Check if `name_fa` contains Persian characters and `name_en` contains English characters
        if not self.contains_persian(self.name_fa):
            raise ValueError("The 'name_fa' field must contain Persian characters.")
        if not self.contains_english(self.name_en):
            raise ValueError("The 'name_en' field must contain English characters.")

        # Generate unique province_id if not set
        if (self.province_id is None) or self.province_id == -1:
            self.province_id = self.generate_unique_province_id()

        super().save(*args, **kwargs)

    @staticmethod
    def contains_persian(text):
        # Check if the text contains Persian characters
        persian_pattern = re.compile(r'[\u0600-\u06FF]')
        return bool(persian_pattern.search(text))

    @staticmethod
    def contains_english(text):
        # Check if the text contains English characters
        english_pattern = re.compile(r'[A-Za-z]')
        return bool(english_pattern.search(text))

    @staticmethod
    def generate_unique_province_id():
        while True:
            new_id = str(random.randint(100000, 999999))
            if not Province.objects.filter(province_id=new_id).exists():
                return new_id

    def __str__(self):
        return self.name_fa


class City(models.Model):
    city_id = models.IntegerField(primary_key=True, default=-1)
    name_fa = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")

    class Meta:
        app_label = 'utils'

    def save(self, *args, **kwargs):
        # Check if `name_fa` contains Persian characters and `name_en` contains English characters
        if not self.contains_persian(self.name_fa):
            raise ValueError("The 'name_fa' field must contain Persian characters.")
        if not self.contains_english(self.name_en):
            raise ValueError("The 'name_en' field must contain English characters.")

        # Generate unique province_id if not set
        if not self.city_id or self.city_id == -1:
            self.city_id = self.generate_unique_city_id()

        super().save(*args, **kwargs)

    @staticmethod
    def contains_persian(text):
        # Check if the text contains Persian characters
        persian_pattern = re.compile(r'[\u0600-\u06FF]')
        return bool(persian_pattern.search(text))

    @staticmethod
    def contains_english(text):
        # Check if the text contains English characters
        english_pattern = re.compile(r'[A-Za-z]')
        return bool(english_pattern.search(text))

    @staticmethod
    def generate_unique_city_id():
        while True:
            new_id = str(random.randint(100000, 999999))
            if not City.objects.filter(city_id=new_id).exists():
                return new_id

    def __str__(self):
        return self.name_fa
  

class CityAdditionalInfo(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country_id = models.IntegerField(default=1)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city_profile = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ('city', 'province', 'country_id')

    def __str__(self):
        return f"{self.city.name_fa} - {self.province.name_fa} - {self.country_id}"

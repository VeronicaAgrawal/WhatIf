from django.db import models
from datetime import datetime


class Category(models.Model):
    DeptNumber = models.CharField(max_length=30, default='')
    DeptName = models.CharField(max_length=200, default='')
    SubDeptNumber = models.CharField(max_length=30, default='')
    SubDeptName = models.CharField(max_length=200, default='')
    CategoryNumber = models.CharField(max_length=30, default='')
    CategoryName = models.CharField(max_length=200, default='')
    UserId = models.IntegerField(default=0)

class Items(models.Model):
    IGTIN = models.CharField(max_length=30, default='')
    ICategoryNumber = models.CharField(max_length=30, default='')
    IDescription = models.CharField(max_length=200, default='')
    ISellSize = models.CharField(max_length=30, default='')
    ISellUnitOfMeasure = models.CharField(max_length=30, default='')
    IBrand = models.CharField(max_length=30, default='')
    IStatus = models.CharField(max_length=30, default='')
    UserId = models.IntegerField(default=0)

class Stores(models.Model):
    StoreID = models.CharField(max_length=30, default='')
    StoreName = models.CharField(max_length=30, default='')
    StoreAddress1 = models.CharField(max_length=200, default='')
    StoreAddress2 = models.CharField(max_length=200, default='')
    StoreCity = models.CharField(max_length=30, default='')
    StoreState = models.CharField(max_length=30, default='')
    StoreZipCode = models.CharField(max_length=30, default='')
    StorePhoneNumber = models.CharField(max_length=30, default='')
    StoreStatus = models.CharField(max_length=30, default='')
    StoreStatusDate = models.CharField(max_length=30, default='')
    StoreTimeZone = models.CharField(max_length=30, default='')
    StoreLatitude = models.CharField(max_length=30, default='')
    StoreLongitude = models.CharField(max_length=30, default='')
    UserId = models.IntegerField(default=0)

class Transactions(models.Model):
    ProcessDate = models.CharField(max_length=30, default='')
    TillNumber = models.CharField(max_length=30, default='')
    TransactionId = models.CharField(max_length=200, default='')
    LineNumber = models.CharField(max_length=200, default='')
    EmployeeId = models.CharField(max_length=30, default='')
    StoreId = models.CharField(max_length=30, default='')
    UPC = models.CharField(max_length=30, default='')
    TransactionType = models.CharField(max_length=30, default='')
    TransactionSubType = models.CharField(max_length=30, default='')
    DepartmentId = models.CharField(max_length=30, default='')
    Quantity = models.CharField(max_length=30, default='')
    ProductPrice = models.CharField(max_length=30, default='')
    TotalAmount = models.CharField(max_length=30, default='')
    Cost = models.CharField(max_length=30, default='')
    PriceTypeId = models.CharField(max_length=30, default='')
    UserId = models.IntegerField(default=0)

class Products(models.Model):
    Name = models.CharField(max_length=30, default='')
    UPC = models.CharField(max_length=30, default='')
    Brand = models.CharField(max_length=30, default='')
    StoreId = models.CharField(max_length=30, default='')
    ProductPrice = models.CharField(max_length=30, null=True, blank=True, default=None)
    Cost = models.CharField(max_length=30, null=True, blank=True, default=None)
    DeptNumber = models.CharField(max_length=30, default='')
    SubDeptNumber = models.CharField(max_length=30, default='')
    CategoryNumber = models.CharField(max_length=30, default='')
    DeptName = models.CharField(max_length=30, default='')
    SubDeptName = models.CharField(max_length=30, default='')
    CategoryName = models.CharField(max_length=30, default='')
    Quantity = models.CharField(max_length=30, null=True, blank=True, default=None)
    Peod = models.FloatField(null=True, blank=True, default=None)
    UserId = models.IntegerField(default=0)
    DateScraped = models.DateTimeField(null= True, blank=True)
    FirstCompetitor = models.CharField(max_length= 50, blank=True, default='')
    FirstCompPrice = models.CharField(max_length=30, null=True, blank=True, default=None)
    SecondCompetitor = models.CharField(max_length=50, blank=True, default='')
    SecondCompPrice = models.CharField(max_length=30, null=True, blank=True, default=None)
    ThirdCompetitor = models.CharField(max_length=50, blank=True, default='')
    ThirdCompPrice = models.CharField(max_length=30, null=True, blank=True, default=None)
    Image = models.URLField(max_length=250, default='imgno.png')
    Description = models.CharField(max_length=1000, default='')
    InterceptCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    PriceCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    PromoIndexCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    WeekCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    CoefficientDate = models.DateTimeField(null=True, blank=True)
    CompetitorIndex = models.IntegerField(null=True)
    NB1_PriceCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    NB1_PromoCoefficient = models.CharField(max_length=30, null=True, blank=True, default=None)
    NB1_ProductId = models.IntegerField(null=True)
    CannibalizationIds = models.CharField(max_length=30, null=True, blank=True, default=None)
    HaloEffectIds = models.CharField(max_length=30, null=True, blank=True, default=None)
    CompetitorBrandIds = models.CharField(max_length=30, null=True, blank=True, default=None)

class Settings(models.Model):
    UserId = models.IntegerField(default=0)
    EndingNumber = models.IntegerField()
    MinCompPrice = models.IntegerField()
    MaxCompPrice = models.IntegerField()
    MinPriceChangeLimits = models.IntegerField()
    MaxPriceChangeLimits = models.IntegerField()
    MinMargin = models.IntegerField()
    MaxMargin = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField()
    MinVolumeChangeLimits = models.IntegerField(null=True)
    MaxVolumeChangeLimits = models.IntegerField(null=True)

class Licence(models.Model):
    UserId = models.IntegerField(default=0)
    CompetitorFeatured = models.BooleanField(default=True)
    WhatIfFeatured = models.BooleanField(default=True)
    ExpiryDate = models.DateTimeField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

class SalesForecast(models.Model):
    WeekNumber = models.IntegerField()
    Year = models.CharField(max_length=30, null=True, blank=True, default=None)
    Date = models.DateTimeField()
    Quantity = models.CharField(max_length=30, null=True, blank=True, default=None)
    ProductId = models.IntegerField()
    UserId = models.IntegerField(default=0)
    PromoId = models.IntegerField(default=0)

class Details(models.Model):
    ProductId = models.IntegerField()
    CompetitorsLogo = models.URLField(max_length=250)
    ProductName = models.CharField(max_length=250, default='')
    Description = models.CharField(max_length=1000, default='')
    Rating = models.CharField(max_length=250, default='')
    Image = models.URLField(max_length=250)
    Price = models.CharField(max_length=30, null=True, blank=True, default=None)
    UserId = models.IntegerField(default=0)
    ProductUrl = models.CharField(max_length=500, null=True, blank=True, default=None)

class ProductHistory(models.Model):
    ProductId = models.IntegerField()
    Price = models.CharField(max_length=30, null=True, blank=True, default=None)
    Date = models.DateTimeField()
    UnitSales = models.CharField(max_length=30, null=True, blank=True, default=None)
    UserId = models.IntegerField(default=0)
    PriceTypeId = models.IntegerField(default=1)
    BrandPresent = models.CharField(max_length=30, null=True, blank=True, default=None)

class Promotions(models.Model):
    ProductId = models.IntegerField()
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    PromotionType = models.CharField(max_length=250, default='')
    PromotionName = models.CharField(max_length=250, default='')
    PromotionSpend = models.CharField(max_length=250, default='')
    SalesWithoutPromo = models.CharField(max_length=30, default='')
    SalesWithPromo = models.CharField(max_length=30, default='')
    BICLocation = models.CharField(max_length=250, default='')
    BICType = models.CharField(max_length=250, default='')
    TotalOpportunity = models.CharField(max_length=30, default='')
    SalesLift = models.CharField(max_length=30, default='')
    UserId = models.IntegerField()
    PromotionIndex = models.IntegerField(null=True)
    PromotionPrice = models.IntegerField(null=True)
    PullForward = models.CharField(max_length=30, null=True, blank=True, default=None)

class Seasonality(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    WeekNumber = models.IntegerField()
    SeasonalityIndex = models.CharField(max_length=30, null=True, blank=True, default=None)
    DateCreated = models.DateTimeField(null= True, blank=True)
    BaselineSales = models.CharField(max_length=30, null=True, blank=True, default=None)

class PromotionTierRule(models.Model):
    PromotionIndexTier = models.IntegerField()
    PromotionPercentage = models.CharField(max_length=30, null=True, blank=True, default=None)
    PromotionType = models.CharField(max_length=250, default='')
    ImpactPercentValue = models.CharField(max_length=30, null=True, blank=True, default=None)
    CreatedDate = models.DateTimeField(auto_now_add=True)

class CompetitorTierRule(models.Model):
    PeodRange = models.CharField(max_length=30, null=True, blank=True, default=None)
    CompetitorTier = models.CharField(max_length=30, null=True, blank=True, default=None)
    ImpactPercentValue = models.CharField(max_length=30, null=True, blank=True, default=None)
    CreatedDate = models.DateTimeField(auto_now_add=True)

class Display(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    Stores = models.CharField(max_length=30, null=True, blank=True, default=None)
    AuthStores = models.CharField(max_length=30, null=True, blank=True, default=None)
    DisplayPresentPercent = models.CharField(max_length=30, null=True, blank=True, default=None)
    AuthDisplayPercent = models.CharField(max_length=30, null=True, blank=True, default=None)

class Region(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    Division = models.CharField(max_length=100, null=True, blank=True, default=None)
    Region = models.CharField(max_length=100, null=True, blank=True, default=None)
    Stores = models.CharField(max_length=30, null=True, blank=True, default=None)
    DisplayPresent = models.CharField(max_length=30, null=True, blank=True, default=None)

class Location(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    SalesLift = models.CharField(max_length=30, null=True, blank=True, default=None)
    DisplayPercent = models.CharField(max_length=30, null=True, blank=True, default=None)
    Sales = models.CharField(max_length=30, null=True, blank=True, default=None)
    Location = models.CharField(max_length=100, null=True, blank=True, default=None)

class Type(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    SalesLift = models.CharField(max_length=30, null=True, blank=True, default=None)
    DisplayPercent = models.CharField(max_length=30, null=True, blank=True, default=None)
    Sales = models.CharField(max_length=30, null=True, blank=True, default=None)
    Type = models.CharField(max_length=100, null=True, blank=True, default=None)

class ValueCapture(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    SalesLift = models.CharField(max_length=30, null=True, blank=True, default=None)
    Execution = models.CharField(max_length=30, null=True, blank=True, default=None)
    BestInClassDisplay = models.CharField(max_length=250, default='')
    AdditionalSales = models.CharField(max_length=30, null=True, blank=True, default=None)
    MissingDollars = models.CharField(max_length=30, null=True, blank=True, default=None)

class Attributes(models.Model):
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    Role = models.CharField(max_length=30, null=True, blank=True, default=None)
    ShelfLife = models.CharField(max_length=30, null=True, blank=True, default=None)
    AvgPurchaseFreq = models.CharField(max_length=30, null=True, blank=True, default=None)







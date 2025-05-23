from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category

class ProductTranslationOptions(TranslationOptions):
    fields = ('name_i18n', 'description_i18n')

class CategoryTranslationOptions(TranslationOptions):
    fields = ()

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)

from django.contrib import admin
from .models import Article, Comment, Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_comment', 'reason', 'created_at', 'is_resolved')
    list_filter = ('resolved', 'created_at')  # ✅ Maintenant, `resolved` est bien un champ du modèle `Report`
    search_fields = ('reporter__username', 'reported_comment__content', 'reason')

    def is_resolved(self, obj):
        """ Retourne True si le signalement est résolu """
        return obj.resolved
    is_resolved.boolean = True  # ✅ Affichage sous forme de case cochée
    is_resolved.short_description = "Resolved"  # ✅ Nom personnalisé

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Report, ReportAdmin)

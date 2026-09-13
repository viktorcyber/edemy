from django.contrib.admin import AdminSite as BaseAdminSite
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path, reverse


@staff_member_required
def admin_statistics(request):
    return render(request, "admin/statistics.html", {"title": "Charts"})


class AdminSite(BaseAdminSite):
    def get_app_list(self, request, _=None):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Statistics",
                "app_label": "statistics",
                "models": [
                    {
                        "name": "Charts",
                        "object_name": "charts",
                        "admin_url": reverse("admin_statistics"),
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [path("statistics/", admin_statistics, name="admin_statistics")]
        return urls

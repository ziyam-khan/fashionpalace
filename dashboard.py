# from django.utils.translation import gettext_lazy as _
# from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
# from jet.dashboard.dashboard_modules import google_analytics
# from django.forms import widgets


# class CustomIndexDashboard(Dashboard):
#     columns = 3

#     def init_with_context(self, context):
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
#        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
#        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)
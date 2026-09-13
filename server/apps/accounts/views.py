from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        return [
            [75, 44, 92, 11, 44, 95, 35],
            [41, 92, 18, 3, 73, 87, 92],
            [87, 21, 94, 3, 90, 13, 65],
        ]

class Stats {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.time_interval = "Weekly";
		this.refresh();
	}

	refresh() {
		this.render_chart();
	}

	render_chart() {
		this.chart_filters = {'type': 'Hub Item View'};
		this.chart_config = {
			timespan: 'Last Year',
			time_interval: 'Monthly',
			type: 'Line',
			value_based_on: 'name',
			chart_type: 'Count',
			document_type: 'Hub Log',
			name: 'Views',
			width: 'half',
			based_on: 'creation'
		};
		this.chart = new frappe.Chart( '#chart', {
			title: ' ',
			type: 'line',
			height: 300,
			data: {
				labels: [],
				datasets: [{}]
			},
			colors: ['green'],
			axisOptions: {
				xIsSeries: true
			},
			lineOptions: {
				hideDots: true,
				heatLine: 1,
				regionFill: 1
			}
		});
		this.update_data();
	}
	
	update_data() {
		this.chart_config.filters_json = JSON.stringify(this.chart_filters);

		frappe.call('hub.www.stats.get_dashboard_data', {
			chart: this.chart_config,
			no_cache: 1,
		}).then(chart => {
			if (chart.message) {
				this.chart.update(chart.message);
			}
		});
	}
}

frappe.ready(() => {
	const stats = new Stats(document.getElementById('chart-container'));
	window.stats = stats;
});
import { Chart } from "frappe-charts"

class Stats {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.time_interval = "Weekly";
		this.timespan = "Last Year";
		this.refresh();
	}

	refresh() {
		this.check_active_period();
		this.render_chart();
	}

	check_active_period() {
		let me = this;
		$(".btn-group > .btn").click(function(){
			let interval = $(this).find('input').attr('id');
			me.time_interval = interval.charAt(0).toUpperCase() + interval.slice(1);
			me.timespan = me.time_interval==='Yearly' ? 'All Time': 'Last Year';
			me.render_chart();
		});
	}

	render_chart() {
		this.chart_filters = {'type': 'Hub Item View'};
		this.chart_config = {
			timespan: this.timespan,
			time_interval: this.time_interval,
			type: 'Line',
			value_based_on: 'name',
			chart_type: 'Count',
			document_type: 'Hub Log',
			name: 'Views',
			width: 'half',
			based_on: 'creation'
		};
		this.chart = new Chart( '#chart', {
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
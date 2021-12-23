const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				green: {
					600: '#009444'
				}
			}
		}
	},
	plugins: [require('daisyui')]
};

module.exports = config;

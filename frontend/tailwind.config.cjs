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
	plugins: [require('daisyui'), require('@tailwindcss/typography')]
};

module.exports = config;

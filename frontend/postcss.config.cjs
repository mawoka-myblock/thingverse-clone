const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const tailwindcss = require("tailwindcss");

const mode = process.env.NODE_ENV;
const dev = mode === 'development';

module.exports = {
	syntax: 'postcss-scss',
	plugins: [
        //Some plugins, like tailwindcss/nesting, need to run before Tailwind,
        tailwindcss(),
        //But others, like autoprefixer, need to run after,
        autoprefixer(),
        !dev && cssnano({
			preset: "default",
		})
    ],
};

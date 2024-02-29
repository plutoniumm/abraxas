import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const sidebar = [
	{
		label: 'Guides',
		items: [
			{ label: 'Welcome', link: '/welcome' },
			{ label: 'toPrime', link: '/prime' },
		],
	},
];


// https://astro.build/config
export default defineConfig( {
	site: 'https://plutoniumm.github.io',
	base: import.meta.env.DEV ? '/' : '/abraxas/',
	integrations: [
		starlight( {
			title: 'Abraxas',
			social: {
				github: 'https://github.com/plutoniumm/abraxas',
			},
			sidebar,
		} ),
	],
} );

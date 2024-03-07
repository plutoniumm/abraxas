import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const sidebar = [
	{
		label: 'Guides',
		items: [
			{ label: 'Welcome', link: '/welcome' },
			{ label: 'String', link: '/prime' },
			{ label: 'Parse', link: '/parse' },
			{ label: 'Uses', link: '/uses' },
		],
	},
	{
		label: 'Modifiers',
		items: [
			{ label: 'String', link: '/prime-mod' },
		],
	}
];

// https://astro.build/config
export default defineConfig( {
	site: 'https://plutoniumm.github.io',
	base: import.meta.env.DEV ? '/' : '/abraxas/',
	markdown: {
		remarkPlugins: [ remarkMath ],
		rehypePlugins: [ rehypeKatex ],
	},
	integrations: [
		starlight( {
			title: 'Abraxas',
			social: {
				github: 'https://github.com/plutoniumm/abraxas',
			},
			sidebar,
			customCss: [
				"./src/css/katex.css"
			]
		} ),
	],
} );

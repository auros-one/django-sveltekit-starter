<script lang="ts">
	import type { SpinnerTypes } from './spinner.type';
	export let color: SpinnerTypes['color'] = '#3484d6';
	export let unit: SpinnerTypes['unit'] = 'px';
	export let duration: SpinnerTypes['duration'] = '0.3s';
	export let size: SpinnerTypes['size'] = '26';
	export let pause: SpinnerTypes['pause'] = false;
	export let ringThickness: SpinnerTypes['ringThickness'] = 1.5;
</script>

<div
	class="circle"
	class:pause-animation={pause}
	style="--size: {size}{unit}; --color: {color}; --duration: {duration}; --thickness: {ringThickness}"
></div>

<style>
	.circle {
		height: var(--size);
		width: var(--size);
		border-color: var(--color) transparent var(--color) var(--color);
		border-width: calc(var(--thickness) * var(--size) / 15);
		border-style: solid;
		border-image: initial;
		border-radius: 50%;
		animation: var(--duration) linear 0s infinite normal none running rotate;
	}
	.pause-animation {
		animation-play-state: paused;
	}
	@keyframes rotate {
		0% {
			transform: rotate(0);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>

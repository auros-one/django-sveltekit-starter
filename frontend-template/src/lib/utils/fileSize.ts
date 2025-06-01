export function formatBytes(bytes: number, decimals = 1): string {
	if (bytes === 0) return '0 Bytes';

	const k = 1000; // Use 1024 for binary standard
	const dm = decimals < 0 ? 0 : decimals;
	const sizes = ['Bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

	const i = Math.floor(Math.log(bytes) / Math.log(k));

	return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

import { writeFile, unlink, readFile } from 'fs/promises';
import { existsSync } from 'fs';
import { exec } from 'child_process';
import fetch from 'node-fetch';
import yaml from 'js-yaml';

const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
const DOCS_PATH = '/api/docs/schema';

fetch(`${BACKEND_URL}${DOCS_PATH}`)
	.then((response) => response.text())
	.then(async (schemaText) => {
		// Write the schema to a temporary file
		await writeFile('./temp-schema.yml', schemaText);

		// Read and parse the schema file
		const schema = yaml.load(await readFile('./temp-schema.yml', 'utf8'));

		// Use npx to generate TypeScript types
		exec(
			'npx openapi-typescript ./temp-schema.yml -o ./src/lib/api/backend-api-schema.d.ts',
			(error, stdout, stderr) => {
				if (error) {
					console.error(`Error: ${error.message}`);
					return;
				}
				if (stderr) {
					console.error(`stderr: ${stderr}`);
					return;
				}

				// Delete the temporary file if it exists
				if (existsSync('./temp-schema.yml')) unlink('./temp-schema.yml');
			}
		);

		console.log(`🚀 Synced Backend: ${schema.info.title} (${schema.info.version})\n`);
	})
	.catch((error) => console.error('Error:', error));

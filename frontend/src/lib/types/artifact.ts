export interface Artifact {
	name: string;
	description: string;
	filename: string;
	category: string;
	complexity: 'beginner' | 'intermediate' | 'advanced';
	tags: string[];
}

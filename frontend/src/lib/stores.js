import { writable } from 'svelte/store';

export const apiurl = "http://localhost:8000"
export const token = writable(null)

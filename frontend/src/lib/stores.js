import { writable } from 'svelte/store';
import Cookies from "js-cookie"

export const apiurl = "http://localhost:8080"
export const loggedin = writable(Cookies.get("expiry") === undefined ? false : true)
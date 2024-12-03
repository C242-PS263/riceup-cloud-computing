import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function apiUrl(url: string) {
  url = url.startsWith("/") ? url : `/${url}`;
  return `${import.meta.env.VITE_BACKEND_URL}${url}`;
}
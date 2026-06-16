import type { NextRequest } from "next/server";

export async function readBody(request: NextRequest) {
  const contentType = request.headers.get("content-type") ?? "";

  if (contentType.includes("application/json")) {
    return (await request.json()) as Record<string, unknown>;
  }

  const formData = await request.formData();
  return Object.fromEntries(formData.entries()) as Record<string, FormDataEntryValue>;
}

export function toString(value: FormDataEntryValue | unknown) {
  return String(value ?? "").trim();
}

export function toNumber(value: FormDataEntryValue | unknown) {
  const parsed = Number(String(value ?? "").trim());
  return Number.isFinite(parsed) ? parsed : Number.NaN;
}

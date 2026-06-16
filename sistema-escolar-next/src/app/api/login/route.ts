import { NextRequest, NextResponse } from "next/server";

import { AUTH_COOKIE_NAME, buildSessionCookie, hasValidCredentials } from "@/lib/auth";

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const username = String(formData.get("usuario") ?? "").trim();
  const password = String(formData.get("senha") ?? "").trim();

  if (!hasValidCredentials(username, password)) {
    const url = new URL("/login", request.url);
    url.searchParams.set("error", "Usuario ou senha invalidos.");
    return NextResponse.redirect(url);
  }

  const { value, expiresAt } = buildSessionCookie(username);
  const response = NextResponse.redirect(new URL("/dashboard", request.url));
  response.cookies.set(AUTH_COOKIE_NAME, value, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    expires: expiresAt,
  });

  return response;
}

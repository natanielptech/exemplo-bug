import { NextRequest, NextResponse } from "next/server";

const AUTH_COOKIE_NAME = "sistema_escolar_session";

const PUBLIC_PATHS = ["/login", "/api/login", "/api/health"];

function isPublicPath(pathname: string) {
  return PUBLIC_PATHS.some((path) => pathname === path || pathname.startsWith(`${path}/`));
}

function looksLikeStaticAsset(pathname: string) {
  return pathname.startsWith("/_next/") || pathname.includes(".");
}

export default function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (looksLikeStaticAsset(pathname) || isPublicPath(pathname)) {
    return NextResponse.next();
  }

  const hasSession = Boolean(request.cookies.get(AUTH_COOKIE_NAME)?.value);

  if (!hasSession) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("error", "Faça login para continuar.");
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};

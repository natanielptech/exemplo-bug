import { createHmac, timingSafeEqual } from "crypto";
import { cookies } from "next/headers";

import type { SessionData } from "@/lib/types";

export const AUTH_COOKIE_NAME = "sistema_escolar_session";
const SESSION_TTL_MS = 8 * 60 * 60 * 1000;

export function getCredentials() {
  return {
    username: process.env.ADMIN_USERNAME ?? "nataniel",
    password: process.env.ADMIN_PASSWORD ?? "123",
  };
}

function getSecret() {
  return process.env.SESSION_SECRET ?? "dev-secret-change-me";
}

function sign(value: string) {
  return createHmac("sha256", getSecret()).update(value).digest("base64url");
}

function safeEquals(a: string, b: string) {
  const left = Buffer.from(a);
  const right = Buffer.from(b);

  if (left.length !== right.length) {
    return false;
  }

  return timingSafeEqual(left, right);
}

function encodeSession(session: SessionData) {
  const payload = Buffer.from(JSON.stringify(session)).toString("base64url");
  const signature = sign(payload);
  return `${payload}.${signature}`;
}

function decodeSession(raw?: string): SessionData | null {
  if (!raw) {
    return null;
  }

  const [payload, signature] = raw.split(".");
  if (!payload || !signature) {
    return null;
  }

  if (!safeEquals(signature, sign(payload))) {
    return null;
  }

  try {
    const decoded = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as SessionData;
    if (
      typeof decoded?.username !== "string" ||
      typeof decoded?.expiresAt !== "number" ||
      Date.now() > decoded.expiresAt
    ) {
      return null;
    }

    return decoded;
  } catch {
    return null;
  }
}

export async function getSession() {
  const cookieStore = await cookies();
  return decodeSession(cookieStore.get(AUTH_COOKIE_NAME)?.value);
}

export function hasValidCredentials(username: string, password: string) {
  const credentials = getCredentials();
  return username === credentials.username && password === credentials.password;
}

export function buildSessionCookie(username: string) {
  const expiresAt = Date.now() + SESSION_TTL_MS;
  return {
    value: encodeSession({ username, expiresAt }),
    expiresAt: new Date(expiresAt),
  };
}

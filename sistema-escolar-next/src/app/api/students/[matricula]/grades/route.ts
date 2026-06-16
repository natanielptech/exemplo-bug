import { NextRequest, NextResponse } from "next/server";

import { readBody, toNumber } from "@/lib/http";
import { lancarNota } from "@/lib/school-store";

type RouteProps = {
  params: Promise<{ matricula: string }> | { matricula: string };
};

function isJson(request: NextRequest) {
  return (request.headers.get("content-type") ?? "").includes("application/json");
}

export async function POST(request: NextRequest, { params }: RouteProps) {
  const resolvedParams = await params;
  const body = await readBody(request);
  const nota = toNumber(body.nota);

  try {
    const student = await lancarNota(resolvedParams.matricula, nota);

    if (isJson(request)) {
      return NextResponse.json(student, { status: 201 });
    }

    const url = new URL(`/alunos/${student.matricula}`, request.url);
    url.searchParams.set("success", "Nota registrada com sucesso.");
    return NextResponse.redirect(url);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Falha ao registrar nota.";

    if (isJson(request)) {
      return NextResponse.json({ error: message }, { status: 400 });
    }

    const url = new URL(`/alunos/${resolvedParams.matricula}`, request.url);
    url.searchParams.set("error", message);
    return NextResponse.redirect(url);
  }
}

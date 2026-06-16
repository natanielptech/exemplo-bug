import { NextRequest, NextResponse } from "next/server";

import { readBody, toString } from "@/lib/http";
import { cadastrarAluno, listarAlunos } from "@/lib/school-store";

function isJson(request: NextRequest) {
  return (request.headers.get("content-type") ?? "").includes("application/json");
}

export async function GET() {
  const students = await listarAlunos();
  return NextResponse.json({ items: students });
}

export async function POST(request: NextRequest) {
  const body = await readBody(request);
  const matricula = toString(body.matricula);
  const nome = toString(body.nome);

  try {
    const student = await cadastrarAluno(matricula, nome);

    if (isJson(request)) {
      return NextResponse.json(student, { status: 201 });
    }

    const url = new URL("/dashboard", request.url);
    url.searchParams.set("success", `Aluno ${student.nome} cadastrado com sucesso.`);
    return NextResponse.redirect(url);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Falha ao cadastrar aluno.";

    if (isJson(request)) {
      return NextResponse.json({ error: message }, { status: 400 });
    }

    const url = new URL("/dashboard", request.url);
    url.searchParams.set("error", message);
    return NextResponse.redirect(url);
  }
}

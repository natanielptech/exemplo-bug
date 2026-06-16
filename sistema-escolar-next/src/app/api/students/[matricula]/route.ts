import { NextRequest, NextResponse } from "next/server";

import { buscarAluno } from "@/lib/school-store";

type RouteProps = {
  params: Promise<{ matricula: string }> | { matricula: string };
};

export async function GET(_request: NextRequest, { params }: RouteProps) {
  const resolvedParams = await params;

  try {
    const student = await buscarAluno(resolvedParams.matricula);
    return NextResponse.json(student);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Aluno nao encontrado.";
    return NextResponse.json({ error: message }, { status: 404 });
  }
}

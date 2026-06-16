import { kv } from "@vercel/kv";
import { mkdir, readFile, writeFile } from "fs/promises";
import { dirname, join } from "path";

import type { SchoolState, Student } from "@/lib/types";

const STORAGE_KEY = "sistema-escolar-next:state";
const LOCAL_STATE_FILE = join(process.cwd(), "data", "school-state.json");

const EMPTY_STATE: SchoolState = {
  students: [],
};

function useKv() {
  return Boolean(process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN);
}

function normalizeStudent(value: unknown): Student | null {
  if (!value || typeof value !== "object") {
    return null;
  }

  const candidate = value as Record<string, unknown>;
  if (typeof candidate.matricula !== "string" || typeof candidate.nome !== "string") {
    return null;
  }

  const notas = Array.isArray(candidate.notas)
    ? candidate.notas.map((nota) => Number(nota)).filter((nota) => Number.isFinite(nota))
    : [];

  const now = new Date().toISOString();

  return {
    matricula: candidate.matricula,
    nome: candidate.nome,
    notas,
    createdAt: typeof candidate.createdAt === "string" ? candidate.createdAt : now,
    updatedAt: typeof candidate.updatedAt === "string" ? candidate.updatedAt : now,
  };
}

function normalizeState(value: unknown): SchoolState {
  if (!value || typeof value !== "object") {
    return EMPTY_STATE;
  }

  const candidate = value as Record<string, unknown>;
  const students = Array.isArray(candidate.students)
    ? candidate.students.map(normalizeStudent).filter((student): student is Student => Boolean(student))
    : [];

  return { students };
}

async function readLocalState(): Promise<SchoolState> {
  try {
    const raw = await readFile(LOCAL_STATE_FILE, "utf8");
    return normalizeState(JSON.parse(raw));
  } catch {
    return EMPTY_STATE;
  }
}

async function writeLocalState(state: SchoolState) {
  await mkdir(dirname(LOCAL_STATE_FILE), { recursive: true });
  await writeFile(LOCAL_STATE_FILE, JSON.stringify(state, null, 2), "utf8");
}

async function readState(): Promise<SchoolState> {
  if (useKv()) {
    const stored = await kv.get<SchoolState>(STORAGE_KEY);
    return normalizeState(stored);
  }

  return readLocalState();
}

async function saveState(state: SchoolState) {
  if (useKv()) {
    await kv.set(STORAGE_KEY, state);
    return;
  }

  await writeLocalState(state);
}

function sortStudents(students: Student[]) {
  return [...students].sort((left, right) => left.nome.localeCompare(right.nome, "pt-BR", { sensitivity: "base" }));
}

function validateMatricula(matricula: string) {
  if (!matricula.trim()) {
    throw new Error("A matricula nao pode ser vazia.");
  }
}

function validateNome(nome: string) {
  if (!nome.trim()) {
    throw new Error("O nome nao pode ser vazio.");
  }
}

function validateNota(nota: number) {
  if (!Number.isFinite(nota)) {
    throw new Error("A nota deve ser numerica.");
  }

  if (nota < 0 || nota > 10) {
    throw new Error("A nota deve estar entre 0 e 10.");
  }
}

export function calcularMedia(notas: number[]) {
  if (!notas.length) {
    return 0;
  }

  const total = notas.reduce((sum, nota) => sum + nota, 0);
  return Math.round((total / notas.length) * 100) / 100;
}

export function calcularSituacao(media: number) {
  return media >= 6 ? "Aprovado" : "Reprovado";
}

export function serializarAluno(aluno: Student) {
  const media = calcularMedia(aluno.notas);

  return {
    matricula: aluno.matricula,
    nome: aluno.nome,
    notas: [...aluno.notas],
    media,
    situacao: calcularSituacao(media),
    createdAt: aluno.createdAt,
    updatedAt: aluno.updatedAt,
  };
}

export async function listarAlunos() {
  const state = await readState();
  return sortStudents(state.students).map(serializarAluno);
}

export async function buscarAluno(matricula: string) {
  validateMatricula(matricula);
  const state = await readState();
  const aluno = state.students.find((item) => item.matricula === matricula);

  if (!aluno) {
    throw new Error("Aluno nao encontrado.");
  }

  return serializarAluno(aluno);
}

export async function cadastrarAluno(matricula: string, nome: string) {
  validateMatricula(matricula);
  validateNome(nome);

  const state = await readState();
  if (state.students.some((aluno) => aluno.matricula === matricula)) {
    throw new Error("Ja existe um aluno com essa matricula.");
  }

  const now = new Date().toISOString();
  const novoAluno: Student = {
    matricula,
    nome,
    notas: [],
    createdAt: now,
    updatedAt: now,
  };

  state.students.push(novoAluno);
  await saveState(state);

  return serializarAluno(novoAluno);
}

export async function lancarNota(matricula: string, nota: number) {
  validateMatricula(matricula);
  validateNota(nota);

  const state = await readState();
  const aluno = state.students.find((item) => item.matricula === matricula);

  if (!aluno) {
    throw new Error("Aluno nao encontrado.");
  }

  aluno.notas.push(nota);
  aluno.updatedAt = new Date().toISOString();
  await saveState(state);

  return serializarAluno(aluno);
}

export async function estatisticas() {
  const alunos = await listarAlunos();
  const totalAlunos = alunos.length;
  const aprovados = alunos.filter((aluno) => aluno.situacao === "Aprovado").length;
  const mediaGeral = totalAlunos
    ? Math.round((alunos.reduce((sum, aluno) => sum + aluno.media, 0) / totalAlunos) * 100) / 100
    : 0;

  return {
    totalAlunos,
    aprovados,
    reprovados: totalAlunos - aprovados,
    mediaGeral,
  };
}

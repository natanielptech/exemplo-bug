export type Student = {
  matricula: string;
  nome: string;
  notas: number[];
  createdAt: string;
  updatedAt: string;
};

export type SchoolState = {
  students: Student[];
};

export type SessionData = {
  username: string;
  expiresAt: number;
};

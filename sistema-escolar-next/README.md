This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:
 # Sistema Escolar em Next.js

 Aplicacao escolar migrada para Next.js App Router, pronta para deploy na Vercel.

 ## Funcionalidades

 - login simples com cookie assinado
 - dashboard com estatisticas
 - cadastro de alunos
 - lancamento de notas
 - detalhe de aluno com historico
 - API JSON para integracao
 - persistencia com Vercel KV ou fallback local em arquivo durante desenvolvimento

 ## Requisitos

 - Node.js 22+

 ## Variaveis de ambiente

 Crie um arquivo `.env.local` com valores como estes:

 ```bash
 SESSION_SECRET=troque-por-uma-chave-segura
 ADMIN_USERNAME=nataniel
 ADMIN_PASSWORD=123
 KV_REST_API_URL=https://...
 KV_REST_API_TOKEN=...
 ```

 Se `KV_REST_API_URL` e `KV_REST_API_TOKEN` nao estiverem definidos, o app usa `data/school-state.json` no ambiente local.

 ## Executar localmente

 ```bash
 npm run dev
 ```

 Abra `http://localhost:3000`.

 ## Build para Vercel

 ```bash
 npm run build
 ```

 ## Rotas principais

 - `/login`
 - `/dashboard`
 - `/alunos/[matricula]`
 - `/api/login`
 - `/api/logout`
 - `/api/students`
 - `/api/students/[matricula]`
 - `/api/students/[matricula]/grades`
 - `/api/health`

 ## Observacao de deploy

 Para persistencia duravel na Vercel, configure um backend de dados suportado no ambiente da plataforma, como Vercel KV/Redis integrado. O fallback local existe apenas para desenvolvimento e nao substitui armazenamento persistente em producao.
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

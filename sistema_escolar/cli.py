from sistema_escolar.repository import AlunoRepository
from sistema_escolar.service import SistemaEscolar


def mostrar_menu() -> None:
    print("\n=== Sistema Escolar Didatico ===")
    print("1. Cadastrar aluno")
    print("2. Lancar nota")
    print("3. Listar alunos")
    print("4. Ver detalhe do aluno")
    print("5. Sair")


def executar() -> None:
    sistema = SistemaEscolar(AlunoRepository())

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                matricula = input("Matricula: ").strip()
                nome = input("Nome: ").strip()
                sistema.cadastrar_aluno(matricula, nome)
                print("Aluno cadastrado com sucesso.")

            elif opcao == "2":
                matricula = input("Matricula do aluno: ").strip()
                nota = float(input("Nota (0 a 10): ").strip())
                sistema.lancar_nota(matricula, nota)
                print("Nota registrada com sucesso.")

            elif opcao == "3":
                alunos = sistema.listar_alunos()
                if not alunos:
                    print("Nenhum aluno cadastrado.")
                for aluno in alunos:
                    print(
                        f"- {aluno.matricula} | {aluno.nome} | "
                        f"Media: {aluno.media:.2f} | {aluno.situacao}"
                    )

            elif opcao == "4":
                matricula = input("Matricula do aluno: ").strip()
                aluno = sistema.buscar_aluno(matricula)
                print(f"Nome: {aluno.nome}")
                print(f"Notas: {aluno.notas if aluno.notas else 'Sem notas'}")
                print(f"Media: {aluno.media:.2f}")
                print(f"Situacao: {aluno.situacao}")

            elif opcao == "5":
                print("Encerrando o sistema.")
                break

            else:
                print("Opcao invalida. Tente novamente.")

        except ValueError as exc:
            print(f"Erro: {exc}")


if __name__ == "__main__":
    executar()

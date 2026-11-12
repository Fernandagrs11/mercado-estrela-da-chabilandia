# Mercado Estrela da Chabilândia — MVP

Projeto acadêmico de controle de estoque com Python, Flask e SQLite.

## Funcionalidades
- Tela inicial com acesso ao cadastro e à consulta.
- Cadastro de produto: nome, quantidade, validade e estoque mínimo.
- Listagem de produtos.
- Alerta para produtos vencidos ou com validade nos próximos 7 dias.
- Alerta quando a quantidade for igual ou inferior ao estoque mínimo.
- Validação de campos e layout responsivo com recursos básicos de acessibilidade.

O registro de entradas e saídas (RF05) ficou fora desta versão, conforme o escopo do MVP.

## Como executar no Windows

1. Instale o Python 3.10 ou superior.
2. Extraia o arquivo ZIP.
3. Abra a pasta `mercado_estrela_mvp` no VS Code.
4. Abra o terminal do VS Code e execute:

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

5. Abra no navegador o endereço indicado no terminal, normalmente:
   `http://127.0.0.1:5000`

## Como testar
- Cadastre um produto com quantidade 10, validade futura e estoque mínimo 5.
- Cadastre outro com quantidade 2 e estoque mínimo 5 para visualizar o alerta de estoque baixo.
- Para testar o alerta de validade, cadastre um produto com validade dentro dos próximos 7 dias.
- A tela de estoque apresenta os alertas e a lista de produtos.

## Observações
- O banco `estoque.db` é criado automaticamente na primeira execução.
- Os dados ficam armazenados localmente no computador.
- Use somente dados fictícios na demonstração acadêmica.
- Este projeto é um protótipo acadêmico, não um sistema pronto para uso comercial.

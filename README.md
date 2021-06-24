# Documentação para o TP2 da disciplica de Scripting no Processamento de Linguagem Natural

# Descrição

Projeto que tem por objetivo simular, a uma escala menor, os formulários que a Google permite criar.
Fá-lo, recebendo do User um ficheiro **XML** com o template do formulário, e criando a partir desse ficheiro **XML** uma pequena aplicação WEB em flask, que disponibiliza esse formulário e guarda localmente os dados submetidos por quem preencher o formulário.

# Formato do ficheiro XML de Input

    <?xml version="1.0"?>

    <data>
      <title>Formulário Teste</title>

      <item type="text" required="true">
          <text>Nome</text>
      </item>

      <item type="number">
          <text>Idade</text>
      </item>

      <item type="radio">
          <title>Sexo</title>
          <text>Masculino</text>
          <text>Feminino</text>
          <text>Outro</text>
      </item>

      <item type="checkbox">
          <title>Cores</title>
          <text>Amarelo</text>
          <text>Azul</text>
          <text>Verde</text>
          <text>Vermelho</text>
      </item>

      <item type="select">
          <title>Estação</title>
          <text>Verão</text>
          <text>Primavera</text>
          <text>Inverno</text>
          <text>Outono</text>
      </item>

      <item type="file">
          <text>Fotografia</text>
      </item>
      
    </data>

O ficheiro de input **XML** para ser aceite deve estar no seguinte formato:

1. Tag data que encapsulará toda as outras tags.
1. Tag <title> onde o User indica o título que o formulário vai ter.
2. Uma lista de tags <item>. Cada uma representará um campo do formulário.
3. Cada tag <item> deverá ter o atributo **type**, que determinará a funcionalidade deste campo do formulário.
4. Cada tag <item> poderá também ter o atributo **required**, que caso esteja com valor **true**, significa que este campo é de preenchimento obrigatório.
  
As tags **item** poderão ter as seguintes variantes, consoante o valor do atributo **type**:
  
* Se o atributo **type** tomar o valor de "text", representa no formulário um campo de texto e a tag <text> representa o nome desse campo.
* Se o atributo **type** tomar o valor de "number", representa no formulário um campo para o utilizador introduzir um número e a tag <text> representa o nome desse campo.
* Se o atributo **type** tomar o valor de "file", representa no formulário uma secção para o utilizador fazer upload de um ficheiro e tag <text> representa o nome desse campo.
* Se o atributo **type** tomar o valor de "radio", representa uma secção no formulário onde o User tem uma sério de opções e tem de escolher apenas 1. A tag <title> representa o título desse campo e as tags "text" representam o nome das diferentes opções disponíveis para serem escolhidas.
* Se o atributo **type** tomar o valor de "checkbox", representa a mesma coisa que o anterior, mas o user pode selecionar 0 ou mais opções.
* Se o atributo **type** tomar o valor de "select", representa um dropdown menu com diferentes opções onde o user seleciona uma. A tag <title> representa o título desse campo e as tags "text" representam o nome das diferentes opções disponíveis para serem escolhidas.
  
Os resultados das submissões do formulário serem guardados num ficheiro à escolha do utilizador, desde que seja em formato **json** ou **csv**.

# Exemplo de Utilização
  
    python3 app.py inputTemplate.xml results.json
  
# Exemplo dos resultados obtidos após a submissão do formulário
  
    [
     {
         "Idade": "13",
         "Nome": "S",
         "Sex": "Girl",
         "Fotografia": "pessoa.jpeg"
     },
     {
         "Idade": "16",
         "Nome": "J",
         "Sex": "Boy",
         "Fotografia": "pessoa.jpeg"
     },
     {
         "Idade": "15",
         "Nome": "M",
         "Sex": "Girl",
         "Fotografia": "pessoa.jpeg"
     },
     {
         "Idade": "2",
         "Nome": "M",
         "Sexo": "Masculino"
     }
    ]

  # Formulário resultante do ficheiro **XML** usado como exemplo.
    
![Screenshot 2021-06-24 at 15 36 37 (2)](https://user-images.githubusercontent.com/68651003/123281997-0c6c3100-d502-11eb-9cd6-bbf39d230e28.png)

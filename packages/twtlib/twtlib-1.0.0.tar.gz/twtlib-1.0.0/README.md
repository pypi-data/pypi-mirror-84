# Twtlib
### (pt) Lib para buscar/postar no Twitter
### (en) Lib to search/post on Twitter
By Daniel Ribeiro | <a href="https://github.com/ribeiro-daniel">github/ribeiro-daniel</a>
<hr>

> ## Documentação/Documentation:

**(pt) Atenção! Para utilizar a Twtlib, você precisará de uma API_KEY, API_SECRET, TOKEN_KEY e TOKEN_SECRET disponibilizadas pelo próprio Twitter.**

<hr>

Para importar a Twtlib, utilize o seguinte comando:

> from twtlib import Twtlib

<hr>

Assim que instanciar a classe Twitter, passe suas credenciais no construtor, caso contrário, não irá funcionar.<br>

> Ex:<br>test = Twtlib(API_KEY, API_SECRET, TOKEN_KEY, TOKEN_SECRET)

<hr>

> ## Métodos/Methods:
- postar(string)
- buscar(string, lang)

  Para resultados em Português Brasileiro, defina lang: 'pt'<br>
  For results in english, set lang: 'en'
  
 <hr>



Bibliotecas utilizadas na Twtlib:

- oauth2
- json
- urllib . parse

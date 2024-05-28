O código antigo, sem o padrão State, apresentava problemas de organização e entendimento, além de ser distribuído em apenas um arquivo, que estava ficando muito grande, e tornou-se 
  difícil pensar em como o que precisava ser feito no projeto poderia ser estruturado da forma que estava.
<br/><br/>O novo código foi feito com o padrão State, tanto em forma de classes, quanto em forma de enumeração, quando foi possível. Cada grande estado tornou-se uma classe e são chamados
   dentro dos métodos do main. Dentro desses estados, em alguns casos, houve mais uma divisão em estados enumerados, como, por exemplo, para desenhar um triângulo, que tem o estado de 
    início e o de final de desenho.
<br/>Existe uma classe de gerenciamento de estados, que contém algumas informações gerais, faz o controle do estado atual e permite que ele seja trocado. Com essas mudanças, ficou 
  muito mais fácil para adicionar novos elementos ao projeto, pois é necessário apenas criar uma nova classe, alterar seus métodos e depois adicionar as operações referentes a ela na classe de gerenciamento.

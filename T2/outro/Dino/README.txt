# Passos para execução do dinoAI

1. Instalar python3
sudo apt-get install python3

2. Instalar pygame
pip install pygame

3. Executar o jogo
python3 dinoAI.py

Como tirar a interface gráfica:

Na linha 11 existe uma flag chamada RENDER_GAME basta trocar ela para False,
assim o jogo roda sem interface gráfica ficando mais rapido pois o jogo
renderiza em 60 fps com a tela, sem a tela o fps é ilimitado.

RENDER_GAME = False

# Como treinar vários Dinos ao mesmo tempo.

User o código de dinoAIParallel.py, as principais modificações são:

- A função playGame recebe como parametro as soluções para o seu problema
- A função playGame retorna não apenas uma pontuação mas um vetor de pontuação para cada solução.
- Existe a função manyPlaysResultsTrain que recebe as soluções joga com elas X rounds e retorna a media de cada um da população
- Existe a função manyPlaysResultsTest que recebe apenas uma solução e retorna a media de pontuação do individuo

OBS: Ao usar esse código vários dinossauros aparecem na tela jogando ao mesmo tempo, para diferencia-los existe um
quadrado colorido em volta de cada dino, com uma cor diferente para cada dino.


## Melhorias feitas por GFWagnitz em 2022-07-02:

Para melhorar a jogabilidade e tornar o desenvolvimento da IA mais interessante,
foram feitas algumas melhorias no código do DinoAI.py, para tornar mais fidedígno ao original chrome://dino.

Para alterar para essa nova versão é necessario substituir o codigo do dinoAI.py e também todos os arquivos da pasta Assets.
As implementações do KeyClassifier são compatíveis nessa versão, caso já tenha começado a trabalhar nela, só utilizar o 
seu código adicionando a variável obHeight na assinatura.

São essas:

  - Melhoria da geração de obstáculos:
    Agora é possível ter mais de um obstaculo na tela, com distancia variável entre eles,
    não somente um novo obstaculo gerado quando o atual sai de tela

  - Aceleração da descida:
    O jogo original do Chrome possui uma mecânica em que ao clicar para baixo durante o salto,
    a descida é acelerada, agora isso também é possível

  - Altura variável do pássaro:
    passaros agora possuem três alturas, como no jogo original do Chrome: razante, médio e alto.
    No primeiro caso, é necessário pular, no segundo, é necessario agaixar-se e no terceiro,
    apenas não se deve pular

  - Nova variável obHeight:
    Variável que informa a altura do obstáculo, já que agora o passaro possui mais de uma altura de voo.
    Essa variável é passada para o classificador. 

  - Proporções mais compatíveis com o jogo original do Chrome:
    Foram alteradas as proporções do dinossauro e dos obstaculos (todos os assets foram refeitos), trazendo
    o efeito de que uma distância maior à frente é visível, dando espaço a mais de um obstaculo na tela,
    para isso também foram alteradas as velocidades de salto

  - Alteração do jogo de 30 fps para 60 fps:
    A versão anterior possuía alguns problemas relacionados à fisica por ter poucos frames,
    já que as mudanças de posição entre um frame e outro eram muito grandes. Atualizei o jogo para rodar
    com 60fps, como na versão original do jogo. Isso inclusive torna o jogo mais fluido para jogar e assistir.

  - PLAYER_MODE e AI_MODE:
    Agora na linha 10 temos a variável GAME_MODE que permite alterar o modo de jogo, dando controle a um jogador humano





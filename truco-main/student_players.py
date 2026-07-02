### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    Camila Jesus Santana
# RA #01 (quem entregou o código):      323249
# Nome #02:                             Guilherme de Oliveira
# RA #02:                               
from basic_players import Player
from judge import card_value

# Implemente neste arquivo seus jogadores para Truco

'''Anotações: 
        - a minha classe herda ra, nome, image_path, image, cards (list), position, remove_card (metodo),
        str e as q tem q implementar
        - qnd truca, no histórico o ultimo elemento da lista se torna 3, 6 ou 9 quando aumenta, senao retorna
        a forma q a carta foi jogada
        - no historico eu tenho uma lista e depois varias listas de listas onde minha listona é o histórico completo
        cada sub-lista é uma rodada (acho q pode ser chamado de mao) e a sub da sub lista são as jogadas
        - pensei em algo como 4 (numero de cartas jogadas por rodada) - posicao pra saber quantos card_values eu vou ter q ver)
        - vejo, pego o maior valor, se for da minha equipe ou minha carta com maior valor ainda for menor do q a de maior valor,
        eu jogo a menor carta ou truco, se nao eu jogo a maior
        -posso guardar a carta numa lista com a carta e a posicao q ela ta e daí quando eu for ver se é da
        minha equipe ou nao ja vai ser mais facil
        - faço uma variavel de "contador" para ir voltando a qtd de casas mecessarias - nao precisou
        
        
        acho q o problema ta em quando alguem ganha o proximo é o jogador a esquerda dele, logo a position ta indo
        até o round anterior
        
        acho q ate funciona mas vou ter q dar um jeito de acompanhar quem esta jogando primeiro'''


# Jogador que não faz nada. Substitua esta classe para criar as suas, devem herdar da classe Player
class FirstPlayer(Player):
    # Se estiver dúvida sobre como começar olhe os players prontos em basic_players.py e o ReadMe
    def __init__(self):
        super().__init__(0, "Camila", image_path='img/Homer_Simpson.png') # Nome do Jogador

    # Função para retornar o que você vai jogar em determinada mão
    def play(self, top_card, play_hist, score_hist):
        sorted_cards = self.sort_cards(top_card) #lista ordenada
        team = (self.position, (self.position+2)%4)
        print(team)

        if len(play_hist[0])>0:
            for round in play_hist: #cada round de 4 cartas
                print("historico ", play_hist)
                print()
                if self.position!=0:
                    best_value = card_value(round[-1][1], top_card)
                    best_card = round[-1][1]
                    best_card_position = round[-1][0]

                    for card in range(0, round[0] == 0, -1):
                        current_card = round[card][1]
                        if card_value(current_card, top_card) > best_value:
                            best_value = card_value(current_card, top_card)
                            best_card = current_card
                            best_card_position = round[card][0]

                    if best_card_position == team[1]:
                        return 0, sorted_cards[0]
                    return 1, sorted_cards[-1]
                else:
                    return 1, sorted_cards[-1]
        else:
            return 1, sorted_cards[-1]
                    

    # Função para retornar o que você vai dar de resposta a trucos
    def respond(self,top_card,play_hist, score_hist):
        return 0
    
    def sort_cards(self, top_card):
        #Função que ordena as cartas em ordem crescente
        sorted_cards = self.cards.copy()
        for i in range(len(sorted_cards)-1):
            m=i
            for j in range(i+1,len(sorted_cards)):
                if card_value(sorted_cards[m], top_card)>card_value(sorted_cards[j], top_card):
                    m=j
            sorted_cards[m], sorted_cards[i] = sorted_cards[i], sorted_cards[m]
        return sorted_cards
    

# Função que define o nome da dupla:
def pair_name():
    return "Camis"  # Defina aqui o nome da sua dupla


# Função que cria a dupla:
def create_pair():
    return (FirstPlayer(), FirstPlayer())  # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.

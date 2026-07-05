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
        
        - pra saber se tem manilha o card value vai ser maior q 1000
        
        Pensando em cada rodada individualmente agora:
        1° 
            1 a jogar: melhor carta
            2 a jogar: 
                se maior carta > carta jogada -> maior carta
                menor carta
            3 a jogar:
                se maior carta do meu amigo (manilha ou 3) -> truco (*)
                se maior carta (manilha ou 3) > maior carta jogada -> truco, maior carta (**)
                se aumentar -> se estiver ganhando (3) -> aceita
                            -> ganhando (manilha) -> aumenta
                            -> perdendo -> corre
            4 a jogar:
                (*), (**)

                
            Problemas: às vzs entra nuns loops fodidos ???
                       ele ta caindo em respond sendo que nem trucou
                '''


# Jogador que não faz nada. Substitua esta classe para criar as suas, devem herdar da classe Player
class FirstPlayer(Player):
    # Se estiver dúvida sobre como começar olhe os players prontos em basic_players.py e o ReadMe
    def __init__(self):
        super().__init__(0, "Camila", image_path='img/Homer_Simpson.png') # Nome do Jogador

    # Função para retornar o que você vai jogar em determinada mão
    def play(self, top_card, play_hist, score_hist):

        sorted_cards = sort_cards(top_card, self.cards) #lista ordenada
        team = (self.position, (self.position+2)%4)
        current_pos = (len(play_hist[-1])%4)+1 #posicao na rodada atual (rodada = 4 cartas)
        manilha = False

        if card_value(sorted_cards[-1], top_card)>=1000: manilha = True # vê se eu tenho alguma manilha

        if current_pos!=1:
            b_value, b_card, b_position = best_card(current_pos, top_card, play_hist)
            manilha_jogada = False

            if b_value>=1000: manilha_jogada = True

            print('manilha jogada', manilha_jogada)

            if manilha: return 2, sorted_cards[-1]

            print('tenho manilha', manilha)

            if manilha_jogada and b_position == team[1]: #se tiver manilha jogada e for do meu time, eu truco c menor carta
                print('caso trucando qnd manilha no time')
                return 2, sorted_cards[0]

            if current_pos == 4: #se eu for a ultima a jogar
                
                if b_value < card_value(sorted_cards[-1], top_card): #truco e maior carta
                    print('caso truco meu')
                    return 2, sorted_cards[-1]
                
                if b_position == team[1]: #se melhor posicao for meu time, truco c pior carta
                    print('caso truco dupla')
                    return 2, sorted_cards[0]

            if b_position == team[1]: #se melhor carta for do meu time, jogo pior carta p baixo
                print('caso 1')
                print('minha posicao na rodada', current_pos)
                print(play_hist)
                return 0, sorted_cards[0]

            if b_value>card_value(sorted_cards[-1], top_card): #se melhor carta for maior q a minha melhor carta, pior carta p cima
                print('caso 2')
                return 1, sorted_cards[0]
            
        
        print('caso final')
        return 1, sorted_cards[-1]  
    
    # Função para retornar o que você vai dar de resposta a trucos
    def respond(self, top_card, play_hist, score_hist):

        sorted_cards = sort_cards(top_card, self.cards) #lista ordenada
        team = (self.position, (self.position+2)%4)
        current_pos = (len(play_hist[-1])%4)+1 #posicao na rodada atual (rodada = 4 cartas)
        b_value, b_card, b_position = best_card(current_pos, top_card, play_hist)
        manilha = False

        if card_value(sorted_cards[-1], top_card)>=1000: manilha = True # vê se eu tenho alguma manilha

        if manilha:
            print('aumentou truco')
            return 2
        
        if sorted_cards[-1] == '3' or manilha: #se trucar e tiver manilha ou 3, aceita
            print('aceitou')
            return 1
        
        if b_position == team[1]:
            print('melhor carta do time')
            return 1

        return 0

#Função que me retorna a maior carta, valor e posição entre as anteriores a mim
def best_card(current_pos, top_card, play_hist):

    if len(play_hist[-1])>0:
        best_value = card_value(play_hist[-1][-1][1], top_card)
        best_card = play_hist[-1][-1][1]
        best_card_position = play_hist[-1][-1][0]

        for card in range(-1, current_pos*(-1), -1):
            current_card = play_hist[-1][card][1]
            if current_card == None:
                current_pos+=1
            if card_value(current_card, top_card) > best_value:
                best_value = card_value(current_card, top_card)
                best_card = current_card
                best_card_position = play_hist[-1][card][0]

        return best_value, best_card, best_card_position

#Função que ordena as cartas em ordem crescente
def sort_cards(top_card, cards):
    
    sorted_cards = cards.copy()
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

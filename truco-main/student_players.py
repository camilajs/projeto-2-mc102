from basic_players import Player
from judge import card_value

# Implemente neste arquivo seus jogadores para Truco

# Jogador que não faz nada. Substitua esta classe para criar as suas, devem herdar da classe Player
class Guerreira(Player):
    # Se estiver dúvida sobre como começar olhe os players prontos em basic_players.py e o ReadMe
    def __init__(self):
        super().__init__(0, "Rumi", image_path='img/none.jpg') # Nome do Jogador

    # Função para retornar o que você vai jogar em determinada mão
    def play(self, top_card, play_hist, score_hist):

        sorted_cards = sort_cards(top_card, self.cards)
        team = (self.position, (self.position+2)%4)
        current_pos = posicao_atual(play_hist) 
        manilha = card_value(sorted_cards[-1], top_card)>=1000 

        can_truco = score_hist[-1][1] < 12

        # Se não for o primeiro a jogar
        if current_pos!=1:

            b_value, b_position = best_card(current_pos, top_card, play_hist)
            menor_carta_p_ganhar = menor_p_vencer(sorted_cards, top_card, b_value)

            # Não estou ganhando a rodada
            if b_position not in team:

                # Realmente não tenho como ganhar
                if menor_carta_p_ganhar is None:
                    return 0, sorted_cards[0]

                # Se tenho manilha ou sou o último da rodada: truco ou aumento se puder
                if (manilha or current_pos == 4):

                    if len(self.cards) == 1:
                        can_truco = False # -> considero que já truquei
                        return (2 if manilha and can_truco else 1), sorted_cards[-1]
                    
                    # Truca se tiver manilha e cartas boas, senão joga normal
                    if sorted_cards[-2][0] in ('3', '2', 'A'):
                        can_truco = False
                        return (2 if manilha and can_truco else 1), menor_carta_p_ganhar          
                    
                return 1, menor_carta_p_ganhar

            # Se nada se aplicar, jogo a menor carta virada
            return 0, sorted_cards[0]
        
        # Se estiver na segunda rodada
        if len(self.cards) == 2:

            lost_first_round = lost_round(play_hist, top_card, team)

            # Se não tiver perdido o primeiro round e tiver manilha: truco com manilha
            if not lost_first_round and manilha and can_truco:
                return 2, sorted_cards[-1]

        # Se nada se aplicar, sou o primeiro a jogar, então vou jogar a maior carta normal        
        return 1, sorted_cards[-1]  
    
    # Função para retornar o que você vai dar de resposta a trucos
    def respond(self, top_card, play_hist, score_hist):

        # Caso mão vazia
        if not self.cards:
            return 1

        sorted_cards = sort_cards(top_card, self.cards) #lista ordenada
        team = (self.position, (self.position+2)%4)
        current_pos = posicao_atual(play_hist)
        b_value, b_position = best_card(current_pos, top_card, play_hist)
        manilha = card_value(sorted_cards[-1], top_card) >= 1000
        can_truco = score_hist[-1][1] < 12

        #Placar atual
        score = score_hist[-1][0] if score_hist else [0, 0]
        my_team = self.position % 2
        enemy_team = 1 - my_team

        # Se o adversário está perto de vencer, evita aumentar o truco
        if score[enemy_team] >= 11:
            if manilha or sorted_cards[-1][0] == '3':
                return 1
            return 0

        # Tenho manilha: aumento se tiver pelo menos uma carta boa além da manilha
        if manilha:
            if len(self.cards) > 1:
                if sorted_cards[-2][0] in ('3', '2', 'A') and can_truco:
                    return 2
            # Senão, só aceito
            return 1
    
        # Tenho um 3: aceito
        if sorted_cards[-1][0] == '3':
            return 1

        # Meu parceiro está ganhando a rodada
        if b_position in team:
            return 1

        # Caso contrário, corro
        return 0

#Verifica se eu perdi o primeiro round
def lost_round(play_hist, top_card, team):
    
    highest_value = card_value(play_hist[-1][0][1], top_card)
    highest_pos = play_hist[-1][0][0]
    
    if len(play_hist[-1]) > 0:

        for pos, card, _ in play_hist[-1]:
            if card_value(card, top_card) > highest_value:
                highest_value = card_value(card, top_card)
                highest_pos = pos

    return highest_pos not in team


# Retorna a menor carta capaz de vencer a carta adversária.
# Se nenhuma vencer, retorna None.
def menor_p_vencer(sorted_cards, top_card, target_value):

    for card in sorted_cards:
        if card_value(card, top_card) > target_value:
            return card

    return None


#Função que me retorna o maior valor e posição entre as anteriores a mim
def best_card(current_pos, top_card, play_hist):

    best_value = 0
    best_card_position = None

    if len(play_hist[-1]) > 0:

        for card in range(-1, current_pos*(-1), -1):

            current_card = play_hist[-1][card][1]

            # Ignora pedidos de truco e respostas
            if current_card is None:
                current_pos+=1

            current_value = card_value(current_card, top_card)

            if current_value > best_value:
                best_value = current_value
                best_card_position = play_hist[-1][card][0]

    return best_value, best_card_position
    

# Função que retorna minha posição na rodada (1º, 2º, 3º ou 4º a jogar).
# O play_hist também guarda pedidos de truco e respostas (carta = None),
# então contamos apenas as jogadas que possuem carta.
def posicao_atual(play_hist):

    if not play_hist or len(play_hist[-1]) == 0:
        return 1

    cartas = 0

    for jogada in play_hist[-1]:
        if jogada[1] is not None:
            cartas += 1

    return (cartas % 4) + 1


#Função que ordena as cartas em ordem crescente
def sort_cards(top_card, cards):
    
    sorted_cards = cards.copy()
    for i in range(len(sorted_cards)-1):
        m=i
        for j in range(i+1,len(sorted_cards)):
            if card_value(sorted_cards[m], top_card) > card_value(sorted_cards[j], top_card):
                m=j
        sorted_cards[m], sorted_cards[i] = sorted_cards[i], sorted_cards[m]
    return sorted_cards
    

# Função que define o nome da dupla:
def pair_name():
    return "Guerreiras do kpop"  # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (Guerreira(), Guerreira())  # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.

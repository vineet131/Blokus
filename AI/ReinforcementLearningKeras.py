from AI.ReinforcementLearningModelKeras import TDN
from blokus import PygameClass
import constants, board, pieces, player, drawElements
import os, copy, numpy as np, tensorflow as tf, matplotlib.pyplot as plt
from tqdm import tqdm
plt.style.use('dark_background')

N_EPISODES = 2000
RENDER_EVERY = N_EPISODES + 1 #Needs some investigation

"""if not os.path.exists('models'):
    os.makedirs('models')
MODEL_SAVE_FOLDER = os.getcwd()
MODEL_SAVE_FILE = os.path('models')"""

def simulation_loop(player_init_params, lr=0.001, epsilon=1, model_name=None):
    #pgc = PygameClass(player_init_params, False)
    tdnet = TDN(lr, epsilon, model_name)
    winner_list = {"1": 0, "2": 0, "Tie": 0}
    losses = []

    for ep in tqdm(range(N_EPISODES), ascii=True, unit="Episodes"):
        game_over = False
        is_render = False
        if ep % RENDER_EVERY == 0 and ep != 0:
            is_render = True
    
        pgc = PygameClass(player_init_params, is_render)
        #initialise e (trace) and other parameters
        trace = 0
        reward = 0
        delta = 0
        V = 0
        V_next = 0
        model_lambda = 0.7
        alpha = tdnet.model.optimizer._hyper["learning_rate"]
        
        # Made the redundant passing to player1 & player2 first
        # and then to active_player & opponent for clarity/legibility
        active_player, opponent = pgc.player1, pgc.player2
        if is_render:
            drawElements.init_piece_rects(pgc.player1.remaining_pieces,\
                                          pgc.player2.remaining_pieces)
        while not game_over:
            #Get action to be taken either randomly or based on policy
            current_move = tdnet.explore_or_exploit(pgc.gameboard, active_player, opponent)
            current_state = copy.copy(pgc.gameboard.board)
            V = tdnet.predict_model(current_state)

            #Take action
            if current_move is not None:
                pgc.gameboard.fit_piece(current_move, active_player, opponent)

            #Observe next state after taking action
            new_state = copy.copy(pgc.gameboard.board)

            #Observe reward if final state has been reached
            if board.is_game_over(pgc.gameboard, pgc.player1, pgc.player2):
                game_over = True
                winner = board.check_higher_score(pgc.player1, pgc.player2)
                #We assign the rule that if player 1 wins, we push the V function
                #closer to 0 and if player 2 wins we push it closer to 1
                if winner == pgc.player1:   V_next = 0
                elif winner == pgc.player2: V_next = 1
                else:                       V_next = 0.5 #In case of a draw
            else:
                #Calculate V_next to be inputted into delta
                V_next = tdnet.predict_model(new_state)

            #Find delta (the Temporal Difference error)
            delta = tf.reduce_sum(V_next - V)

            #Update the vector of eligibility traces
            trainable_vars = tdnet.get_weights()
            grads = tdnet.get_gradients(current_state, V, trainable_vars)

            updated_traces = []
            for grad in grads:
                trace = tf.Variable(tf.zeros(grad.get_shape()), trainable=False)
                #Eligibility trace decayed by lambda: e_t = lambda * e_t-1 + dV_t/dTheta_t
                trace_op = ((model_lambda * trace) + grad)

                # grad with trace theta_t+1 - theta_t = alpha * delta_t * e_t
                grad_trace = alpha * delta * trace_op

                updated_traces.append(grad_trace)

            #Update the parameter vector theta_t+1 <- theta_t + (alpha * delta_t * trace_t)
            tdnet.model.optimizer.apply_gradients(zip(updated_traces, trainable_vars))
            #tdnet.model.compiled_metrics.update_state(y, y_pred)
            #tdnet.train_model(next_state, V_next)

            active_player, opponent = player.switch_active_player(active_player, opponent)
            if is_render:
                # Set the screen background
                pgc.screen.fill(constants.BLACK)
        
                drawElements.draw_infobox(pgc.background, pgc.player1, pgc.player2)
                drawElements.draw_pieces(pgc.background, pgc.player1, pgc.player2, active_player, pgc.selected)
                drawElements.draw_gameboard(pgc.background, pgc.board_rects, pgc.gameboard, None, active_player)
                pgc.screen.blit(pgc.background, (0,0))
        
                # Limit to 60 frames per second
                pgc.clock.tick(60)
 
                # Update the screen with what is drawn.
                pygame.display.update()
        history = tdnet.train_model(new_state, V_next)
        pgc = None
        if winner is not None:
            winner_list[str(winner.number)] +=1
        else:
            winner_list["Tie"] += 1
        losses.append(history.history["loss"][0])
    plt.figure()
    plt.subplot(1,2,1)
    plt.xlabel("Winner")
    plt.ylabel("Number of wins")
    plt.title("Wins vs no of episodes")
    plt.bar(winner_list.keys(), winner_list.values())
    plt.subplot(1,2,2)
    plt.xlabel("Episode #")
    plt.ylabel("Loss")
    plt.title("Loss vs episodes")
    plt.plot(losses, marker='o')
    plt.savefig("winner_vs_wins__losses_per_episode.png")
    tdnet.save_model(model_name)

def train():
    player_init_params = {"p1" : {"is_ai" : True, "color" : constants.PURPLE, "name_if_ai" : "RandomMovesBot",
                                  "ai_class": None},
                          "p2" : {"is_ai" : True, "color" : constants.ORANGE, "name_if_ai" : "RandomMovesBot",
                                  "ai_class": None}}
    simulation_loop(player_init_params, model_name="test.pb", epsilon=0.99)

def test():
    player_init_params = {"p1" : {"is_ai" : True, "color" : constants.PURPLE, "name_if_ai" : "RandomMovesBot",
                                  "ai_class": None},
                          "p2" : {"is_ai" : True, "color" : constants.ORANGE, "name_if_ai" : "RandomMovesBot",
                                  "ai_class": None}}
    simulation_loop(player_init_params, epsilon=0.1)

if __name__ == "__main__":
    constants.VERBOSITY = 0
    train()
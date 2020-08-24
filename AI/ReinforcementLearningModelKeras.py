#TD Reinforcement Learning using Keras 2.3
import copy, numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from RandomMovesBot.RandomMovesBot import return_random_move
import pieces, constants, board

class TDN:
    def __init__(self, state_shape, lr, epsilon, model_name):
        #state_size = 196 (14x14 - size of the gameboard)
        self.state_shape = state_shape
        self.lr = lr
        self.epsilon = epsilon
        self.epsilon_decay = 0.00005

        # Main model that we train at every step
        self.model = self.create_model()
        if model_name is not None:
            print("Loading weights")
            self.load_model(model_name)
    
    """
    Simple convolutional fully connected network. Takes the board array as input
    and an action with maximum value spit out by the network is selected as output.
    """
    def create_model(self):
        #Input size = 196 (14x14 - size of the gameboard)
        model_input = keras.Input(shape=self.state_shape, name="board_input")

        layer_1 = layers.Dense(128, activation="sigmoid")(model_input)
        layer_2 = layers.Dense(64, activation="sigmoid")(layer_1)
        layer_3 = layers.Dense(50, activation="sigmoid")(layer_2)

        #model_output gives the evaluated value of the inputted board state
        model_output = layers.Dense(1, activation="sigmoid")(layer_3)

        model = keras.Model(model_input, model_output, name="simple_convolution")
        model.compile(loss="mse", optimizer=keras.optimizers.Adam(self.lr), metrics=['accuracy'])
        if constants.VERBOSITY > 1:
            print("Created the model:\n", model.summary())
        return model
    
    def train_model(self, state, V):
        self.model.fit([[state.flatten()]], V, epochs=1)

    def predict_model(self, state):
        return self.model.predict([[state.flatten()]])
    
    def get_weights(self):
        return self.model.trainable_weights
    
    def get_gradients(self):
        return self.model.optimizer.get_gradients(self.model.total_loss, self.get_weights())
    
    def explore_or_exploit(self, gameboard, player, opponent_player):
        chosen_move = None
        random_number = np.random.random()
        if random_number <= self.epsilon:
            self.epsilon -= self.epsilon_decay
            chosen_move = return_random_move(gameboard, player)
            if constants.VERBOSITY > 1: print("Epsilon value is now", self.epsilon)
            if constants.VERBOSITY > 0: print("Chose to explore")
        else:
            best_score = constants.M_INFINITY
            for move in board.return_all_pending_moves(gameboard, player):
                board_copy = copy.deepcopy(gameboard)
                player_copy = copy.deepcopy(player)
                opponent_copy = copy.deepcopy(opponent_player)
                if board_copy.fit_piece(move, player_copy, opponent_copy):
                    score = self.predict_model(board_copy.board)
                    if score > best_score:
                        best_score = score
                        chosen_move = move
            if constants.VERBOSITY > 0: print("Chose to exploit")
        return chosen_move
    
    def save_model(self, name):
        self.model.save_weights(name)
    
    def load_model(self, name):
        self.model.load_weights(name)
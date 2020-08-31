#TD Reinforcement Learning using Keras 2.3
import copy, numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from RandomMovesBot.RandomMovesBot import return_random_move
import pieces, constants, board

class CustomModel(keras.Model):
    def train_step(self, data):
        # Unpack the data. Its structure depends on your model and
        # on what you pass to `fit()`.
        x, y = data

        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)  # Forward pass
            # Compute the loss value
            # (the loss function is configured in `compile()`)
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)
        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)
        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}

class TDN:
    def __init__(self, lr = 0.001, epsilon = 0, model_name = None):
        #state_shape = 196 (14x14 - size of the gameboard)
        self.state_shape = (constants.ROW_COUNT * constants.COLUMN_COUNT,)
        self.lr = lr
        self.epsilon = epsilon
        self.epsilon_decay = 0.00005

        # Main model that we train at every step
        self.loss_fn = keras.losses.MeanSquaredError()
        self.model = self.create_model()
        self.model_checkpoint_callback = None
        if model_name is not None:
            print("Loading weights")
            self.load_model(model_name)
            self.model_checkpoint_callback = keras.callbacks.ModelCheckpoint(model_name)
    
    """
    Simple convolutional fully connected network. Takes the board array as input
    and an action with maximum value spit out by the network is selected as output.
    """
    def create_model(self):
        #Input size = 196 (14x14 - size of the gameboard)
        model_input = keras.Input(shape=self.state_shape, name="board_input")

        layer_1 = layers.Dense(128, activation="sigmoid")(model_input)
        layer_2 = layers.Dense(100, activation="sigmoid")(layer_1)
        layer_3 = layers.Dense(50, activation="sigmoid")(layer_2)

        #model_output gives the evaluated value of the inputted board state
        model_output = layers.Dense(1, activation="sigmoid")(layer_3)

        #model = CustomModel(model_input, model_output, name="simple_convolution")
        model = keras.Model(model_input, model_output, name="simple_convolution")
        model.compile(loss=self.loss_fn, optimizer=keras.optimizers.Adam(self.lr))
        if constants.VERBOSITY > 1:
            print("Created the model:\n%s" % (model.summary()))
        return model
    
    def train_model(self, state, V):
        state = np.reshape(state, (1,196))
        V = np.array([[V]])
        if self.model_checkpoint_callback is not None:
            return self.model.fit(state, V, epochs=1, callbacks=[self.model_checkpoint_callback])
        else:
            return self.model.fit(state, V, epochs=1)

    def predict_model(self, state):
        return self.model.predict(np.reshape(state, (1,196)))
    
    def get_weights(self):
        return self.model.trainable_weights
    
    def get_gradients(self, state, V, trainable_vars):
        with tf.GradientTape() as tape:
            V_pred = self.model(np.reshape(state, (1, 196)), training=True)
            loss_value = self.loss_fn(V, V_pred)
        return tape.gradient(loss_value, trainable_vars)
    
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
            verb = constants.VERBOSITY
            constants.VERBOSITY = 0
            for move in board.return_all_pending_moves(gameboard, player):
                if gameboard.fit_piece(move, player, opponent_player, mode="ai"):
                    score = self.predict_model(gameboard.board)
                    if score > best_score:
                        best_score = score
                        chosen_move = move
                    gameboard.unfit_last_piece(player, opponent_player)
            constants.VERBOSITY = verb
            if constants.VERBOSITY > 0: print("Chose to exploit")
        return chosen_move
    
    def save_model(self, name):
        self.model.save_weights(name)
    
    def load_model(self, name):
        self.model.load_weights(name)
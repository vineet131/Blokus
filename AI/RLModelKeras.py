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
            try:
                self.load_model_weights(model_name)
                print("Loaded model weights")
                self.model_checkpoint_callback = keras.callbacks.ModelCheckpoint(model_name)
            except:
                print("Model name exists but couldn't find model in the folder. Using initial random weights")
    
    """
    Simple convolutional fully connected network. Takes the board array as input
    and an action with maximum value spit out by the network is selected as output.
    """
    def create_model(self):
        #Input explanation:
        #-392 units (196 for black and 196 for white) representing binarily whether player's piece is present at that board position
        #-2 units for the score of each side
        #-2 units for a binray representation of whose turn it is
        #Total - 396 input units
        model_input = keras.Input(shape=(396,), name="board_input")

        layer_1 = layers.Dense(256, activation="sigmoid")(model_input)
        layer_2 = layers.Dense(75, activation="sigmoid")(layer_1)

        #model_output gives the evaluated value of the inputted board state
        model_output = layers.Dense(1, activation="sigmoid")(layer_2)

        #model = CustomModel(model_input, model_output, name="simple_convolution")
        model = keras.Model(model_input, model_output, name="simple_convolution")
        model.compile(loss=self.loss_fn, optimizer=keras.optimizers.Adam(self.lr))
        if constants.VERBOSITY > 1:
            print("Created the model:\n%s" % (model.summary()))
        return model
    
    def generate_model_input(self, state, score_p1, score_p2, current_turn):
        final_arr = []
        p1 = np.where(state == 1, 1, 0)
        p2 = np.where(state == 2, 1, 0)
        if current_turn == 1:
            turn_arr = np.array([1, 0])
        else:
            turn_arr = np.array([0, 1])
            temp = p1
            p1 = p2
            p2 = temp
        for element in [[score_p1/88, score_p2/88], turn_arr, p1.flatten(), p2.flatten()]:
            final_arr.extend(element)
        return np.reshape(final_arr, (1,396))
    
    def train_model(self, state, V, score_p1, score_p2, current_turn):
        final_arr = self.generate_model_input(state, score_p1, score_p2, current_turn)
        V = np.array([[V]])
        
        if self.model_checkpoint_callback is not None:
            return self.model.fit(final_arr, V, epochs=1, batch_size=None, callbacks=[self.model_checkpoint_callback])
        else:
            return self.model.fit(final_arr, V, epochs=1, batch_size=None)

    def predict_model(self, state, score_p1, score_p2, current_turn):
        final_arr = self.generate_model_input(state, score_p1, score_p2, current_turn)
        return self.model.predict(final_arr)
    
    def get_weights(self):
        return self.model.trainable_weights
    
    def get_gradients(self, state, score_p1, score_p2, current_turn, V):
        trainable_vars = self.get_weights()
        final_arr = self.generate_model_input(state, score_p1, score_p2, current_turn)
        with tf.GradientTape() as tape:
            V_pred = self.model(final_arr, training=True)
            loss_value = self.loss_fn(V, V_pred)
            #loss_value += sum(self.model.losses)
        return tape.gradient(loss_value, trainable_vars), loss_value, V_pred
    
    def get_temporal_difference(self, V_next, V, grads, model_lambda, alpha):
        trainable_vars = self.get_weights()
        #Find delta (the Temporal Difference error)
        delta = tf.reduce_sum(V_next - V)

        updated_traces = []
        for grad in grads:
            trace = tf.Variable(tf.zeros(grad.get_shape()), trainable=False)
            #Eligibility trace decayed by lambda: e_t = lambda * e_t-1 + dV_t/dTheta_t
            trace_op = ((model_lambda * trace) + grad)

            # grad with trace theta_t+1 - theta_t = alpha * delta_t * e_t
            grad_trace = alpha * delta * trace_op

            updated_traces.append(grad_trace)

        #Update the parameter vector theta_t+1 <- theta_t + (alpha * delta_t * trace_t)
        self.model.optimizer.apply_gradients(zip(updated_traces, trainable_vars))
    
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
                    score = self.predict_model(gameboard.board, player.score, opponent_player.score, player.number)
                    if score > best_score:
                        best_score = score
                        chosen_move = move
                    gameboard.unfit_last_piece(player, opponent_player)
            constants.VERBOSITY = verb
            if constants.VERBOSITY > 0: print("Chose to exploit")
        return chosen_move
    
    def save_model_weights(self, name):
        self.model.save_weights(name)
    
    def load_model_weights(self, name):
        self.model.load_weights(name)
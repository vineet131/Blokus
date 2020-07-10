#Deep Q-Learning using Keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
#from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import numpy as np

#There are 21*2 pieces for both players, so maximum of 42 moves can be made
#We randomly choose the last n moves made by both players leading upto the result
REPLAY_MEMORY_SIZE = 42

class DQN:
    def __init__(self, state_size):
        # Main model that we train at every step
        self.model = self.create_model()

        # Target network that we predict at every step
        self.target_model = self.create_model(state_size)
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # Custom tensorboard object
        #self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0
        
        self.epsilon = 0.5
    
    def create_model(self, state_size):
        #model = Sequential()
        #model.add(Conv2D(256, (3, 3), input_shape=state_size)) #state_size=196x1 for the 14x14 gameboard
        
        #Toy resnet model
        inputs = keras.Input(shape=state_size, name="img")
        x = layers.Conv2D(32, 3, activation="relu")(inputs)
        x = layers.Conv2D(64, 3, activation="relu")(x)
        block_1_output = layers.MaxPooling2D(3)(x)

        x = layers.Conv2D(64, 3, activation="relu", padding="same")(block_1_output)
        x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
        block_2_output = layers.add([x, block_1_output])

        x = layers.Conv2D(64, 3, activation="relu", padding="same")(block_2_output)
        x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
        block_3_output = layers.add([x, block_2_output])

        x = layers.Conv2D(64, 3, activation="relu")(block_3_output)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation="relu")(x)
        x = layers.Dropout(0.5)(x)
        #Linear activation for direct correlation between state space and action space
        output1 = layers.Dense(action_size_1, activation="linear")(x)
        output2 = layers.Dense(action_size_2, activation="linear")(x)

        model = keras.Model(inputs, [output1, output2], name="toy_resnet")
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model
    
    def train_model(self):
        self.model.fit(np.array(X)/255, np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False, callbacks=[self.tensorboard] if terminal_state else None)
    
    def remember(self, state, action, reward, next_state, done = False):
        self.replay_memory.append((state, action, reward, next_state, done))
    
    def explore_or_exploit(self, state):
        if np.random.rand() <= self.epsilon:
            return None
        piece, place_on_board_at = self.model.predict(state)
        return [np.argmax(piece), np.argmax(place_on_board_at)]
    
    def replay(self, batch_size):
        minibatch = self.replay_memory[np.random.randint(batch_size):]
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + GAMMA * np.amax(self.model.predict(next_state)[0])
            target_future = self.model.predict(state)
            target_future[0][action] = target
            
            self.model.fit(state, target_future, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self, name):
        self.model.save_weights(name)
    
    def load_model(self, name):
        self.model.load_weights(name)
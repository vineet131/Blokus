import torch, torch.nn as nn, torch.nn.functional as F, torch.optim as optim
import constants

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#TDN = Temporal Difference Network
class TDNModel(nn.Module):
    def __init__(self, model_name = None):
        super(TDN, self).__init__()
        self.model_name = model_name
        self.input_shape = (constants.ROW_COUNT * constants.COLUMN_COUNT)
        self.input_layer = nn.Linear(self.input_shape, 192)
        self.fc1 = nn.Linear(192, 100)
        self.output_layer = nn.Linear(100, 1)
    
    def forward(self, x):
        x = self.input_layer(x)
        x = F.sigmoid(x)

        x = self.fc1(x)
        x = F.sigmoid(x)

        x = self.output_layer(x)
        output = F.sigmoid(x)
        return output

class TDN:
    def __init__(self, model_name = None):
        self.model = TDNModel(model_name)
        self.lr = 0.001
        self.loss = nn.MSELoss()
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr, momentum=0.9)
    
    def save_model(self, path):
        #path = "entire_model.pt"
        torch.save(self.model, path)

    def load_model(self, path):
        self.model = torch.load(path)
        self.model.eval()

    def save_checkpoint(self, path):
        #Saving checkpoints
        # Additional information
        EPOCH = 5
        #PATH = "model.pt"
        LOSS = 0.4

        torch.save({
            'epoch': EPOCH,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': LOSS,
            }, PATH)

    def load_checkpoint(self, path):
        #Loading checkpoints
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        loss = checkpoint['loss']

        self.model.eval()
        # - or -
        #model.train()
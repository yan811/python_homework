import torch.nn as nn
#lstm
class lstm(nn.Module):
    def __init__(self, chars_len, hidden_dim, layer_num):
        super(lstm, self).__init__()
        self.chars_len = chars_len
        embedding_dim = 100
        self.hidden_dim = hidden_dim
        self.layer_num = layer_num

        self.embedding = nn.Embedding(chars_len, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=layer_num)
        self.linear = nn.Sequential(nn.Dropout(0.2), nn.Linear(hidden_dim, 4))
        

    def forward(self, x): 
        #print ('x0',x.shape)
        x = self.embedding(x)
        x = x.view(len(x), 1, -1)
        #print ('x1',x)
        x = self.lstm(x)[0]
        #print ('x2',len(x))
        #x = np.array(x,dtype=float)
        out = self.linear(x)
        
        #print('out',out.shape)
        return out

import torch
import torch.nn as nn
import random
import numpy as np
import matplotlib.pyplot as plt
import itertools
from hw3_utils import vocab


DEBUG = False


class NameGenerator(nn.Module):
    def __init__(self,
            input_vocab_size,
            n_embedding_dims,
            n_hidden_dims,
            n_lstm_layers,
            output_vocab_size):
        """
        Initialize our name generator, following the
        equations laid out in the assignment. In other words,
        we'll need an Embedding layer, an LSTM layer, a
        Linear layer, and LogSoftmax layer.

        Note:
        Remember to set batch_first=True when initializing your LSTM layer!

        Also note: When you build your LogSoftmax layer,
        pay attention to the dimension that you're
        telling it to run over!
        """
        super(NameGenerator, self).__init__()
        self.lstm_dims = n_hidden_dims
        self.lstm_layers = n_lstm_layers

        self.input_lookup = nn.Embedding(
                num_embeddings=input_vocab_size,
                embedding_dim=n_embedding_dims)

        self.lstm = nn.LSTM(
                input_size=n_embedding_dims,
                hidden_size=n_hidden_dims,
                num_layers=n_lstm_layers,
                batch_first=True)

        self.output = nn.Linear(
                in_features=n_hidden_dims,
                out_features=output_vocab_size)

        self.softmax = nn.LogSoftmax(dim=2)


    def forward(self, history_tensor, prev_hidden_state):
        """
        Given a history, and a previous timepoint's
        hidden state, predict the next character.

        Note: Make sure to return the LSTM hidden
        state, so that we can use this for
        sampling/generation in a one-character-at-
        a-time pattern, as in Goldberg 9.5!
        """
        n = history_tensor.shape[1]

        input = self.input_lookup(history_tensor)

        h_output, (hn,cn) = self.lstm(input, prev_hidden_state)

        output = self.output(h_output)

        #if DEBUG:
        #    print(history_tensor.shape)
        #    print(input.shape)
        #    print(h_output.shape)
        #    print(hn.shape)
        #    print(cn.shape)
        #    print(output.shape)

        return self.softmax(output), (hn,cn)

    def init_hidden(self):
        """
        Generate a blank initial history value, for use
        when we start predicting over a fresh sequence.
        """
        h_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)
        c_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)

        # was this supposed to be here?:
        return (h_0,c_0)

### Utility functions

def train(model, epochs, training_data, c2i):
    """
    Train model for the specified number of epochs,
    over the provided training data.

    Make sure to shuffle the training data at the
    beginning of each epoch!
    """
    opt = torch.optim.Adam(model.parameters())

    loss_func = torch.nn.NLLLoss()

    loss_batch_size = 100

    for epoch in range(epochs):
        random.shuffle(training_data)
        #loss = 0

        for i, sntnce in enumerate(training_data):

            if i % loss_batch_size == 0:
                opt.zero_grad()

            x_tnsr = vocab.sentence_to_tensor(sntnce[:-1], c2i)

            y_hat, _ = model(x_tnsr, model.init_hidden())
                    #(torch.randn(model.lstm_layers, 1, model.lstm_dims),
                    #torch.randn(model.lstm_layers, 1, model.lstm_dims)))

            y_tnsr = torch.tensor(c2i[sntnce[-1]])

            #y_hat = y_hat[0,-1].unsqueeze(0)
            #print(y_hat.shape, y_tnsr.unsqueeze(0).shape)
            loss = loss_func(y_hat[0,-1].unsqueeze(0), y_tnsr.unsqueeze(0))
            #loss += loss_func(y_hat[0,-1].unsqueeze(0), y_tnsr.unsqueeze(0))

            if i % 8000 == 0:
                print(f"{i}/{len(training_data)} average per-item loss: {loss / len(sntnce) - 1}")

            #if i % loss_batch_size == 0 and i > 0:
            # send back gradients:
            # retain graph because error message told me to
            loss.backward(retain_graph=True)
            # now, tell the optimizer to update our weights:
            opt.step()
                #loss = 0

        # now one last time:
        loss.backward(retain_graph=True)
        opt.step()

    return model


def sample(model, c2i, i2c, max_seq_len=200):
    """
    Sample a new sequence from model.

    The length of the resulting sequence should be < max_seq_len, and the
    new sequence should be stripped of <bos>/<eos> symbols if necessary.
    """
    raise NotImplementedError


def compute_prob(model, sentence, c2i):
    """
    Compute the negative log probability of p(sentence)

    Equivalent to equation 3.3 in Jurafsky & Martin.
    """

    nll = nn.NLLLoss(reduction='sum')

    with torch.no_grad():
        s_tens = vocab.sentence_to_tensor(sentence, c2i, True)
        x = s_tens[:,:-1]
        y = s_tens[:,1:]
        y_hat, _ = model(x, model.init_hidden())
        return nll(y_hat.squeeze(), y.squeeze()).item() # get rid of first dimension of each

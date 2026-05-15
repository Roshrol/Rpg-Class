import torch
import pandas as pd
import pickle
import numpy as np

class DataPrepPipeline:
  #before training we prepared the data
  def __init__(self):

    self.feature_cols = ["Strength", "Intelligence", "Willpower", "Agility", "Speed",
                         "Endurance", "Personality", "Luck",
                         "Armorer",  "Athletics", "Blade", "Block", "Blunt", "Hand to Hand", "Heavy Armor",
                         "Alchemy", "Alteration", "Conjuration", "Destruction", "Illusion", "Mysticism",
                         "Restoration", "Acrobatics", "Light Armor", "Marksman", "Mercantile", "Security",
                         "Sneak", "Speechcraft"]
    #standard deviation and average used for normalization
    self.mean = None
    self.std = None

    #converting class names to numbers using a dictionary
    self.class_type = {}

  #learning stats from our training data
  def fit(self, X_df, y_df):
    self.mean = X_df[self.feature_cols].mean()
    self.std = X_df[self.feature_cols].std()

    classes = y_df.unique()
    for i, c in enumerate(classes):
        self.class_type[c] = i

  #normalizing our features and converting to a pytorch tensor
  def transform(self, X_df):
    X = (X_df[self.feature_cols] - self.mean) / (self.std + 1e-8)
    return torch.tensor(X.values, dtype=torch.float32)

  #coverting the class labels to int labels
  def transform_labels(self, y_df):
    y = [self.class_type[c] for c in y_df]
    return torch.tensor(y, dtype=torch.long) # made it long instead of a float

#our multiclass cross entropy loss function
def cross_entropy_loss(q, y):
  return torch.nn.functional.cross_entropy(q, y)

#multiclass logistic regression
class RPG_Model:
    def __init__(self, input_dim, num_classes):
      #our weights should be features x classes I think
      self.W = torch.randn(input_dim, num_classes, requires_grad=True) #grad as in will need to be applied to the gradient
      self.b = torch.zeros(num_classes, requires_grad=True)

    def forward(self, X):
      return X @ self.W + self.b

    def predict(self, X):
      q = self.forward(X)
      return torch.argmax(q, dim=1)


class GradientDescentOptimizer:
    def __init__(self, model, lr = 0.01):
        self.model = model
        self.lr = lr

    def step(self):
        self.model.W.data -= self.lr * self.model.W.grad
        self.model.b.data -= self.lr * self.model.b.grad

        self.model.W.grad.zero_()
        self.model.b.grad.zero_()

#mesures prediction accuracy
def accuracy(model, X, y):
  pred = model.predict(X)
  return (pred == y).float().mean()

#Main function goes below
if __name__ == "__main__":
    # Load the data
    url = "https://raw.githubusercontent.com/Roshrol/Rpg-Class/refs/heads/main/data/oblivion_characters.csv"
    train = pd.read_csv(url)

    # remove broken rows
    train = train.dropna()

    # remove scraped values
    train = train[
        (train.select_dtypes(include=[np.number]) < 300).all(axis=1)
    ]

    # remove rows where all skills are 0
    skill_cols = [
        "Armorer", "Athletics", "Blade", "Block", "Blunt",
        "Hand to Hand", "Heavy Armor", "Alchemy", "Alteration",
        "Conjuration", "Destruction", "Illusion", "Mysticism",
        "Restoration", "Acrobatics", "Light Armor", "Marksman",
        "Mercantile", "Security", "Sneak", "Speechcraft"
    ]

    train = train[(train[skill_cols].sum(axis=1) > 0)]
    # Randomly sample 80% of the rows to be the training set
    train_ix = train.sample(frac=0.8, random_state=42).index
    test_ix = train.drop(train_ix).index

    # separate the features and targets
    X_df = train.drop(columns=["class", "url"])
    y_df = train["class"]

    # fit and save the data prep pipeline
    pipeline = DataPrepPipeline()
    pipeline.fit(X_df.loc[train_ix], y_df.loc[train_ix])

    X_train = pipeline.transform(X_df.loc[train_ix])
    y_train = pipeline.transform_labels(y_df.loc[train_ix])

    # Transform test features using the same stat from training set
    X_test = pipeline.transform(X_df.loc[test_ix])
    y_test = pipeline.transform_labels(y_df.loc[test_ix])

    num_classes = len(set(y_df))
    model = RPG_Model(X_train.shape[1], num_classes)
    opt = GradientDescentOptimizer(model, lr=0.01)

    losses = []

    #training loop
    for epoch in range(70000):
        q = model.forward(X_train)
        loss = cross_entropy_loss(q, y_train)

        loss.backward()
        opt.step()

        losses.append(loss.item())

        if epoch % 1000 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    # save the model
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    q = model.forward(X_train)
    final = cross_entropy_loss(q, y_train).item()

    #training accuracy
    acc = accuracy(model, X_train, y_train).item()

    #test accuracy
    test_acc  = accuracy(model, X_test,  y_test).item()

    print("Train loss:", final)
    print("Train accuracy:", acc)
    print("Test accuracy: ", test_acc)

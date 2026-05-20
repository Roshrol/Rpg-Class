import pandas as pd
url = "https://raw.githubusercontent.com/Roshrol/Rpg-Class/refs/heads/main/data/oblivion_characters.csv" #our playwrite info should go here I believe
train = pd.read_csv(url)
train.head()

import torch
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

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

  #converting the class labels to int labels
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
    def __init__(self, model, lr = 0.1):
        self.model = model
        self.lr = lr

    def step(self):
        self.model.W.data -= self.lr * self.model.W.grad
        self.model.b.data -= self.lr * self.model.b.grad

        self.model.W.grad.zero_()
        self.model.b.grad.zero_()

#measures prediction accuracy
def accuracy(model, X, y):
  pred = model.predict(X)
  return (pred == y).float().mean()

def ell_2_regularization(w):
    return torch.mean(w[1:]**2)

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
    opt = GradientDescentOptimizer(model, lr=0.1)
    regularization = 0.01

    losses = []
    train_accs = []
    reg_losses = []

    #training loop
    for epoch in range(30000):
        q = model.forward(X_train)
        data_loss = cross_entropy_loss(q, y_train)
        reg_loss = regularization * ell_2_regularization(model.W)

        loss = data_loss + reg_loss


        loss.backward()
        opt.step()

        losses.append(loss.item())
        train_accs.append(accuracy(model, X_train, y_train).item())
        reg_losses.append(reg_loss.item())

        if epoch % 1000 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    # save the model
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    q = model.forward(X_train)
    train_loss = cross_entropy_loss(q, y_train).item()

    #training accuracy
    acc = accuracy(model, X_train, y_train).item()

    #test accuracy
    test_acc  = accuracy(model, X_test,  y_test).item()
    test_loss = cross_entropy_loss(model.forward(X_test), y_test).item()

    print("Train loss:", train_loss)
    print("Train accuracy:", acc)
    print("Test accuracy: ", test_acc)
    print("Test Loss:", test_loss)


    ig, ax = plt.subplots(1, 2, figsize=(10, 4))

    #Loss comparison
    ax[0].set_title("Train vs Test Loss")
    ax[0].set_ylabel("Loss")

    # Accuracy comparison
    acc_bars = ax[1].bar(
        ["Train Accuracy", "Test Accuracy"],[acc, test_acc])

    ax[1].set_title("Train vs Test Accuracy")
    ax[1].set_ylabel("Accuracy")

    # highlight test accuracy bar
    acc_bars[1].set_color("crimson")
    acc_bars[1].set_alpha(0.8)

    bars = ax[0].bar(["Train Loss", "Test Loss"],[train_loss, test_loss])

    # highlight test loss bar
    bars[1].set_color("crimson")
    bars[1].set_alpha(0.8)

    ax[0].text(1, test_loss, f"{test_loss:.2f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.show()

    # Loss
    fig, ax = plt.subplots()

    ax.plot(losses)
    ax.set_title("Training Loss Over Time")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")

    plt.show()

    fig, ax = plt.subplots()

    ax.plot(reg_losses)
    ax.set_title("Regularization Loss Over Time")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Regularization Loss")

    plt.show()

    # Created a plot that shows strength vs intelligence by class
    plt.figure(figsize=(8,6))
    classes = y_df.unique()

    fig, ax = plt.subplots(figsize=(8,6))
    # Give me only the rows where the class equals i
    for i in classes:
        subset = train[train["class"] == i]

        ax.scatter(
            subset["Strength"],
            subset["Intelligence"],
            label=i,
            alpha=1
        )

    ax.set_title("Strength vs Intelligence by Class")
    ax.set_xlabel("Strength")
    ax.set_ylabel("Intelligence")
    # A few points were getting blocked by legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()

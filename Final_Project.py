{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "machine_shape": "hm",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Roshrol/Rpg-Class/blob/main/Final_Project.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 216
        },
        "id": "IBAYLzsGBuI6",
        "outputId": "2b6f0e11-ad46-4009-e44f-8f8c89c53c62",
        "collapsed": true
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "name 'io' is not defined",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_36171/1407806147.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mcsv_text\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mrequests\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mlink\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtext\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;31m# if you don't care about column names omit names=names and do headers=None instead\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 7\u001b[0;31m \u001b[0mdf\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread_csv\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mStringIO\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcsv_text\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mnames\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mnames\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      8\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      9\u001b[0m \u001b[0mdf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mhead\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mNameError\u001b[0m: name 'io' is not defined"
          ]
        }
      ],
      "source": [
        "import pandas as pd\n",
        "link = \"https://github.com/Roshrol/Rpg-Class/blob/main/Oblivion/scrape_test.py\" #our playwrite info should go here I believe\n",
        "import io\n",
        "import requests\n",
        "csv_text = requests.get(link).text\n",
        "# if you don't care about column names omit names=names and do headers=None instead\n",
        "df = pd.read_csv(io.StringIO(csv_text), names=names)\n",
        "\n",
        "df.head()\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import torch\n",
        "import pandas as pd\n",
        "import pickle\n",
        "import numpy as np\n",
        "#womp womp\n",
        "\n",
        "class DataPrepPipeline:\n",
        "  def __init__(self):\n",
        "    self.feature_cols = [\"Strength\", \"Intelligence\", \"Willpower\", \"Agility\", \"Speed\", \"Endurance\", \"Personality\", \"Luck\"]\n",
        "    self.mean = None\n",
        "    self.std = None\n",
        "    self.class_type = {}\n",
        "\n",
        "  def fit(self, X_df, y_df):\n",
        "      self.mean = X_df[self.feature_cols].mean()\n",
        "      self.std = X_df[self.feature_cols].std()\n",
        "\n",
        "      classes = y_df.unique()\n",
        "      for i, c in enumerate(classes):\n",
        "          self.class_to_idx[c] = i\n",
        "\n",
        "  def transform(self, X_df):\n",
        "      X = (X_df[self.feature_cols] - self.mean) / (self.std + 1e-8)\n",
        "      return torch.tensor(X.values, dtype=torch.float32)\n",
        "\n",
        "  def transform_labels(self, y_df):\n",
        "      y = [self.class_to_idx[c] for c in y_df]\n",
        "      return torch.tensor(y, dtype=torch.long)\n",
        "\n",
        "  def cross_entropy_loss(Q, y):\n",
        "      Q = torch.clamp(Q, min=1e-7)\n",
        "      return -torch.mean(y * torch.log(Q))\n",
        "\n",
        "#multiclass logistic regression I think\n",
        "class RPG_Model:\n",
        "    def __init__(self, input_dim, num_classes):\n",
        "      #our weights should be features x classes I think\n",
        "      self.W = torch.randn(input_dim, num_classes, grad=True) #grad as in will need to be applied to the gradient\n",
        "      self.b = torch.zeros(num_classes, grad=True)\n",
        "\n",
        "    def forward(self, X):\n",
        "      return X @ self.W + self.b\n",
        "\n",
        "    def predict(self, X):\n",
        "      Q = self.forward(X)\n",
        "      return torch.argmax(Q, dim=1)\n",
        "\n",
        "\n",
        "class GradientDescentOptimizer:\n",
        "    def __init__(self, model, lr = 0.1):\n",
        "        self.model = model\n",
        "        self.lr = lr\n",
        "\n",
        "    def step(self):\n",
        "        self.model.W.data -= self.lr * self.model.W.grad\n",
        "        self.model.b.data -= self.lr * self.model.b.grad\n",
        "\n",
        "        self.model.W.grad.zero_()\n",
        "        self.model.b.grad.zero_()\n",
        "\n",
        "def train(model, opt, X, y, epochs=200):\n",
        "  for epoch in range(epochs):\n",
        "    Q = model.forward(X)\n",
        "    loss = cross_entropy_loss(Q, y)\n",
        "    loss.backward()\n",
        "    opt.step()\n",
        "\n",
        "    if epoch % 20 == 0:\n",
        "      print(f\"Epoch {epoch}, Loss: {loss.item()}\")\n",
        "\n",
        "def accuracy(model, X, y):\n",
        "  pred = model.predict(X)\n",
        "  return (pred == y).float().mean()\n",
        "\n",
        "#Main function goes below\n",
        "#hi\n",
        "if __name__ == \"__main__\":\n",
        "    # Load the data\n",
        "    url = \"https://github.com/Roshrol/Rpg-Class/blob/main/Oblivion/scrape_test.py\"\n",
        "    train = pd.read_csv(url)\n",
        "    print(train.columns)\n",
        "\n",
        "    # separate the features and targets\n",
        "    X_df = train.drop(columns=[\"class\"])\n",
        "    y_df = train[\"class\"]\n",
        "\n",
        "    # fit and save the data prep pipeline\n",
        "    pipeline = DataPrepPipeline()\n",
        "    pipeline.fit(X_df, y_df)\n",
        "\n",
        "    X = pipeline.transform(X_df)\n",
        "    y = pipeline.transform_labels(y_df)\n",
        "\n",
        "    # now we can apply the pipeline to the data to get it ready for training the model\n",
        "    X_train = pipeline.transform(X_df)\n",
        "\n",
        "    # train the model\n",
        "    # taken/based from notebook\n",
        "    y_train_df = pd.get_dummies(train[\"genre\"])\n",
        "    y_train = torch.tensor(y_train_df.values, dtype=torch.float32)\n",
        "\n",
        "    model = GenreModel(X_train.shape[1], y_train.shape[1])\n",
        "    opt = GradientDescentOptimizer(model, lr=0.1)\n",
        "\n",
        "    losses = []\n",
        "    for epoch in range(1000):\n",
        "        q = model.forward(X_train)\n",
        "        loss = cross_entropy(q, y_train)\n",
        "        losses.append(loss.item())\n",
        "        opt.step(X_train, y_train)\n",
        "\n",
        "    # save the model\n",
        "    with open(\"model.pkl\", \"wb\") as f:\n",
        "        pickle.dump(model, f)\n",
        "\n",
        "    q = model.forward(X_train)\n",
        "    print(\"Train loss:\", cross_entropy(q, y_train).item())\n",
        "    print(\"Train accuracy:\", accuracy(q, y_train))"
      ],
      "metadata": {
        "id": "XuAdT-6pFfGX",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 382
        },
        "outputId": "1ad7c1b0-3bd7-4c36-ea73-c297190f76f1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "error",
          "ename": "FileNotFoundError",
          "evalue": "[Errno 2] No such file or directory: ''",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_36171/1121992110.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     77\u001b[0m     \u001b[0;31m# Load the data\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     78\u001b[0m     \u001b[0murl\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 79\u001b[0;31m     \u001b[0mtrain\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread_csv\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0murl\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     80\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     81\u001b[0m     \u001b[0;31m# separate the features and targets\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/parsers/readers.py\u001b[0m in \u001b[0;36mread_csv\u001b[0;34m(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)\u001b[0m\n\u001b[1;32m   1024\u001b[0m     \u001b[0mkwds\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mupdate\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mkwds_defaults\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1025\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1026\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0m_read\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfilepath_or_buffer\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mkwds\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1027\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1028\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/parsers/readers.py\u001b[0m in \u001b[0;36m_read\u001b[0;34m(filepath_or_buffer, kwds)\u001b[0m\n\u001b[1;32m    618\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    619\u001b[0m     \u001b[0;31m# Create the parser.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 620\u001b[0;31m     \u001b[0mparser\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mTextFileReader\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfilepath_or_buffer\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwds\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    621\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    622\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0mchunksize\u001b[0m \u001b[0;32mor\u001b[0m \u001b[0miterator\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/parsers/readers.py\u001b[0m in \u001b[0;36m__init__\u001b[0;34m(self, f, engine, **kwds)\u001b[0m\n\u001b[1;32m   1618\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1619\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mhandles\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mIOHandles\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0;32mNone\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1620\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_engine\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_make_engine\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mf\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mengine\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1621\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1622\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mclose\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m->\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/parsers/readers.py\u001b[0m in \u001b[0;36m_make_engine\u001b[0;34m(self, f, engine)\u001b[0m\n\u001b[1;32m   1878\u001b[0m                 \u001b[0;32mif\u001b[0m \u001b[0;34m\"b\"\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mmode\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1879\u001b[0m                     \u001b[0mmode\u001b[0m \u001b[0;34m+=\u001b[0m \u001b[0;34m\"b\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1880\u001b[0;31m             self.handles = get_handle(\n\u001b[0m\u001b[1;32m   1881\u001b[0m                 \u001b[0mf\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1882\u001b[0m                 \u001b[0mmode\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/common.py\u001b[0m in \u001b[0;36mget_handle\u001b[0;34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[0m\n\u001b[1;32m    871\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mioargs\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mencoding\u001b[0m \u001b[0;32mand\u001b[0m \u001b[0;34m\"b\"\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mioargs\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmode\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    872\u001b[0m             \u001b[0;31m# Encoding\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 873\u001b[0;31m             handle = open(\n\u001b[0m\u001b[1;32m    874\u001b[0m                 \u001b[0mhandle\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    875\u001b[0m                 \u001b[0mioargs\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmode\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: ''"
          ]
        }
      ]
    }
  ]
}
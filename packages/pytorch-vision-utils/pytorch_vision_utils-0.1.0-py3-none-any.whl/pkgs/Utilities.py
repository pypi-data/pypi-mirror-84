import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import os

from datetime import datetime
from PIL import Image

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from torch import nn, optim
from torchvision.transforms.functional import to_tensor
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
  
  
def get_timestamp():
  now = datetime.now()
  timestamp = now.strftime("%m-%d-%Y_%M")
  return timestamp


def reload_models(model, model_dir, folder_name, device="cuda"):
  models = []

  print('Reading in models...')
  path = os.path.join(model_dir, folder_name)
  for i, (subdir, dirs, files) in enumerate(os.walk(path)):
    if not files:
      continue

    for f in files:
      print(f'Reading {f}')
      model = model.to(device)
      model.load_state_dict(state_dict=torch.load(subdir+'/'+f)['model_state_dict'])
      models.append(model)

  return models


  
class DataVisualizationUtilities:
    def __init__(self, device=None):
        '''This class contains common data visualization graphs I like to use, using Seaborn.'''
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if not device else device
    
    
    def im_convert(self, tensor, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        '''Converts the image making it possible to plot using `matplotlib`.'''
        image = tensor.clone().detach().numpy()
        image = image.transpose(1, 2, 0)
        image = image * np.array(std) + np.array(mean) # [0, 1] -> [0, 255]
        image = image.clip(0, 1)
        return image


    def display_dataset(self, loader, classes, batch_size=16, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        '''Displays a small portion of the dataset given a dataloader'''
        dataiter = iter(loader)
        images, labels = dataiter.next()
        fig = plt.figure(figsize=(25, 4))

        for idx in np.arange(min(batch_size, 20)):
            ax = fig.add_subplot(2, 10, idx+1, xticks=[], yticks=[])
            plt.imshow(self.im_convert(images[idx], mean=mean, std=std))
            ax.set_title(classes[labels[idx].numpy()])
                
    
    def display_metric_results(self, model, model_name, loader, train_utils, labels=[], cmap="Blues_r", batch_size=16, figsize=(7, 7)):
        '''Displays the classification report along with a heatmap of the confusion matrix'''
        with torch.no_grad():
            y_pred, y_true = train_utils.get_predictions(model, loader)
            
        y_true = torch.tensor(y_true).to(self.device, dtype=torch.long)
        stacked = torch.stack((y_true, y_pred.argmax(dim=1)), dim=1)
        xticks = yticks = labels
        
        print("Classification Report\n")
        print(classification_report(y_true.cpu(), y_pred.argmax(dim=1).cpu()), target_names=xticks)
        print("Confusion Matrix")
        cnf_mat = confusion_matrix(y_true.cpu(), y_pred.argmax(dim=1).cpu())

        # plot
        plt.figure(figsize=figsize)
        sns.heatmap(cnf_mat, xticklabels=xticks, yticklabels=yticks, annot=True, cmap=cmap)
        plt.ylabel('Ground Truth')
        plt.xlabel('Predictions')
        plt.title("Confusion Matrix " + model_name)
        plt.show()  
        
        
    def display_results(self, loss, acc, val_loss, val_acc, title, figsize=(10, 10)):
        '''Displays the running training and validation losses and accuracies'''
        plt.figure(figsize=figsize)
        plt.subplot(2, 1, 1)

        plt.plot(acc, label='Training Accuracy', color='blue')
        plt.plot(val_acc, label='Validation Accuracy', color='lightseagreen')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([0, 1.2])
        plt.title('Training and Validation Accuracy '+ title)

        y_upper_bound = max(max(loss), max(val_loss))
        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss', color='blue')
        plt.plot(val_loss, label='Validation Loss', color='lightseagreen')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, y_upper_bound+y_upper_bound*0.2])
        plt.title('Training and Validation Loss '+ title)
        plt.xlabel('epoch')
        plt.show() 


class TrainingUtilities:
    '''This class contains common training functions and methodologies I use when working with PyTorch'''
    def __init__(self, data_dir, model=None, device=None):
        self.model = model
        self.data_dir = data_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if not device else device

    
    def loader(self, dataset, batch_size=16, shuffle=True):
        '''Creates the dataloader'''
        return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    

    def to_categorical(self, labels):
        '''Converts the labels from names to integers'''
        labels = np.array(labels)
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(labels)
        
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        return onehot_encoder.fit_transform(integer_encoded)
        
    
    def split_data_and_create_folds(self, n_splits=5, input_size=(299, 299)):
        '''Loads the images and prepares the folds for training'''
        X = [] # features
        y = [] # labels

        walk = list(os.walk(self.data_dir))
        walk.sort()
        for i, (subdir, dirs, files) in enumerate(walk):
            if not files:
                continue

            print(f'Creating {subdir}...')
            for idx, f in enumerate(files):
                img = Image.open(subdir+'/'+f)
                img = img.resize(size=input_size)
                img = img.convert('RGB')
                img = np.asarray(img)
                # img = np.transpose((2, 0, 1))
                X.append(img)
                y.append(i-1)

        print(f'{len(X)} total images loaded')
        folds = list(StratifiedKFold(n_splits=n_splits, shuffle=True).split(X, y))
        return folds, np.array(X), np.array(y) #, self.to_categorical(y)
    
    
    @torch.no_grad() # https://deeplizard.com/learn/video/0LhiS6yu2qQ
    def get_predictions(self, model, loader):
        '''Creates a set of predictions given a dataloader and a model.'''
        y_pred = torch.tensor([]).to(self.device, dtype=torch.long)
        y_true = torch.tensor([]).to(self.device, dtype=torch.long)
        
        for images, labels in loader:
            images = images.to(self.device, dtype=torch.float)
            labels = labels.to(self.device, dtype=torch.long)
            
            pred = model(images).to(self.device, dtype=torch.long)
            y_pred = torch.cat((y_pred, pred), dim=0)
            y_true = torch.cat((y_true, labels), dim=0)
            
        return y_pred, y_true
    
    
    def _loop_fn(self, mode, dataset, dataloader, model, criterion, optimizer, ascii_=False):
        '''Inner training loop used to predict on the batches given by the dataloader.'''
        if mode == "train":
            model.train()
        elif mode == "test":
            model.eval()

        cost = correct = 0
        for feature, target in tqdm(dataloader, ascii=ascii_, desc=mode.title()):
            feature, target = feature.to(self.device, dtype=torch.float32), target.to(self.device, dtype=torch.long)
            output = model(feature)
            loss = criterion(output, target)
            model.metric = loss
            
            if mode == "train":
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

            cost += loss.item() * feature.shape[0]
            correct += (output.argmax(1) == target).sum().item()

        cost = cost / len(dataset)
        acc = correct / len(dataset)
        return cost, acc
    

    # https://stackoverflow.com/questions/58996242/cross-validation-for-mnist-dataset-with-pytorch-and-sklearn
    def train(self, model, train_dataset, test_dataset, filepath, criterion, optimizer, fold, epochs=1000, patience=5, scheduler=None, batch_size=16, shuffle=True, min_delta=0):
        '''Training loop used to iterate through multiple epochs.'''
        early_stopping = EarlyStopping(filepath, fold, min_delta=min_delta)
        train_total_loss = []
        train_total_acc = []
        val_total_loss = []
        val_total_acc = []
        test_loader = self.loader(test_dataset, batch_size=batch_size, shuffle=shuffle)
        train_loader = self.loader(train_dataset, batch_size=batch_size, shuffle=shuffle)
            
        for epoch in range(1, epochs+1):
            print(f'\nEpoch {epoch}')
            train_cost, train_score = self._loop_fn("train", train_dataset, train_loader, model, criterion, optimizer, self.device)
            with torch.no_grad():
                test_cost, test_score = self._loop_fn("test", test_dataset, test_loader, model, criterion, optimizer, self.device)
                
            if scheduler:
                scheduler.step(test_cost)
                
            train_total_loss.append(train_cost)
            train_total_acc.append(train_score)
            val_total_loss.append(test_cost)
            val_total_acc.append(test_score)
                
            es_counter = early_stopping.checkpoint(model, epoch, test_cost, test_score, optimizer)
            print(f'\nTrain Loss: {train_cost:.3f}   | Train Acc: {train_score:.4f}  | Val Loss: {test_cost:.3f}   | Val Acc: {test_score:.4f}')
            print(f'Early Stopping Patience at: {es_counter}')
                
            if es_counter == patience:
                DataVisualizationUtilities().display_results(train_total_loss, train_total_acc, val_total_loss, val_total_acc, title=early_stopping.fold_name)
                DataVisualizationUtilities().display_metric_results(early_stopping.best_model, model_name=early_stopping.fold_name, loader=test_loader, train_utils=self, batch_size=batch_size)
                break
            
            epoch += 1
            
        return early_stopping.min_loss, early_stopping.max_acc

    
                           
class EarlyStopping():
    '''Custom made early stopping class. Used for exactly what it sounds like.'''
    def __init__(self, filepath, fold, min_delta=0):
        self.filepath = filepath
        self.min_loss = float('inf')
        self.max_acc = -1
        self.min_delta = min_delta
        self.fold_name = f'model_fold_{fold}_{get_timestamp()}'
        self.path = str(os.path.join(self.filepath, self.fold_name+'.pth'))
        self.count = 0
        self.first_run = True
        self.best_model = None
        
    def checkpoint(self, model, epoch, loss, acc, optimizer):
        '''Creates the checkpoint.'''
        print(f' Loss to beat: {(self.min_loss - self.min_delta):.4f}')
        if (self.min_loss - self.min_delta) > loss or self.first_run:
            self.first_run = False
            self.min_loss = loss
            self.max_acc = acc
            self.best_model = model
            self.count = 0
            torch.save({'epoch': epoch,
                        'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'loss': loss,}, self.path)
            
        else:
            self.count += 1
            
        return self.count
    
          
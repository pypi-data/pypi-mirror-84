from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms

from .dataset import TrainDataset

DEBUG = False

__all__ = ['Network']


class Network(nn.Module):
    def __init__(self, model_name, ctx_id=-1):
        super(Network, self).__init__()
        self.model_name = model_name
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")

    @staticmethod
    def transform_data():
        """
        数据增强函数，可改写
        :return:
        """
        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((224, 224)),  # fix from 224 to 299
                # transforms.RandomCrop(224),
                # transforms.RandomVerticalFlip(),
                transforms.RandomHorizontalFlip(),
                # transforms.RandomRotation(45),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize((224, 224)),
                # transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ])
        }

        return data_transforms

    # def _load_data(self, data_dir, batch_size):
    #     import os
    #     data_transforms = self.transform_data()
    #     image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
    #                       for x in ['train', 'val']}
    #     dataset_loaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True)
    #                        for x in ['train', 'val']}
    #     dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    #
    #     return dataset_loaders, dataset_sizes

    @staticmethod
    def _load_data(data_dir, batch_size, classes):
        import os
        dataset_train = TrainDataset(os.path.join(data_dir, 'train'), classes=classes)
        dataset_train.augment()
        # dataset_train.augment(first=False)
        dataset_val = TrainDataset(os.path.join(data_dir, 'val'), classes=classes)
        print("{} training samples, {} validation samples".format(len(dataset_train), len(dataset_val)))
        dataset_loaders = {"train": torch.utils.data.DataLoader(dataset=dataset_train, batch_size=batch_size),
                           "val": torch.utils.data.DataLoader(dataset=dataset_val, batch_size=batch_size)}
        dataset_sizes = {"train": len(dataset_train),
                         "val": len(dataset_val)}
        return dataset_loaders, dataset_sizes

    def create_model(self, num_classes):
        """
        创建模型，可改写
        :return:
        """
        net = models.resnet18(pretrained=True)
        num_feature = net.fc.in_features
        net.fc = nn.Linear(num_feature, num_classes)
        if torch.cuda.is_available():
            if torch.cuda.device_count() > 1:
                net = nn.DataParallel(net)
            net.cuda()
        return net

    @staticmethod
    def _get_loss_function():
        criterion = nn.CrossEntropyLoss()
        return criterion

    @staticmethod
    def _get_optimizer(model):
        optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=1e-3)
        return optimizer

    @staticmethod
    def _get_lr_function(optimizer, model):
        # 使用cosine
        from .snapshot import CosineAnnealingLR_with_Restart
        lr = CosineAnnealingLR_with_Restart(optimizer, T_max=4, T_mult=1.5, model=model, out_dir="logs",
                                            take_snapshot=True, eta_min=1e-6)
        # Decay LR by a factor of 0.1 every 7 epochs
        # lr = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.8)
        return lr

    def train(self, data_dir, num_classes, batch_size=32, num_epochs=50, classes=[]):
        import time
        if DEBUG:
            from .logger import Logger
        # 1、创建模型
        model = self.create_model(num_classes)
        # 2、加载数据集
        dataset_loaders, dataset_sizes = self._load_data(data_dir, batch_size, classes)
        # 3、定义损失函数
        criterion = self._get_loss_function()
        # 4、定义优化器
        optimizer = self._get_optimizer(model)
        # 5、定义学习率衰减函数
        scheduler = self._get_lr_function(optimizer, model)

        best_acc = 0.0
        train_loss_list, val_loss_list = [], []
        train_acc_list, val_acc_list = [], []
        # 6、训练模型
        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            begin_time = time.time()
            scheduler.step()
            for phase in ['train', 'val']:
                count_batch = 0
                if phase == 'train':
                    model.train(True)  # Set model to training mode
                else:
                    model.train(False)  # Set model to evaluate mode
                running_loss = 0.0
                running_corrects = 0.0
                running_counts = 0
                for inputs, labels in dataset_loaders[phase]:
                    count_batch += 1
                    if torch.cuda.is_available():
                        inputs, labels = inputs.cuda(), labels.cuda()
                    optimizer.zero_grad()
                    # fix 20200926
                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs.data, 1)
                        loss = criterion(outputs, labels)
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data).to(torch.float32)
                    running_counts += preds.shape[0]
                    if count_batch % 1 == 0:
                        batch_loss = running_loss / running_counts
                        batch_acc = running_corrects / running_counts
                        print('{} Epoch [{}] Batch [{}] Loss: {:.4f} Acc: {:.4f} Time: {:.4f}s'. \
                              format(phase, epoch, count_batch, batch_loss, batch_acc, time.time() - begin_time))
                        begin_time = time.time()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects / dataset_sizes[phase]
                print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

                if phase == "train":
                    train_loss_list.append(epoch_loss)
                    train_acc_list.append(epoch_acc)
                else:
                    val_loss_list.append(epoch_loss)
                    val_acc_list.append(epoch_acc)

                if DEBUG:
                    # (1) Log the scalar values
                    info = {'loss': epoch_loss, 'accuracy': epoch_acc}
                    if phase == 'train':
                        logger = Logger('./logs/train')
                    else:
                        logger = Logger('./logs/val')

                    for tag, value in info.items():
                        logger.scalar_summary(tag, value, epoch)

                    # (2) Log values and gradients of the parameters (histogram)
                    for tag, value in model.named_parameters():
                        tag = tag.replace('.', '/')
                        logger.histo_summary(tag, value.data.cpu().numpy(), epoch)
                        logger.histo_summary(tag + '/grad', value.grad.data.cpu().numpy(), epoch)

                    # (3) Log the images
                    info = {'images': inputs.view(-1, 3, 224, 224)[:5].cpu().data.numpy()}

                    for tag, images in info.items():
                        logger.image_summary(tag, images, epoch)

                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    print('Best val Acc: {:4f}'.format(best_acc))
                    # 7、保存模型
                    torch.save(model,
                               self.model_name.split('_')[0] + "_" + str(epoch) + "_" + str(float(best_acc)) + ".pth")

        # 8、显示
        import numpy as np
        import matplotlib.pyplot as plt

        x = np.arange(0, len(train_loss_list))
        plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plt.plot(x, train_loss_list, color='r')
        plt.plot(x, val_loss_list, color='g')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(['train_loss', 'test_loss'], loc=4)
        plt.title('loss curve')

        plt.subplot(122)
        plt.plot(x, train_acc_list, color='r')
        plt.plot(x, val_acc_list, color='g')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend(['train_acc', 'test_acc'], loc=4)
        plt.title('acc curve')

        plt.savefig("loss_acc.jpg")

        return model

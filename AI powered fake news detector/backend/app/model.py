import torch
import torch.nn as nn
from transformers import BertModel
import torchvision.models as models

class MultiModalModel(nn.Module):
    def __init__(self, num_labels):
        super(MultiModalModel, self).__init__()

        # BERT for text
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.text_fc = nn.Linear(self.bert.config.hidden_size, 256)

        # ResNet50 for image
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad = False  # Freeze resnet
        resnet.fc = nn.Identity()  # Remove last layer
        self.resnet = resnet
        self.image_fc = nn.Linear(2048, 256)

        # Final classifier
        self.classifier = nn.Sequential(
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_labels)
        )

    def forward(self, input_ids, attention_mask, image):
        text_feat = self.bert(input_ids=input_ids, attention_mask=attention_mask).pooler_output
        text_feat = self.text_fc(text_feat)

        img_feat = self.resnet(image)
        img_feat = self.image_fc(img_feat)

        combined = torch.cat((text_feat, img_feat), dim=1)
        output = self.classifier(combined)
        return output

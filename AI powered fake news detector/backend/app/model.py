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

    def forward(self, input_ids, attention_mask, image=None):
        try:
            # Process text
            print("Processing text with BERT...")
            text_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
            text_feat = text_output.pooler_output
            print(f"BERT output shape: {text_feat.shape}")
            text_feat = self.text_fc(text_feat)
            print(f"Text feature shape after FC: {text_feat.shape}")

            # If image is provided, process it and combine with text features
            if image is not None:
                print(f"Forward pass - Input shapes: text={input_ids.shape}, image={image.shape}")
                
                # Process image
                print("Processing image with ResNet...")
                img_feat = self.resnet(image)
                print(f"ResNet output shape: {img_feat.shape}")
                img_feat = self.image_fc(img_feat)
                print(f"Image feature shape after FC: {img_feat.shape}")

                # Combine features
                print("Combining text and image features...")
                combined = torch.cat((text_feat, img_feat), dim=1)
                print(f"Combined feature shape: {combined.shape}")
            else:
                # For text-only mode, create a zero tensor with the same shape as image features
                print("Image not provided, using text-only mode")
                batch_size = text_feat.size(0)
                img_feat = torch.zeros(batch_size, 256, device=text_feat.device)
                combined = torch.cat((text_feat, img_feat), dim=1)
                print(f"Combined feature shape (text-only): {combined.shape}")
            
            # Final classification
            print("Running classifier...")
            output = self.classifier(combined)
            print(f"Output shape: {output.shape}")
            
            return output
            
        except Exception as e:
            print(f"Error in model forward pass: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

import torch 
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from fastapi import FastAPI, UploadFile, File
from PIL import Image

model = models.resnet18()
model.fc = nn.Linear(model.fc.in_features, 10)
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# FastAPI 
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Model API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Load Image
    image = Image.open(file.file).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)
    
    # Predict 
    with torch.no_grad():
        outputs = model(img_tensor)
        pred = torch.argmax(outputs, dim=1).item()
        
    return {"prediction": int(pred)}
from core import SpikitDataset
from torch.utils.data import DataLoader

# Initialize Spikit Dataset with DatasetId
dataset = SpikitDataset(dataset_id='DATASET-a8c46a8b-0d6f-11eb-ac1d-1f554c27758e')

# Access included Zarr array
print(dataset.array)

# Plug-in to Pytorch DataLoader
loader = DataLoader(dataset, batch_size=4)

# Print all of the batches (batching handled by PyTorch DataLoader)
for batch in loader:
    print(batch)
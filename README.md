# sketch-identifier
A Sketch identifier example using tensorflow and google quickdraw dataset.

To train the CNN with the specified project specifications you must download
the data first and place it in a data/ directory:

#Installation

```bash
pip install -r requirements.txt
```

# Running sketcher
This repo has a pre trained CNN (85% Accuracy) when you clone it so you can just run the following command to test the sketcher

```bash
python sketcher.py
```


# Training

From project root run:
```bash
mkdir data && cd data/
gsutil -m cp 'gs://quickdraw_dataset/full/numpy_bitmap/*.npy' .
```
This downloads around 36GB of data, now to train your CNN, just run:

```bash
python sketcher.py -train
```

For the sketcher user interface after training
```bash
python sketcher.py
```



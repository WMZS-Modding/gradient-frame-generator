# Gradient Frame Generator
A Python application can help you create the frames based on input and output images

## Features
### Main features
- Load input and output images
- Choose input and output colors
- Choose frames by using a slider (Maximum: 500)
- Generate frames of your gradient

### Sub features
Frame Extractor: It's useful if you don't want to extract frames of 1 sprite sheet image manually with your photo editor/paint tools

## Requirements
You need to install `Pillow`:

```bash
pip install pillow
```

## Installation
You have 2 methods to use this application:
1. Download from [Releases](https://github.com/WMZS-Modding/gradient-frame-generator/releases)
2. Clone repository:

```bash
git clone https://github.com/WMZS-Modding/gradient-frame-generator.git
```

And then run:

```bash
python main.py
```

## Usage
### Frame Extractor
#### Single Image
1. Open the application
2. Choose `Frame Extractor` section
3. Choose your sprite sheet image
4. Edit the `Frame Height` and `Frame Width`
5. Click `EXTRACT FRAMES` button
6. Go to `save/frames_<number>/` and copy these frame images

#### Folder Batch
1. Open the application
2. Choose `Frame Extractor` section
3. Choose `Folder Batch` section
4. Click `Browse Folder` button to choose your folder of sprite sheets
5. Click `EXTRACT FRAMES` button
6. Go to `save/frames_<number>/` and copy these frame images

### Manual mode
1. Open the application
2. Choose your input and output images (they must be the same)
3. Choose your colors to your gradient
4. Choose your frames you want
5. Click `START GENERATION` button
6. Go to `save/gradient_frame_<number>/` and copy these gradient frame images

### Automatic mode
1. Open the application
2. Tick `Auto mode`
3. Choose your input and output images (they must be the same)
4. Choose your frames you want
5. Click `START GENERATION` button
6. Go to `save/gradient_frame_<number>/` and copy these gradient frame images

## Advantages and Disadvantages
### Manual mode
- Advantages: Gives you the correct result. It can handle both two identical input colors in image 1 and two different output colors in image 2
- Disadvantages: Still wastes your time because you must add colors manually. And it maybe make a mistake if you don't add missing colors

### Automatic mode
- Advantages: Gives you the same result as manual mode. It can still handle both two identical input colors in image 1 and two different output colors in image 2. The only different is it doesn't requires adding colors manually
- Disadvantages: Difficult to control because it scans both images simultaneously

#### Single Image
- Advantages: Can extract accurately frame sizes by entering width and height
- Disadvantages: For single image only, still waste your time

#### Folder Batch
- Advantages: Extremely fast. It can handle your folder of sprite sheets no matter they have different frame sizes
- Disadvantages: Sometimes it can output frames with incorrect original dimensions for sprite sheets with different frame sizes. I recommend separating folders that has different sprite sheets with different frame sizes, it's even faster than handling the whole them

## Note
If you don't want 500 frames limit, you can follow these step to change limit:
1. Fork this repository
2. Go to `main.py`
3. Change this code:

```python
self.frame_slider = tk.Scale(slider_frame, from_=2, to=500, variable=self.frame_count_var, orient=tk.HORIZONTAL, length=300)
```

Warning: Only change `to=500`, **don't** set it to `to=2` and change `from_=2` or they'll cause errors

4. Push your change to your forked repository and then run `release_assets.yml`

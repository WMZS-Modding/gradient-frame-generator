# Gradient Frame Generator
A Python application can help you create the frames based on input and output images

## Features
- Load input and output images
- Choose input and output colors
- Choose frames by using a slider (Maximum: 500)
- Generate frames of your gradient

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
1. Open the app
2. Choose your input and output images (must be the same)
3. Choose your colors to your gradient
4. Choose your frames you want
5. Click `START GENERATION` button
6. Go to `save/gradient-frame-<number>/` and copy these gradient frame images

## Note
If you don't want 500 frames limit, you can follow these step to change limit:
1. Fork this repository
2. Go to `main.py`
3. Change this code:

```python
self.frame_slider = tk.Scale(slider_frame, from_=2, to=500, variable=self.frame_count_var, orient=tk.HORIZONTAL, length=300)
```

Warning: Only change `to=500`, don't change `from_=2` or it'll error

4. Push your change to your forked repository and then run `release_assets.yml`
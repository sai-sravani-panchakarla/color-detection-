import cv2
import pandas as pd

img_path = r'pic2 (1).jpg'
csv_path = r'colors.csv'

#  Read the CSV file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Read and resize the image
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to get the closest color name
def get_color_name(R, G, B):
    minimum = 1000
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

#  Mouse click callback function
def draw_function(event, x, y, flags, params):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Create OpenCV window and set callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

#  Main loop
while True:
    cv2.imshow('image', img)

    if clicked:
        # Draw rectangle and display color info
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + f' R={r} G={g} B={b}'

        # Decide text color based on brightness
        text_color = (0, 0, 0) if r + g + b >= 600 else (255, 255, 255)

        cv2.putText(img, text, (50, 50), 2, 0.8, text_color, 2, cv2.LINE_AA)

    # Press 'Esc' key to exit
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

import pytesseract as pt
import cv2
import concurrent.futures
from time import time
from dotenv import load_dotenv, dotenv_values
load_dotenv()
pt.pytesseract.tesseract_cmd = dotenv_values()['TESSERACT_PATH']


def process_cell(i, j, gray, cell_height, cell_width):
    cell = gray[int(i * cell_height):int((i + 1) * cell_height),
                int(j * cell_width):int((j + 1) * cell_width)]
    cell = cell[10:cell.shape[0] - 10, 10:cell.shape[1] - 10]
    cell = cv2.threshold(
        cell, 240, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cell = cv2.resize(cell, (28, 28), interpolation=cv2.INTER_AREA)
    cell = cv2.dilate(cell, (3, 3))
    number = pt.image_to_string(
        cell, lang='eng', config='-c tessedit_char_whitelist=123456789 --psm 6')
    if number == '':
        return ''
    else:
        return int(number.split('\n')[0])


def extract_data(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    height, width = gray.shape
    cell_width = width / 9
    cell_height = height / 9

    grid = []
    start = time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            process_cell, i, j, gray, cell_height, cell_width) for i in range(9) for j in range(9)]
        results = [f.result() for f in futures]
        for i in range(9):
            grid.append(results[i*9:i*9+9])
    print(time() - start)
    return grid

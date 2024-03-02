import fitz
import pytesseract
import io
from PIL import Image
from tqdm import tqdm


def get_text_data(file_path):
    doc = fitz.open(file_path)

    text = ""

    for page_num in tqdm(range(doc.page_count)):
        page = doc[page_num]
        # image = page.get_pixmap(alpha=False)
        #
        # disp_img = Image.open(io.BytesIO(image.tobytes()))
        #
        # # To see the image
        # # import matplotlib.pyplot as plt
        # # plt.imshow(disp_img)
        # # plt.show()
        #
        # text += pytesseract.image_to_string(disp_img)
        # # print(text)

        text += page.get_text()

    return text




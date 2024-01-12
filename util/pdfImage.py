import fitz  # PyMuPDF
from PIL import Image
import os,io,base64
from .constants import outputDir

desired_dpi = 300


def convertToPageImage(filename):
    """
        take the file path and return list of page as images data in base64 format
    """
    # Open the PDF file
    pdf_document = fitz.open(filename) # type: ignore

    base64_images = []  

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the specific page
        page = pdf_document.load_page(page_number)

        # Render the page as an image with the desired DPI
        pix = page.get_pixmap(matrix=fitz.Matrix(desired_dpi / 72, desired_dpi / 72),alpha=False)

        
        # Convert the page to an image
        pix = page.get_pixmap()

        # Create a BytesIO object to hold the image data
        img_bytes_io = io.BytesIO()

        # Convert the image to JPG format and save it to the BytesIO object
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples) # type: ignore
        img.save(img_bytes_io, format="JPEG")
        
        # # save image
        # with open(os.path.join(outputDir, f"{page_number}.jpg"), "wb") as f:
        #     f.write(img_bytes_io.getvalue())

        # Get the JPG image data as bytes
        jpg_image_data = img_bytes_io.getvalue()
        # print(type(jpg_image_data))

        # Encode the image data as Base64 and append it to the list
        base64_image_data = base64.b64encode(jpg_image_data).decode('utf-8')
        base64_images.append(f"data:image/jpeg;base64,{base64_image_data}")

    # Close the PDF file
    pdf_document.close()

    # 'all_pages' now contains all the pages of the PDF
    return base64_images


def extractTextAndLinksFromPDF(filePath):
    # read file from path
    result = ""

    with fitz.open(filePath) as pdf_file: # type: ignore
        for page_index in range(len(pdf_file)):
            # get the page
            page = pdf_file[page_index]
            # get the text
            text = page.get_text("text")
            # clean the text
            text = text.replace("\r", " ").replace("\n", "  ")
            # get links on the page
            page_links = " ".join([ x.get('uri', '') for x in page.links()])
            result += text + "\n" + page_links + "\n"

    # return the final result
    return result

if __name__ == '__main__':
    # get all the pdf files from the directory
    pdf_files = [
        os.path.join(outputDir, f) for f in os.listdir(outputDir) if os.path.isfile(os.path.join(outputDir, f)) and f.endswith('.pdf')]
    # Input PDF file path
    pdf_file = pdf_files[0]
    print(pdf_file)
    image = convertToPageImage(pdf_file)
    print(len(image))
    with open('tes','a') as f:
        f.write(image[0])
    # print("https://data:"+image[0])
import fitz  # PyMuPDF
import os
import requests

def download_pdf(url, save_path):
    """
    Downloads a PDF file from a URL and saves it locally.
    
    Args:
        url (str): The URL of the PDF file.
        save_path (str): The path to save the downloaded PDF file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded PDF from {url} to {save_path}")
    else:
        raise Exception(f"Failed to download the PDF. HTTP Status Code: {response.status_code}")


def extract_images_from_pdf(pdf_path, output_folder):
    """
    Extracts all images from a PDF using PyMuPDF and saves them as separate files.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Directory to save the extracted images.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    image_count = 0  # Counter for images

    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)  # Get all images on the page
        
        # If there are no images, skip the page
        if not images:
            continue
        
        for img_index, img in enumerate(images):
            xref = img[0]  # Reference to the image object
            base_image = pdf_document.extract_image(xref)  # Extract image details
            image_bytes = base_image["image"]  # Raw image data
            image_ext = base_image["ext"]  # Image file extension (e.g., png, jpeg)
            
            # Save the image to the output folder
            image_filename = f"page_{page_number + 1}_image_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)
            
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            print(f"Saved image: {image_path}")
            image_count += 1
    
    pdf_document.close()
    print(f"\nTotal images extracted: {image_count}")


# Specify the link to the PDF file and output folder
pdf_url = "https://monet.en.kku.ac.th/courses/EN812303/book/Introduction.to.Algorithms.4th.Edition.pdf"  # Replace with the actual URL of the PDF
downloaded_pdf_path = "downloaded_book.pdf"  # Name to save the downloaded PDF
output_folder = "/home/peter/Downloads/extracted_images"  # Folder to save extracted images

# Download the PDF and extract images
download_pdf(pdf_url, downloaded_pdf_path)
extract_images_from_pdf(downloaded_pdf_path, output_folder)
